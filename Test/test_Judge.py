import redis
import json
import time
import unittest
import pytest

redisClient = redis.Redis(host='10.20.87.51', port=6379, decode_responses=True,db=3)

times = 1


def test_Range():
    for i in range(0, times):
        print(times)

@pytest.mark.parametrize("jsonFilePath", ["../testJson/postgres/windowFunction_AC.json", "../testJson/postgres/joinInput_AC.json"])
def test_postgre_windowFuntion(jsonFilePath):
    file=open(jsonFilePath,encoding="utf8")
    judgeInputMessage=json.load(file)
    #print(file.readlines())
    message=json.dumps(judgeInputMessage)
    print("发送：",message)
    redisClient.lpush("judgelist",message)
    result = redisClient.brpop("result", 5)
    assert result
    print(result)

@pytest.mark.parametrize("jsonFilePath", ["../testJson/sqlite/"])
def testAll_sqlite(jsonFilePath):
    import os
    datanames = os.listdir(jsonFilePath)
    for dataname in datanames:
        if os.path.splitext(dataname)[1] == '.json':  # 目录下包含.json的文件
            start = time.time()
            relativePath=jsonFilePath+dataname
            print(relativePath)
            file = open(relativePath, encoding="utf8")
            judgeInputMessage = json.load(file)
            file.close()
            message = json.dumps(judgeInputMessage)
            print("发送：", message)
            redisClient.lpush("judgelist", message)
            totalTime = 0
            result = redisClient.brpop("result", 5)
            print(relativePath,",判题结果:",result)
            end = time.time()
            totalTime += end - start
            print("totalTime:", totalTime)


@pytest.mark.parametrize("jsonFilePath", ["../testJson/postgres/"])
def testAll_postgres(jsonFilePath):
    import os
    datanames = os.listdir(jsonFilePath)
    for dataname in datanames:
        if os.path.splitext(dataname)[1] == '.json':  # 目录下包含.json的文件
            start = time.time()
            relativePath=jsonFilePath+dataname
            print(relativePath)
            file = open(relativePath, encoding="utf8")
            judgeInputMessage = json.load(file)
            file.close()
            message = json.dumps(judgeInputMessage)
            print("发送：", message)
            redisClient.lpush("judgelist", message)
            totalTime = 0
            result = redisClient.brpop("result", 5)
            print(relativePath,",判题结果:",result)
            end = time.time()
            totalTime += end - start
            print("totalTime:", totalTime)

@pytest.mark.parametrize("jsonFilePath", ["../testJson/mysql/"])
def testAll_mysql(jsonFilePath):
    import os
    datanames = os.listdir(jsonFilePath)
    for dataname in datanames:
        if dataname.endswith('joinInput_AC.json'):  # 目录下包含.json的文件
            start = time.time()
            relativePath=jsonFilePath+dataname
            print(relativePath)
            file = open(relativePath, encoding="utf8")
            judgeInputMessage = json.load(file)
            file.close()
            message = json.dumps(judgeInputMessage)
            print("发送：", message)
            redisClient.lpush("judgelist", message)
            totalTime = 0
            result = redisClient.brpop("result", 5)
            print(relativePath,",判题结果:",result)
            end = time.time()
            totalTime += end - start
            print("totalTime:", totalTime)



