
class JudgeInput:
    def __init__(self,JudgeDatabase='',
                 userName='testJson',
                 passWord='abc123',
                 beforeInput='',
                 userInput='',
                 afterInput='',
                 spaceLimit=256,
                standardAnswer=None,
                 timeLimit=2000,
                 additionFields=None
                 ):
        self.JudgeDatabase=JudgeDatabase
        self.userName=userName
        self.passWord=passWord
        self.beforeInput=beforeInput
        self.userInput=userInput
        self.afterInput=afterInput
        self.standardAnswer=standardAnswer
        self.timeLimit=timeLimit
        self.additionFields=additionFields

def test_fun():
    with open('testJson/select_problem1_point1_AC.json', 'r') as f:
        data = json.load(f)
        print(data)
        conn = psycopg2.connect(database="testJson", user="testJson", password="abc123", host="10.20.87.51",
                                port="12001")
        cur = conn.cursor()
        # cur.execute(judge_select%(test2,test3))
        try:
            cur.execute(judge_select % (test1, test2))
            result = cur.fetchone()
            print(result[0])
        except Exception as err:
            print(type(err))
            print(err)
        finally:
            print('ok')
    # def __init__(self,a):
    #     pass