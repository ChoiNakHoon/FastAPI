from requests import session
from Singleton import CSingleton

# DB관리하는 매니저
class CDBManager(CSingleton):
    __session_pools = list()
    
    def loadConfig(self, configs):
        from .Db import CDbSessionPool
        # DB 설정 가져옴
        length = len(configs)
        
        for num in range(length):
            config = configs[num]
            
            session_dict = dict()
            keys = config.keys()
            
            for key in keys:
                db_info = config[key]
                
                db_write = db_info["write"]
                db_reads = None
                
                if "reads" in db_info:
                    db_reads = db_info["reads"]
                    
                db_session_pool = CDbSessionPool(
                        host=db_write["host"],
                        port=db_write["port"],
                        user=db_write["user"],
                        passwd=db_write["passwd"],
                        db_name=db_write["db_name"],
                        max_size=db_write["max_pool"]
                    )
                
                pool_dict = dict()
                pool_dict["write"] = db_session_pool
                
                if db_reads != None:
                    read_count = len(db_reads)
                    
                    read_pool_list = list()
                    
                    for read_num in range(read_count):
                        db_read = db_reads[read_num]
                        db_session_pool = CDbSessionPool(
                            host=db_read["host"],
                            port=db_read["port"],
                            user=db_read["user"],
                            passwd=db_read["passwd"],
                            db_name=db_read["db_name"],
                            max_size=db_read["max_pool"]   
                        )
                        read_pool_list.append(db_session_pool)
                    pool_dict["reads"] = read_pool_list
                    
                session_dict[key] = pool_dict
                
            self.__session_pools.append(session_dict)
    
    async def InsertPool(self, key, sql, num=0):
        if len(self.__session_pools) > num:
            session_pool = self.__session_pools[num]

            if key in session_pool:
                session = session_pool[key]
                db_pool = session["write"]
                return db_pool.Insert(sql)
            
        return -1
    
    async def UpdatePool(self, key, sql, num=0):
        if len(self.__session_pools) > num:
            session_pool = self.__session_pools[num]
            
            if key in session_pool:
                session = session_pool[key]
                db_pool = session["write"]
                db_pool.Update(sql)
                
    async def DeletePool(self, key, sql, num=0):
        if len(self.__session_pools) > num:
            session_pool = self.__session_pools[num]
            
            if key in session_pool:
                session = session_pool[key]
                db_pool = session["write"]
                db_pool.Delete(sql)
                
    async def SelectPool(self, key, sql, num=0):
        if len(self.__session_pools) > num:
            session_pool = self.__session_pools[num]
            
            if key in session_pool:
                session = session_pool[key]

                if "reads" in session:
                    session_reads = session["reads"]
                    reads_count = len(session_reads)
                    
                    if reads_count == 1:
                        db_pool = session_reads[0]
                    else:
                        import random
                        target = random.randrange(reads_count)
                        db_pool = session_reads[target]
                else:
                    db_pool = session["write"]
                
                return db_pool.Select(sql)
        
        return None
    
    async def CallProcPool(self, key, proc, parameters = (), num=0, read=False):
        if len(self.__session_pools) > num:
            session_pool = self.__session_pools[num]
            
            if key in session_pool:
                session = session_pool[key]
                db_pool = None
                
                if read:
                    if "reads" in session:
                        session_reads = session["reads"]
                        reads_count = len(session_reads)
                        
                        if reads_count == 1:
                            db_pool = session_reads[0]
                        else:
                            import random
                            target = random.randrange(reads_count)
                            db_pool = session_reads[target]
                else:
                    db_pool = session["write"]
                
                return db_pool.CallProc(proc=proc, parameters=parameters)
            
            return None