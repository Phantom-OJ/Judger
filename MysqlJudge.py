import time
import json
import traceback
import pymysql
from ConnectionAndContainer import getContainerAndConnection



def judgeMysql(judgeInputMessage:dict,judgeResultMessage:dict):

    judgeResults = list()
    filt = {"ancestor": "judge-mysql:1.0"}
    for judgeInput in judgeInputMessage['judgeInputs']:
        print("judgeInput:", judgeInput)
        databaseinfo=judgeInput.get("JudgeDatabase")
        print("dadabaseInfo:",databaseinfo)
        databaseinfo['user']='root'
        databaseinfo['password']='abc123'
        databaseinfo['port']='3306/tcp'
        container, connection = getContainerAndConnection(databaseinfo=databaseinfo,driver=pymysql)
        judgefunction = select_mysql
        if (judgeInput['additionFields']['type'] == 'select'):
            judgefunction = select_mysql
        elif (judgeInput['additionFields']['type'] == 'trigger'):
            judgefunction = trigger
        judgeResult=judgefunction(connection,judgeInput)
        # judgeResult = judge_with_time_out(judgefunction, connection=connection, judgeInput=judgeInput,
        #                                   timeout=judgeInput['timeLimit'])
        print("judgeResult:", judgeResult)
        judgeResults.append(judgeResult)
        container.stop()
    judgeResultMessage['judgeResults'] = judgeResults
    judgeResultMessage['problemId'] = judgeInputMessage['problemId']
    judgeResultMessage['codeId'] = judgeInputMessage['codeId']
    judgeResultMessage['userId'] = judgeInputMessage['userId']
    judgeResultMessage = json.dumps(judgeResultMessage)
    return judgeResultMessage

def select_mysql(connection,judgeInput):
    judgeResult = dict()
    try:
        cur = connection.cursor()
        sql1=judgeInput['standardAnswer']
        cur.execute(sql1)
        answer=set(cur.fetchall())
        time_start=time.time_ns()
        sql2=judgeInput['userInput']
        cur.execute(sql2)
        time_end = time.time_ns()
        userResult=set(cur.fetchall())
        lack_set=answer-userResult
        exceed_set=userResult-answer
        lack_num=len(lack_set)
        exceed_num=len(exceed_set)
        time_cost=(time_end-time_start)//(10**6)

        if (lack_num == 0 and exceed_num == 0):
            judgeResult['code']=0
            judgeResult['codeDescription']="Answer Correct"
        else:
            judgeResult['code']=3
            judgeResult['codeDescription'] = "There are %d rows lacking and %d rows exceeding varing from correct answer"%(lack_num,exceed_num)
        judgeResult['runTime']=time_cost
        print("一个判题点结束",judgeResult)
        return judgeResult
    except Exception as e:
        traceback.print_stack()
        print(e)
        judgeResult['code'] = 3
        judgeResult['codeDescription'] = "WA"
        judgeResult['runTime'] = 0
        return judgeResult

def trigger(connection,judgeInput):
    connection.autocommit=True
    cur = connection.cursor()
    time_start=time.time_ns()
    if(judgeInput.get('beforeInput')):
        cur.execute(judgeInput['beforeInput'])
    try:
        cur.execute("")
    except Exception as e:
            print(e)
    sqls=judgeInput['afterInput'].split(";")
    for sql in sqls:
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
    result=cur.fetchall()
    index=[index for index in range(1,len(result)+1)]
    dic_result=dict(zip(index,result))
    print("学生执行结果",dic_result)
    file=open("answer.txt",'w',encoding='UTF-8')
    print(json.dumps(dic_result),file=file)
    file.close()
    standard_answer=json.loads(judgeInput['standardAnswer'])

    for key in standard_answer.keys():
        standard_answer[key]=tuple(standard_answer[key])

    lackset=set(standard_answer.values()) - set(dic_result.values())
    exceedset=set(dic_result.values())- set(standard_answer.values())
    print("lackset is ",lackset)
    print("exceed set is ",exceedset)

    lacknum=len(lackset)
    exceednum=len(exceedset)
    print("两个集合的差",)
    print("答案:", standard_answer)

    time_end=time.time_ns()
    time_cost=(time_end-time_start)//(10**6)
    judgeResult=dict()
    if(lacknum==0 and exceednum==0):
        judgeResult['code']=0
        judgeResult['codeDescription']="Answer Correct"
    else:
        judgeResult['code']=1
        judgeResult['codeDescription'] = "There are %d rows lack and %d rows exceed from correct answer"%(lacknum,exceednum)
    judgeResult['runTime']=time_cost
    print("一个判题点结束",judgeResult)
    return judgeResult