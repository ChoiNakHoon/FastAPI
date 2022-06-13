from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class DataSample(BaseModel):
    phone: Optional[str] = Query(
        None,
        title="폰",
        description="폰번호 입력하세요."
    )
    age: Optional[int] = Query(
        None,
        title="나이",
        description="나이를 입력하세요!"
    )