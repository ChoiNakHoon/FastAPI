

class CDbSession:
    __host = None
    __port = None
    __user = None
    __passwd = None
    __db_name = None
    __conn = None
    
    def __init__(self, host, port, user, passwd, db_name):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__db_name = db_name
    
    # DB 연결
    def Connect(self):
        try:
            import pymysql
            if self.__conn == None or not self.__conn.open:
                self.__conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__passwd, db=self.__db_name, charset="utf8")
            
            return self.__conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            print(e)
            
        return None
    
    # DB 실행
    def Execute(self, query):
        # listrowid db_cursor를 이용해 excute한 
        lastrowid = 0
        try:
            curs = self.Connect()
            curs.execute(query)
            self.__conn.commit()
            lastrowid = curs.lastrowid
            curs.close()
            self.__conn.close()
        except Exception as e:
            print(e)
        return lastrowid
    
    # DB 실행 결과
    def ExecuteResult(self, query):
        rows = []
        
        try:
            curs = self.Connect()
            curs.execute(query)
            rows = curs.fetchall()
            curs.close()
            self.__conn.close()
        except Exception as e:
            print(e)
        
        return rows
    
    # 프로시저 실행
    def ExecuteProcedure(self, proc, parameters = ()):
        rows = []
        
        try:
            param = str(parameters)
            param = param.replace(",)", ")")
            
            if param.find('(') == -1 and len(param) != 0:
                if param.isnumeric():
                    param = f"({param})"
                else:
                    param = f"('{param}')"
                    
                curs = self.Connect()
                curs.execute(f"call {proc}{param}")
                self.__conn.commit()
                rows = curs.fetchall()
                curs.close()
                self.__conn.close()
        except Exception as e:
            print(e)
            
        return rows
    
    
    
    
        