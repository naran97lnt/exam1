from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from models.memo import Memo
from schemas.memo import MemoCreate, MemoUpdate, MemoOut
from typing import List

#예). himedia.co.kr/memos/add, .../memos/total, .../memos/update
router = APIRouter(prefix="/memos", tags=["memos"])

@router.post("/add", response_model=MemoOut)
async def create_memo(payload: MemoCreate, db: AsyncSession = Depends(get_db)):
    memo = Memo(
        title=payload.title,
        content=payload.content
        
    )
    db.add(memo) #동기메서드
    await db.commit() #비동기메서드 I/O 이기 때문에 await필수
    await db.refresh(memo) #DB에서 idx와 create_at 등을 다시 읽음
    return memo

#목록보기 = 전체 보기 
@router.post("/list", response_model=List[MemoOut])
async def list_memo(db: AsyncSession = Depends(get_db)):
    #SqlAlchemy 2.0의 스타일
    stmt = select(Memo).order_by(Memo.idx)
    result = await db.execute(stmt)
    list = result.scalars().all()
    return list

#update = 수정 
@router.put("/edit", response_model=MemoOut)
async def edit_memo(idx: int, payload:MemoUpdate, db: AsyncSession = Depends(get_db)):
    #idx로 검색
    memo = await db.get(Memo, idx)
    #위의 memo가 있을 때만 수정기능을 수행해야 한다. 
    if memo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memo not found"
        )
    #컬럼 값 수정
    if payload.title is not None: # 인자로 넘어오는 title이 비어있지 않다면 
        memo.title = payload.title #ORM모델의 title을 인자값 title로 변경
    if payload.content is None:
        memo.content = payload.content
        
        
    await db.commit()
    await db.refresh(memo)
    return memo 

#삭제

@router.delete("/delete")
async def delete_memo(idx: int, db: AsyncSession = Depends(get_db)):
    #인자로 받은 idx로 먼저 검색하여 검새된 결과과 있으며 삭제 하며 된다. 
    memo = await db.get(Memo, idx)
    if memo is None:
        raise HTTPException(status_code=404, detail="Memo not foud")
    
    await db.delete(memo)
    await db.commit()
    return None
    
    