def test_PostgresSelect_nobefore():
    for i in range(0, times):
        judgedatabase = dict()
        judgedatabase['image_id'] = "judgedb:2.0"
        judgedatabase['database'] = "postgres"

        judgeInputs = list()
        judgeInput = dict()
        additionalType = dict()
        additionalType['type'] = 'select'
        judgeInput['JudgeDatabase'] = judgedatabase
        judgeInput[
            'userInput'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInput['timeLimit'] = 10000
        judgeInput['additionFields'] = additionalType
        judgeInput[
            'standardAnswer'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInputs.append(judgeInput)
        judgeInputmessage = dict()
        judgeInputmessage['judgeInputs'] = judgeInputs
        judgeInputmessage['codeId'] = 18
        judgeInputmessage['problemId'] = 1
        judgeInputmessage["userId"] = 1
        judgeInputmessage["dialect"] = "pgsql"
        jsonstr = json.dumps(judgeInputmessage)
        redisClient.lpush("judgelist", jsonstr)
        print("放入容器:", jsonstr)
        result = redisClient.brpop("result", 10)
        print(result)


def test_Postgrestrigger_nobefore():
    for i in range(0, times):
        judgedatabase = dict()
        judgedatabase['image_id'] = "judgedb:2.0"
        judgedatabase['database'] = "trigger_db"
        judgeInputs = list()
        file=open("../testJson/trigger_AC.json","r",encoding='utf-8')
        print(file)
        judgeInput=json.load(file)
        judgeInputs.append(judgeInput)
        judgeInputmessage = dict()
        judgeInputmessage['judgeInputs'] = judgeInputs
        judgeInputmessage['codeId'] = 18
        judgeInputmessage['problemId'] = 1
        judgeInputmessage["userId"] = 1
        judgeInputmessage["dialect"] = "pgsql"
        jsonstr = json.dumps(judgeInputmessage)
        redisClient.lpush("judgelist", jsonstr)
        print("放入容器:", jsonstr)
        result = redisClient.brpop("result", 5)
        print(result)


def test_MysqlSelect_nobefore():
    for i in range(0, times):
        judgedatabase = dict()
        judgedatabase['image_id'] = "judge-mysql:1.0"
        judgedatabase['database'] = "filmdb"
        judgeInputs = list()
        judgeInput = dict()
        additionalType = dict()
        additionalType['type'] = 'select'
        judgeInput['JudgeDatabase'] = judgedatabase
        judgeInput[
            'userInput'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInput['timeLimit'] = 10000
        judgeInput['additionFields'] = additionalType
        judgeInput[
            'standardAnswer'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInputs.append(judgeInput)
        judgeInputmessage = dict()
        judgeInputmessage['judgeInputs'] = judgeInputs
        judgeInputmessage['codeId'] = 18
        judgeInputmessage['problemId'] = 1
        judgeInputmessage["userId"] = 1
        judgeInputmessage["dialect"] = "mysql"
        jsonstr = json.dumps(judgeInputmessage)
        redisClient.lpush("judgelist", jsonstr)
        print("放入容器:", jsonstr)
        result = redisClient.brpop("result", 10)
        print(result)


def test_PostgresSelect_drop_table():
    for i in range(0, times):
        judgedatabase = dict()
        judgedatabase['image_id'] = "judgedb:2.0"
        judgedatabase['database'] = "testJson"
        judgeInputs = list()
        judgeInput = dict()
        additionalType = dict()
        additionalType['type'] = 'select'
        judgeInput['JudgeDatabase'] = judgedatabase
        judgeInput['userInput'] = "drop table movies"
        judgeInput['timeLimit'] = 10000
        judgeInput['additionFields'] = additionalType
        judgeInput[
            'standardAnswer'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInputs.append(judgeInput)
        judgeInputmessage = dict()
        judgeInputmessage['judgeInputs'] = judgeInputs
        judgeInputmessage['codeId'] = 18
        judgeInputmessage['problemId'] = 1
        judgeInputmessage["userId"] = 1
        judgeInputmessage["dialect"] = "pgsql"
        jsonstr = json.dumps(judgeInputmessage)
        redisClient.lpush("judgelist", jsonstr)
        print("放入容器:", jsonstr)
        result = redisClient.brpop("result", 10)
        print(result)


def test_sqliteSelect_drop_table():
    for i in range(0, times):
        judgedatabase = dict()
        judgedatabase['image_id'] = "judgedb:2.0"
        judgedatabase['database'] = "sqlite"
        judgeInputs = list()
        judgeInput = dict()
        additionalType = dict()
        additionalType['type'] = 'select'
        judgeInput['JudgeDatabase'] = judgedatabase
        judgeInput['userInput'] = "drop table movies"
        judgeInput['timeLimit'] = 10000
        judgeInput['additionFields'] = additionalType
        judgeInput[
            'standardAnswer'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInputs.append(judgeInput)
        judgeInputmessage = dict()
        judgeInputmessage['judgeInputs'] = judgeInputs
        judgeInputmessage['codeId'] = 18
        judgeInputmessage['problemId'] = 1
        judgeInputmessage["userId"] = 1
        judgeInputmessage["dialect"] = "sqlite"
        jsonstr = json.dumps(judgeInputmessage)
        redisClient.lpush("judgelist", jsonstr)
        print("放入容器:", jsonstr)
        result = redisClient.brpop("result", 10)
        print(result)


def test_MysqlSelect_drop_table():
    for i in range(0, times):
        judgedatabase = dict()
        judgedatabase['image_id'] = "judge-mysql:1.0"
        judgedatabase['database'] = "filmdb"
        judgeInputs = list()
        judgeInput = dict()
        additionalType = dict()
        additionalType['type'] = 'select'
        judgeInput['JudgeDatabase'] = judgedatabase
        judgeInput['userInput'] = "drop table movies"
        judgeInput['timeLimit'] = 10000
        judgeInput['additionFields'] = additionalType
        judgeInput[
            'standardAnswer'] = "SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'"
        judgeInputs.append(judgeInput)
        judgeInputmessage = dict()
        judgeInputmessage['judgeInputs'] = judgeInputs
        judgeInputmessage['codeId'] = 18
        judgeInputmessage['problemId'] = 1
        judgeInputmessage["userId"] = 1
        judgeInputmessage["dialect"] = "mysql"
        jsonstr = json.dumps(judgeInputmessage)
        redisClient.lpush("judgelist", jsonstr)
        print("放入容器:", jsonstr)
        result = redisClient.brpop("result", 10)
        print(result)


def getMessage():
    list = redisClient.lrange("judgelist", 0, -1)
    for item in list:
        print(item)
        print()
# if __name__=='__main__':
#     unittest.main()
