from starlette.responses import JSONResponse
from fastapi import Header, HTTPException, Response, Request, status

class CBaseRequest:
    __path = None
    __method = None
    __request_model = None
    __response_model = None
    __response_class = None
    __description = None
    __tags = None
    __responses = None
    __files = None
    __name = None
    __jwt_secret = None
    __hash_code = None
    __is_depends = None
    
    _cookie = None
    
    
    def __init__(self, path, method="GET", name="request", request_model=None, response_model=None, response_class=JSONResponse, tags=[], description="", files=None, is_depends=False):
        self.__path = path
        self.__method = method
        self.__request_model = request_model
        self.__response_model = response_model
        self.__tags = tags
        self.__description = description
        self.__name = name
        self.__files = files
        self.__response_class = response_class
        self.__hash_code = ""
        self._cookie = dict()
        self.__responses = dict()
        self.__is_depends = is_depends
        
    def addResponse(self, status_code, modal, description=""):
        res = dict()
        res["model"] = modal
        res["description"] = description
        self.__responses[status_code] = res
        
    def initFastApi(self, app, responses={}, jwt_secret = "FastApiJwtSecret", hash_code=""):
        # app이 있다면
        if app != None:
            from typing import Optional
            from fastapi.responses import JSONResponse
            
            # responses가 있다면
            if len(self.__responses.keys()) != 0:
                # responses에 업데이트
                responses.update(self.__responses)
            
            self.__jwt_secret = jwt_secret
            self.__hash_code = hash_code
            
            # POST일때
            if self.__method == "POST":
                # 파일이 없을때
                if self.__files == None:
                    # request_model이 없을 때
                    if self.__request_model == None:
                        # router 시작
                        @app.post(self.__path, response_model=self.__response_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                        async def onPost(request: Request, response: Response):
                            return await self.OnRun(request=request, response=response)
                    else:
                        # depends가 있다면
                        if self.__is_depends:
                            from fastapi import Depends
                            @app.post(self.__path, response_model=self.__response_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                            async def OnPost(request: Request, response: Response, request_model:self.__request_model = Depends()):
                                return await self.OnRun(request=request, response=response, resquest_model=request_model)
                        else:
                            @app.post(self.__path, response_model=self.__response_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class )
                            async def OnPost(request_model:self.__request_model, request: Request, response: Response):
                                return await self.OnRun(request=request, response=response, request_model=request_model)
                else:
                    # 파일이 존재함
                    from typing import List
                    from fastapi import UploadFile
                    
                    if self.__request_model == None:
                        @app.post(self.__path, response_model=self.__response_model, tags=self.__tags, description=self.__description, name=self.__name, response_class=self.__response_class)
                        async def OnPost(request: Request, response: Response, files: List[UploadFile] = self.__files):
                            return await self.OnRun(request=request, response=response, files=files)
                    else:
                        if self.__is_depends:
                            from fastapi import Depends
                            @app.post(self.__path, response_model=self.__response_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                            async def OnPost(request: Request, response: Response, files: List[UploadFile] = self.__files, request_model:self.__request_model=Depends()):
                                return await self.OnRun(request=request, response=response, request_model=request_model, files=files)
                        else:
                            @app.post(self.__path, response_model=self.__response_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                            async def OnPost(request_model:self.__request_model, request: Request, response: Response, files: List[UploadFile] = self.__files):
                                return await self.OnRun(request=request, response=response, request_model=request_model, files=files)
            # GET일때
            elif self.__method == "GET":                
                if self.__files == None:
                    if self.__request_model == None:
                        @app.get(self.__path, response_model=self.__request_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                        async def OnGet(request: Request, response: Response, request_model:self.__request_model=Depends()):
                            return await self.OnRun(request=request, response=response, request_model=request_model)
                    else:
                        @app.get(self.__path, response_model=self.__request_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                        async def OnGet(request_model:self.__request_model, request: Request, response: Response):
                            return await self.OnRun(request=request, response=response, request_model=request_model)
                else:
                    from typing import List
                    from fastapi import UploadFile
                    
                    if self.__request_model == None:
                        @app.get(self.__path, response_model=self.__response_model, tag=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                        async def OnGet(request: Request, response: Response, files: List[UploadFile] = self.__files):
                            return await self.OnRun(request=request, response=response, files=files)
                        
                    else:
                        if self.__is_depends:
                            from fastapi import Depends
                            @app.get(self.__path, response_model=self.__request_model, tags=self.__tags, responses=responses, description=self.__description, name=self.__name, response_class=self.__response_class)
                            async def OnGet(request: Request, response: Response, files: List[UploadFile] = self.__files, request_model:self.__request_model=Depends()):
                                return await self.OnRun(request=request, response=response, request_model=request_model, files=files)
                        else:
                            @app.get(self.__path, response_model=self.__response_model, tags=self.__tags, response=response, description=self.__description, name=self.__name, response_class=self.__response_class)
                            async def OnGet(request: Request, response: Response, files: List[UploadFile] = self.__files, request_model:self.__request_model=Depends()):
                                return await self.OnRun(request=request, response=response, request_model=request_model, files=files)
                            
    async def OnRun(self, request:Request, response:Response, request_model = None, files = None):
        if self.__hash_code != None and len(self.__hash_code) != 0:
            if not "hash_code" in request.headers:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                hash_code = request.headers["hash_code"]
                
                if self.__hash_code != hash_code:
                    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
        import jwt
        
        self._cookie.clear()
        
        if "cookie" in request.cookies:
            cookie = request.cookies["cookie"]
            try:
                if len(cookie) != 0:
                    self._cookie = jwt.decode(cookie, self.__jwt_secret, algorithms="HS256")
            except Exception as e:
                self._cookie = dict()
                print(e)
                
                
        res = await self.Run(request=request, response=response, request_model=request_model, files=files)
        
        if len(self._cookie.keys()) != 0:
            str_cookie = jwt.encode(self._cookie, self.__jwt_secret, algorithm="HS256")
            response.set_cookie("cookie", str_cookie)
        else:
            response.delete_cookie(key="cookie")
        
        return res
    
    async def Run(self, request:Request, response:Response, resquest_mode = None, files = None):
        return ""