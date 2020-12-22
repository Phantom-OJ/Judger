import time
import json
import psycopg2
from ConnectionAndContainer import getContainerAndConnection
import traceback
judge_select="with user_answer as (%s), standard_answer as (%s)select count(*) as count from ((select * from user_answer except select * from standard_answer)  union (select * from  standard_answer except select * from user_answer))a;"


def judgePgsql(judgeInputMessage:dict,judgeResultMessage:dict):
    try:
        judgeResults=list()
        for judgeInput in judgeInputMessage['judgeInputs']:
            print("judgeInput:", judgeInput)
            databaseinfo=judgeInput.get("JudgeDatabase")
            databaseinfo['user'] = 'postgres'
            databaseinfo['password'] = 'abc123'
            databaseinfo['port'] = '5432/tcp'
            container, connection = getContainerAndConnection(databaseinfo=judgeInput.get("JudgeDatabase"),driver=psycopg2)
            judgefunction = judge_select
            if (judgeInput['additionFields']['type'] == 'select'):
                judgefunction = select
            elif (judgeInput['additionFields']['type'] == 'trigger'):
                judgefunction = trigger
            else:
                pass
            # judgeResult = judge_with_time_out(judgefunction, connection=connection, judgeInput=judgeInput,
            #                                   timeout=judgeInput['timeLimit'])
            judgeResult = judgefunction(connection,judgeInput)
            print("judgeResult:", judgeResult)
            judgeResults.append(judgeResult)
            container.stop()
        judgeResultMessage['judgeResults'] = judgeResults
        judgeResultMessage['problemId'] = judgeInputMessage['problemId']
        judgeResultMessage['codeId'] = judgeInputMessage['codeId']
        judgeResultMessage['userId'] = judgeInputMessage['userId']
    except Exception as e:
        traceback.print_stack()
        print(e)
    return json.dumps(judgeResultMessage)

def select(connection,judgeInput):
    judgeResult = dict()
    cur = connection.cursor()
    time_start=time.time_ns()
    userInput=judgeInput['userInput'].replace(";","")
    standardAnswer=judgeInput['standardAnswer'].replace(";","")

    sql=judge_select%(userInput,standardAnswer)
    print(sql)
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        judgeResult['code']=4
        judgeResult['codeDescription'] = "Runtime Error"
        judgeResult['runTime'] = 0
        return judgeResult

    time_end=time.time_ns()

    time_cost=(time_end-time_start)//(10**6)
    difference=cur.fetchall()[0]

    if(difference[0]==0):
        judgeResult['code']=0
        judgeResult['codeDescription']="Answer Correct"

    else:
        judgeResult['code']=3
        judgeResult['codeDescription'] = "There are %d rows varing from correct answer"%(difference)
    judgeResult['runTime']=time_cost
    print("一个判题点结束",judgeResult)
    return judgeResult

def trigger(connection,judgeInput):

    connection.autocommit=True
    cur = connection.cursor()
    time_start=time.time_ns()
    if(judgeInput.get('beforeInput')):
        cur.execute(judgeInput['beforeInput'])
    try:
        cur.execute(judgeInput['userInput'])
    except Exception as e:
            print(e)
    sqls=judgeInput['afterInput'].split(";")
    for sql in sqls:
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
    result=cur.fetchall()
    # index=[index for index in range(1,len(result)+1)]
    # dic_result=dict(zip(index,result))
    # print("学生执行结果",dic_result)
    # file=open("answer.txt",'w',encoding='UTF-8')
    # print(json.dumps(dic_result),file=file)
    # file.close()
    standard_answer=judgeInput['standardAnswer']

    for i in range(0,standard_answer.__len__()):
        standard_answer[i]=tuple(standard_answer[i].split("|"))

    print("standardAnswerAfterparse:",standard_answer)

    lackset=set(standard_answer) - set(result)
    exceedset=set(result)- set(standard_answer)
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
        judgeResult['code']=3
        judgeResult['codeDescription'] = "There are %d rows lack and %d rows exceed from correct answer"%(lacknum,exceednum)
    judgeResult['runTime']=time_cost
    print("一个判题点结束",judgeResult)
    return judgeResult