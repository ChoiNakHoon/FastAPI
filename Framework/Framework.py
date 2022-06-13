from Singleton import CSingleton

class CFramework(CSingleton):
    __app = None
    __routeDispatcher = None
    __awsS3BotoManager = None
    __dbManager = None
    __pushManager = None
    __redisManager = None
    
    def __init__(self):
        from Route import CRouteDispatcher