from pydantic import BaseModel
from typing import Optional, List
from fastapi import Query

from . import Data

class SuccessSample(BaseModel):
    result: Optional[int] = Query(
        None,
        title="결과 코드",
        description="성공했습니다."
    )
    data_list: Optional[List[Data.DataSample]] = Query(
        None,
        title="리스트",
        description="샘플 오브젝트"
    )