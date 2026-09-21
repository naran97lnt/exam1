from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from models.base import Base

class Memo(Base):
    __tablename__ = "memo"
    
    idx : Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str]= mapped_column(String(2000))
    
    
    #글쓴 날짜
    create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    
    #수정날짜 -수정할 때 자동으로 갱신 
    update_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    #SQLAlchemy 2.0부터 타입 힌트 기반으로 Mapped[...] = mapped_column()형식을 표준처럼 사용함
    