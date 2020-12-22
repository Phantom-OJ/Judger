import pymysql
import paramiko
import sqlite3
import shutil
import os
import sys
def mysql_test():
    # 打开数据库连接
    db = pymysql.connect(host='10.20.87.51', port=13000,user='root',passwd="abc123", db="filmdb")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select * from movies limit 10")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()

    print(data)

    # 关闭数据库连接
    db.close()

def test_sqlite():

    conn = sqlite3.connect('filmdb.sqlite')
    print("Opened database successfully")
    cursor = conn.execute("SELECT * from movies limit 10")
    result=cursor.fetchall()
    print(result)



def test_ssh():
    ip='10.20.87.51'
    port=22
    password='qweasdzxc'
    name='maozunyao'
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=port, username=name, password=password)
    stdin, stdout, stderr = ssh.exec_command("sqlite3 /home/maozunyao/ooad/filmdb.sqlite  \"select * from movies limit 10\"")
    file=stdout.readlines()
    for row in file:
        print(row)
def copy(source,target):
    try:
        os.system("cp %s %s"%(source, target))
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

    # 远程ssh执行shell命令

if __name__=='__main__':
    copy("D:\\courseStation\\CS309\\python-docker\\filmdb.sqlite","D:\\courseStation\\CS309\\python-docker\\testJson")


