from starlette.responses import JSONResponse
from fastapi import Header, HTTPException, Response, Request, status

class CBaseRequest:
    __path = None
    __method = None
    __request_model = None
    __response_model = None
    __description = None
    __tags = None
    __responses = None
    __files = None
    __name = None
    __jwt_secret = None
    __hash_code = None
    __is_depends = None
    
    _cookie = None