from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass #클래스를 정의하고 아무것도 구현하지 않으면 오류다. pass로 오류를 넘길 수 있다. 
