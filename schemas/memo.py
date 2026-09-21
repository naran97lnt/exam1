from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

#메모 저장시 사용할 객체
class MemoCreate(BaseModel):
    title:str
    content: str
    
#메모 수정시 사용할 객체
class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
#메모 목록을 클라이언트에게 보랠 때 사용할 객체 
class MemoOut(BaseModel):
    idx: int
    title: str
    content: str
    create_at: datetime
    update_at: datetime
    
    #sqlalchemy ORM 모델 객체를 Pydantic모델로 자동 변화기 위한 설정
    model_config = ConfigDict(from_attributes=True)