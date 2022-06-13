from unittest import result
from Singleton import CSingleton

class CRouteDispatcher(CSingleton):
    __app = None
    __responses = dict()
    __fast_api_requests = list()
    __fast_api_websockets = list()
    __jwt_secret = ""
    __hash_code = ""
    
    # 설정을 합니다.
    def initAppConfig(self, app, config):
        self.__app = app
        
        # Response시작
        self.initResponse(config=config)
        # FastApiRequests 시작
        self.initFastApiRequests()
        
    def initResponse(self, config = None):
        
        # 초기화
        self.__responses = {} 
        
        if config != None:
            
            # config에서 error data를 가져옴
            error_config = config["error"]
            
            for error in error_config:
                error_dict = dict()
                content_dict = dict()
                example_dict = dict()
                
                # error에서 "code" 가져옵니다
                result_code = error["code"] 
                
                error_dict["description"] = error["description"]
                
                # response라면
                if "response" in error: 
                    # example dict의 example에 error response 값을 저장합니다.
                    example_dict["example"] = error["response"]
                    
                content_dict["application/json"] = example_dict
                error_dict["content"] = content_dict
                
                # __response에 result_code를 key로 두고 error_dict을 value로 저장합니다.
                self.__responses[result_code] = error_dict
            
            # config에 jwt_secret이 있다면 __jwt_secret에 저장합니다.
            if "jwt_secret" in config:
                self.__jwt_secret = config["jwt_secret"]
                
            # config에 hash_code가 있다면 __hash_code에 저장합니다.
            if "hash_code" in config:
                self.__hash_code = config["hash_code"]
                
    def initFastAPIRequests(self):
        from Route.Request import Api