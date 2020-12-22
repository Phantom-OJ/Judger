import sys
import os
import sqlite3
import json
import time
import shutil

def judgeSqlite(judgeInputMessage:dict,judgeResultMessage:dict):
    print("使用sqlite方法判题")
    judgeResults = list()
    for judgeInput in judgeInputMessage['judgeInputs']:
        databaseinfo = judgeInput.get("JudgeDatabase")
        print("judgeInput:", judgeInput)
        shutil.copy("resources\\filmdb.sqlite","filmdb.sqlite")
        judgefunction = select_sqlite
        if (judgeInput['additionFields']['type'] == 'select'):
            judgefunction = select_sqlite
        elif (judgeInput['additionFields']['type'] == 'trigger'):
            pass
        judgeResult = judgefunction(filename="filmdb.sqlite",judgeInput=judgeInput)
        print("judgeResult:", judgeResult)
        judgeResults.append(judgeResult)
    judgeResultMessage['judgeResults'] = judgeResults
    judgeResultMessage['problemId'] = judgeInputMessage['problemId']
    judgeResultMessage['codeId'] = judgeInputMessage['codeId']
    judgeResultMessage['userId'] = judgeInputMessage['userId']
    judgeResultMessage = json.dumps(judgeResultMessage)
    return judgeResultMessage

def select_sqlite(filename,judgeInput):
    conn=sqlite3.connect(".\\filmdb.sqlite")
    cur=conn.cursor()
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
    print("userResult:",userResult)
    print("answer:",answer)
    time_cost=(time_end-time_start)//(10**6)
    judgeResult=dict()
    if (lack_num == 0 and exceed_num == 0):
        judgeResult['code']=0
        judgeResult['codeDescription']="Answer Correct"
    else:
        judgeResult['code']=3
        judgeResult['codeDescription'] = "There are %d rows lacking and %d rows exceeding varing from correct answer"%(lack_num,exceed_num)
    judgeResult['runTime']=time_cost
    print("一个判题点结束",judgeResult)
    return judgeResult

if __name__=="__main__":
    shutil.copy("resources\\filmdb.sqlite", "filmdb.sqlite")