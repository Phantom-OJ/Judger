import traceback
import time
import docker

wait_time=2
dockerclient=docker.DockerClient(base_url='tcp://10.20.87.51:2375',version='auto',tls=False)
def getContainerAndConnection(databaseinfo:dict,driver):
    while (1):
        try:
            print(databaseinfo.get('image_id'))
            cl=dockerclient.containers.list(filters={"ancestor": databaseinfo.get('image_id')})
            containerSet = set(cl)
            container = containerSet.pop()
            port = container.ports[databaseinfo['port']][0]['HostPort']
            connection = driver.connect(database=databaseinfo['database'], user=databaseinfo['user'], password=databaseinfo['password'],
                                          host="10.20.87.51", port=int(port))
            print("使用容器：", (port, container, connection))
            return container,connection
        except Exception as e:
            traceback.print_exc()
            print(e)
            print("获取判题容器失败，等待%d秒" % (wait_time))
            time.sleep(wait_time)

container_set=set()

def containerRefresh():
    pgenv={"POSTGRES_PASSWORD":"abc123"}
    mysqlenv={"MYSQL_ROOT_PASSWORD":"abc123"}
    while 1:
        for i in range(12000,12015):
            try:
                portbinding = {"5432/tcp": i}
                container=dockerclient.containers.run("judgedb:2.0",command="postgres",remove=True,ports=portbinding,detach=True,environment=pgenv)
                print("端口%d创建容器成功"%i)
                #container_set.add((i,container,connection))
            except:
                pass
        for i in range(12015,12020):
            try:
                portbinding = {"3306/tcp": i}
                container = dockerclient.containers.run("judge-mysql:1.0", command="mysqld",
                                                        remove=True, ports=portbinding, detach=True,
                                                        environment=mysqlenv)
                print("端口%d创建容器成功" % i)
            except:
                pass