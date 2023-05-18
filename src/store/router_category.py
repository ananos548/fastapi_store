from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from store.models import Category, Product
from store.schemas import CategorySchema

router = APIRouter(
    tags=['Category']
)


@router.post('/category/add_category')
async def add_category(new_category: CategorySchema, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Category).values(**new_category.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get('/categories')
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

