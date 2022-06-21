from Managed import AwsS3BotoManager
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
        from Managed import CDBManager, CAwsS3BotoManager
        
        config = None
        
        # config 파일 열기
        try:
            with open("config.json", "r", encoding="UTF-8") as f:
                text = f.read()
                
                import json
                config = json.loads(text)
                
                print(f"config file : {config}")
                
            # config 파일이 없다면
            if config == None:
                print("not found 'config.json'")
                exit(0)
        except:
            # config 파일 open 예외처리
            print("load error 'config.json' file")
            exit(0)
        
        # FastApi 실행
        self.loadFastApi(config["project"])
        
        # 클래스 선언
        self.__routeDispatcher = CRouteDispatcher.instance()
        self.__dbManager = CDBManager.instance()
        self.__awsS3BotoManager = CAwsS3BotoManager.instance()
        
        # 라우트 디스패처 시작
        self.__routeDispatcher.initAppConfig(self.__app, config=config)
        
        # DB 로드
        self.__dbManager.loadConfig(config["db"])
        # AWS S3 로드
        self.__awsS3BotoManager.loadConfig(config["s3"])
        
    
    def loadFastApi(self, config):
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
        
        self.__app = FastAPI(
            title=config["title"],
            version=config["version"],
            description=config["description"]
        )
        
    def getFastApiApp(self):
        return self.__app
    
    def getRouteDispatcher(self):
        return self.__routeDispatcher
    
    def getAwsS3BotoManager(self):
        return self.__awsS3BotoManager
    
    def getDBManager(self):
        return self.__dbManager
    