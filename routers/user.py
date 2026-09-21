from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
from passlib.context import CryptContext

from db import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserOut



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

 #비밀번호 암호화는 함수
def hash_password(pwd): #비밀번호 암호화는 함수 
    return pwd_context.hash(pwd) #인자로 받은 비밀번호가 해시처리가 되어 반환됨

#검증하는 함수
def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)


#예). himedia.co.kr/memos/add, .../memos/total, .../memos/update
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/add", response_model=UserOut)
async def create_memo(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_pwd = hash_password(payload.pwd)
    
    user = User(
       mname = payload.name,
       memail = payload.email,
       mpw = hashed_pwd
        
    )
    db.add(user) #동기메서드
    await db.commit() #비동기메서드 I/O 이기 때문에 await필수
    await db.refresh(user) #DB에서 idx와 create_at 등을 다시 읽음
    return user

@router.post("/login", response_model=UserOut)
async def login_user(request: Request, data: UserLogin, db: AsyncSession = Depends(get_db)):
    # 비밀번호는 암호화가 되어 있어서 비교할 수 없다. 그래서 먼저
    #이메일을 검색한다
    result = await db.execute(select(User).where(User.memail == data.memail))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="이메일 또는 비밀번호가 틀립니다.")
    
    #비밀번호 검증
    
    if not verify_password(data.mpw, user.mpw):
        raise HTTPException(status_code=404, detail="이메일 또는 비밀번호가 틀립니다.")
    
    #인증이 된 경우
    request.session['login_data'] = user.mname
    return user