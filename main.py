from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from db import engine
from models.base import Base
from routers.memo import router as memo_router
from routers.user import router as user_router


#회원 가입시 비밀번호를 암호화 시키기 위새 필요한 것
#passlib bcrypt==3.2.2
# 세션처리 itsdangerous

#pip install itsdangerous passlib bcrypt==3.2.2

#시킴스는 해시알고리즘을 지정함
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware

#프로그램이 시작하기 전과 후에 실행할 것들을 지정하는 lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield #프로그래밍 실행되는 구간
    await engine.dispose()
    
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

#*********************************라우터 include를 시키는 구간*************

app.include_router(memo_router)
app.include_router(user_router)





#비밀번호가 암호화가 되는 지 확인만 했다. 
'''
@app.get("/test")
def test_pwd(pwd: str):
    test_pwd = hash_password(pwd)
    return {"pwd": test_pwd}
'''