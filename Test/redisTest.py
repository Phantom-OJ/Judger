import redis
from time import sleep
import json



#学习redis的使用
def test1():
    judgeList=[i for i in range(1,11)]
    client=redis.Redis(host='10.20.87.51',port=6379,decode_responses=True)
    while(1):
        sleep(2)
        for i in judgeList:
            rt=client.sismember("judgeset",i)
            if(rt==1):
                print(i,"号已存在，跳过")
            else:
                rt=client.sadd("judgeset",i)
                if(rt==1):
                    print("成功添加",i,"到集合中")
                else:
                    print("添加失败",i,"到集合中")

def test2():
    client = redis.Redis(host='10.20.87.51', port=6379, decode_responses=True)
    list=client.lrange('judgelist',0,-1)
    judgelist=list[0]
   # judgelistInput=judgelist[0]
    #print(judgelistInput)
    s=json.loads(judgelist)
    print(s[2]['JudgeDatabase'])
    #print(s['JudgeDatabase'])


if __name__=='__main__':
    test2()




