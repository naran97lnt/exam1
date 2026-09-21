from models.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    midx : Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    memail: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    mname: Mapped[str] = mapped_column(String(50))
    mpw: Mapped[str] = mapped_column(String(100))
    mstatus: Mapped[int] = mapped_column(Integer, default=0)