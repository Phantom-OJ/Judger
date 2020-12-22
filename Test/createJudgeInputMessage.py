import redis
import json





if __name__ == '__main__':
    file=open("testJson//mysql//windowFunction_AC.json",mode="w")
    client = redis.Redis(host='10.20.87.51', port=6379, decode_responses=True)
    data=client.lindex("judgelist",0)
    judgeInput=json.loads(data)
    print(judgeInput,file=file)