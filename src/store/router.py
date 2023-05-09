from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, orm, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from store.models import Product, Category
from store.schemas import ProductSchema

router = APIRouter(
    prefix='/products',
    tags=['Store']
)


@router.post('/')
async def add_product(new_task: ProductSchema, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Product).values(**new_task.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get('/products')
async def get_products(session: AsyncSession = Depends(get_async_session)):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()
