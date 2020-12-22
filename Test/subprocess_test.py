import subprocess
#学习subprocess的使用
if __name__=="__main__":
    env={"PGPASSWORD":"abc123"}
    proc_args = ["D:\\program\\testJson\\12\\bin\\psql.exe","--host=localhost","--port=5432","--username=testJson","--command=select * from movies limit 5;select * from movies limit 10;"]
    proc = subprocess.Popen(proc_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print("out:",out.decode("GBK"))
    print("error:",err.decode("utf8"))
