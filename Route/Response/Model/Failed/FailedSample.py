from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class FailedSample(BaseModel):
    result: Optional[int] = Query(
        None,
        title="결과코드",
        description="실패했을 경우에 사용하는거다."
    )