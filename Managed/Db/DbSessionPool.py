# DB Session
from queue import Queue

class CDbSessionPool:
    __host = None
    __port = None
    __user = None
    __passwd = None
    __db_name = None
    __max_size = None
    __pool = list()
    __queue = Queue()
    
    def __init__(self, host, port, user, passwd, db_name, max_size=5):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__db_name = db_name
        self.__max_size = max_size
        
    def Connection(self):
        try:
            from . import CDbSession
            while len(self.__pool) < self.__max_size:
                session = CDbSession(self.__host, self.__port, self.__user, self.__passwd, self.__db_name)
                self.__pool.append(session)
                self.__queue.put(session)
                
            return self.__queue.get()
        
        except Exception as e:
            print(e)
    
    def Insert(self, sql):
        lastrowid = 0
        session = self.Connection()
        try:
            session.Execute(sql)
        except Exception as e:
            print(e)
        finally:
            self.__queue.put(session)
        
        return lastrowid
    
    def Update(self, sql):
        session = self.Connection()
        try:
            session.Execute(sql)
        except Exception as e:
            print(e)
        finally:
            self.__queue.put(session)
    
    def Delete(self, sql):
        session = self.Connection()
        try:
            session.Execute(sql)
        except Exception as e:
            print(e)
        finally:
            self.__queue.put(session)
            
    def Select(self, sql):
        rows = []
        session = self.Connection()
        try:
            rows = session.ExecuteResult(sql)
        except Exception as e:
            print(e)
        finally:
            self.__queue.put(session)
            
    def CallProc(self, proc, parameters = ()):
        rows = None
        
        session = self.Connection()
        try:
            rows = session.ExecuteProcedure(proc, parameters)
        except Exception as e:
            print(e)
        finally:
            self.__queue.put(session)
            
        return rows
        