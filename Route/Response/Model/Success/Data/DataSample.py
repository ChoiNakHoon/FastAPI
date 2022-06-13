from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class DataSample(BaseModel):
    text: Optional[str] = Query(
        None,
        title="텍스트",
        description="문자열 넣기"
    )