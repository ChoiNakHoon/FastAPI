from Route.Request.Api import Model
from Route.Response.Model import Success
from Route.Response.Model import Failed

from Route.Request.Base import CBaseRequest

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from typing import List

class CApiSample(CBaseRequest):
    def __init__(self):
        
        # 부모 클래스는 CBaseRequest
        # response_model일 경우 클라에서 전달해주는 api 구조는 json 구조이다
        # body에 넣어서 보내야 함
        # body말고 parameter로 보내고 싶을때는 is_depends=True를 뒤에 추가해주면 됨
        super().__init__(path="/api/sample", method="POST", name="Api Sample", request_model=Model.ModelSample, response_model=Success.SuccessSample,
                         tags=["샘플", "태그는 1개 이상 가능"], description=["API 샘플용이다."])
        
        self.addResponse(status.HTTP_400_BAD_REQUEST, Failed.FailedSample, "Sample Api가 실패했을 경우다. \n 에러 result code는 400번이다. 4xx 단위로 써라")
        
    async def Run(self, request:Request, response:Response, request_model:Model.ModelSample=None, files=None):
        # 쿠키 값을 넣어줄 수 있다. 클라가 cookie 데이터를 유지 해야 한다.
        self._cookie['key'] = 'value'
        
        # 문제 발생 조건일 경우. 아래와 같이 에러를 리턴
        if True: 
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Failed.FailedSample(result=1).dict())
        
        # DB 사용법
        if True:
            from Managed import CDBManager, CAwaS3BotoManager