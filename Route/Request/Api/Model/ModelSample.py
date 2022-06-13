from tkinter.messagebox import NO
from pydantic import BaseModel
from typing import Optional
from fastapi import Query

from . import Data

class ModelSample(BaseModel):
    name: Optional[str] = Query(
        None,
        title="이름",
        description="당신의 이름"
    )
    info: Optional[Data.DataSample] = Query(
        None,
        title="개인정보",
        description="유저 개인 정보 입력하세요"
    )