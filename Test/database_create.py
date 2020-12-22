import docker
import psycopg2
from time import sleep

json="{'judgeDatabaseUrl':'jdbc:postgresql://localhost:5432/testJson','userName': 'testJson','passWord': 'abc123','userInput': 'SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'','standardAnswer': 'SELECT title, country, year_released FROM movies WHERE country <>'us' AND year_released = 1991 AND title LIKE 'The%'','timeLimit': 2000}"
if __name__=='__main__':


    client=docker.DockerClient(base_url='tcp://10.20.87.51:2375',version='auto',tls=False)


    env={"POSTGRES_PASSWORD":"abc123"}
    while 1:
        for i in range(12000,12010):
            try:
                portbinding = {"5432/tcp": i}
                container=client.containers.run("judgedb:2.0",command="docker-entrypoint.sh testJson",remove=True,ports=portbinding,detach=True,environment=env)
                print(i,"端口创建容器成功")
                # conn=psycopg2.connect(database="testJson",user="testJson",password="abc123",host="10.20.87.51",port="12011")
                # cur=conn.cursor()
                # cur.execute("select * from movies limit 10")
                # result=cur.fetchall()
                # print(result)
                # container.stop()
            except:
                pass
                #print('%d端口创建容器失败'%(i))
        sleep(2)

def containerRefresh():
    client=docker.DockerClient(base_url='tcp://10.20.87.51:2375',version='auto',tls=False)
    env={"POSTGRES_PASSWORD":"abc123"}
    while 1:
        for i in range(12000,12010):
            try:
                portbinding = {"5432/tcp": i}
                container=client.containers.run("judgedb:1.1",command="docker-entrypoint.sh testJson",remove=True,ports=portbinding,detach=True,environment=env)
                print(i,"端口创建容器成功")
            except:
                pass
                #print('%d端口创建容器失败'%(i))
        sleep(2)
