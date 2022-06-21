from tkinter.tix import Tree


class CBaseWebSocket:
    __app = None
    __websocket = None
    
    __path = None
    __jwt_secret = None
    
    _client = dict()
    
    def __init__(self, path):
        self.__path = path
        
    def initFastApi(self, app, jwt_secret = "FastApiJwtSecret"):
        if app != None:
            self.__app = app
            self.__jwt_secret = jwt_secret
            
            
            from fastapi import WebSocket
            from fastapi.param_functions import Query
            
            @self.__app.websocket(self.__path)
            async def OnWebSocket(websocket: WebSocket, jwt: str = Query(...)):
                await websocket.accept()
                await self.open(websocket=websocket, jwt_token=jwt)
                while True:
                    try:
                        msg = await websocket.receive_text()
                        await self.message(msg)
                    except:
                        await self.close()
                        break
    
    def getClientDict(self):
        return self._client
    
    def isClientUser(self, user_idx):
        return False if self._client['user_idx'] != user_idx else True
    
    async def send(self, msg):
        await self.__websocket.send_text(msg)
    
    async def open(self, websocket, jwt_token):
        self.__websocket = websocket
        
        import jwt
        
        try:
            self._cookie = jwt.decode(jwt_token, self.__jwt_secret, algorithms="HS256")
        except Exception as e:
            self._cookie = dict()
            print(e)
            
    async def close(self):
        pass
    
    async def message(self, msg):
        pass
    
    
    