import json
import time
import redis
import docker
import traceback
import sys
import os
import argparse
import multiprocessing
import Constant
from multiprocessing.dummy import Pool as ThreadPool
import ConnectionAndContainer
from MysqlJudge import judgeMysql
from PostgresJudge import judgePgsql
from judgeSqlite import judgeSqlite

str123='{"judgeDatabaseUrl":"jdbc:postgresql://localhost:5432/testJson","userName": "testJson","passWord": "abc123","userInput": "SELECT title, country, year_released FROM movies WHERE country <>\"us\" AND year_released = 1991 AND title LIKE \'The%\'","standardAnswer": "SELECT title, country, year_released FROM movies WHERE country <>\'us\' AND year_released = 1991 AND title LIKE \"The%\"","timeLimit": "2000"}'
judge_select="with user_answer as (%s), standard_answer as (%s)select count(*) as count from ((select * from user_answer except select * from standard_answer)  union (select * from  standard_answer except select * from user_answer))a;"
wait_time=0.5

        #time.sleep(wait_time)

def beginListen(redishost='10.20.87.51',port=6379,dbnumber=2):
    redisclient = redis.Redis(host=redishost, port=port, decode_responses=True,db=dbnumber)
    while(1):
        message=redisclient.brpoplpush("judgelist","test1",0)
        try:
            print(message)
            judgeInputMessage=json.loads(message)
            start=time.time()
            judgeResultMessage=judgeRoot(judgeInputMessage)
            print("要放进redis里的:", judgeResultMessage)
            redisclient.lpush("result", judgeResultMessage)
            end=time.time()
            print("判题机处理时间:%f seconds"%(end-start))
        except Exception as e:
            traceback.print_stack()
            print("发生错误，但可以继续监听")
            print(e)
            redisclient.lpush("result", throwServerError(message))


def trigger_sqlite():
    pass



def thrownodialectError(judgeInputMessage:dict,judgeResultMessage:dict):
    judgeResults=list()
    for judgeInput in judgeInputMessage['judgeInputs']:
        judgeResult = dict()
        judgeResult['code'] = 8
        judgeResult['codeDescription'] = "dialect not supported"
        judgeResult['runTime'] = 0
        judgeResults.append(judgeResult)
    judgeResultMessage['judgeResults'] = judgeResults
    judgeResultMessage['problemId'] = judgeInputMessage['problemId']
    judgeResultMessage['codeId'] = judgeInputMessage['codeId']
    judgeResultMessage['userId'] = judgeInputMessage['userId']
    judgeResultMessage = json.dumps(judgeResultMessage)
    return judgeResultMessage
def throwServerError(message:dict):
    judgeResultMessage=dict()
    judgeResults=list()
    judgeInputMessage=json.loads(message)
    for judgeInput in judgeInputMessage['judgeInputs']:
        judgeResult = dict()
        judgeResult['code'] = Constant.SE
        judgeResult['codeDescription'] = Constant.SE_DESCRIPTION
        judgeResult['runTime'] = 0
        judgeResults.append(judgeResult)
    judgeResultMessage['judgeResults'] = judgeResults
    judgeResultMessage['problemId'] = judgeInputMessage['problemId']
    judgeResultMessage['codeId'] = judgeInputMessage['codeId']
    judgeResultMessage['userId'] = judgeInputMessage['userId']
    judgeResultMessage['recordId']=judgeInputMessage['recordId']
    judgeResultMessage = json.dumps(judgeResultMessage)
    return judgeResultMessage

def copy(source,target):
    try:
        os.system("cp %s %s"%(source, target))
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

def judgeRoot(judgeInputMessage:dict):
    judgeResultMessage=dict()
    judgeResultMessage['problemId'] = judgeInputMessage['problemId']
    judgeResultMessage['codeId'] = judgeInputMessage['codeId']
    judgeResultMessage['userId'] = judgeInputMessage['userId']
    judgeResultMessage['recordId']=judgeInputMessage.get('recordId')
    dialect=judgeInputMessage.get("dialect",None)
    #TODO 在这里try catch一下应该可以保证不会报错
    if(dialect=='pgsql'):
        judgePgsql(judgeInputMessage,judgeResultMessage)
    elif(dialect=='mysql'):
        judgeMysql(judgeInputMessage,judgeResultMessage)
    elif(dialect=='sqlite'):
        judgeSqlite(judgeInputMessage,judgeResultMessage)
    else:
        thrownodialectError(judgeInputMessage,judgeResultMessage)
    return  json.dumps(judgeResultMessage)


def judge_with_time_out(judge_function, *args, **kwargs):
    timeout = kwargs.get('timeout', None)
    judgeInput = kwargs.get('judgeInput', None)
    connection=kwargs.get('connection',None)
    print("timeout:",timeout)
    p = ThreadPool(1)
    res = p.apply_async(judge_function, args=(connection,judgeInput))
    judgeResult = dict()
    try:
        judgeResult = res.get(1)  # Wait timeout seconds for func to complete.
    except multiprocessing.TimeoutError:
        print("Aborting due to timeout")
        judgeResult['code']=2
        judgeResult['codeDescription']="Time Limit Exceed"
    finally:
        return judgeResult



def testOneJudge():
    (port, container, connection) = (0, 0, 0)
    client = redis.Redis(host='10.20.87.51', port=6379, decode_responses=True)
    message = client.lindex("judgelist", 0)
    print(message)
    judgeInputMessage = json.loads(message)
    judgeRoot(judgeInputMessage, redisclient=client)

def param_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument( "--redishost", type=str, default="10.20.87.51")
    parser.add_argument( "--redisport", type=int, default=6379)
    parser.add_argument("--dbnumber", type=int, default=2)
    parser.add_argument( "--maxhost", type=int, default=5)
    parser.add_argument( "--wait_time", type=int, default=2)

    args = parser.parse_args()
    redishost=args.redishost
    port = args.redisport
    dbnumber=args.dbnumber
    maxhost = args.maxhost
    wait_time = args.wait_time
    return redishost,port,dbnumber,maxhost,wait_time

if __name__ == '__main__':
    # 1.开启循环创建docker容器的进程
    redishost, port,dbnumber, maxhost, wait_time=param_parse()
    p=multiprocessing.Process(target=ConnectionAndContainer.containerRefresh,args=())
    p.start()
    # 2.开启redis队列监听服务
    beginListen(redishost,port,dbnumber)



