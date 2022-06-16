from Singleton import CSingleton

# DB관리하는 매니저
class CDBManager(CSingleton):
    __session_pools = list()
    
    def loadConfig(self, configs):
        from .Db import CDbSessionPool 