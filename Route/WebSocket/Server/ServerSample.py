import asyncio
from Route.WebSocket.Base import CBaseWebSocket

class CServerSample(CBaseWebSocket):
    # 접속시 url 뒤에 jwt->get파라미터를 넣어야 함. cookie 연동 작업
    def __init(self):
        super().__init__(path="/server/sample")
    
    async def open(self, websocket, jwt_token):
        await super().open(websocket=websocket, jwt_token=jwt_token)
        
    async def close(self):
        await super().close()
        
    async def message(self, msg):
        await super().message(msg=msg)
        await self.send(msg)