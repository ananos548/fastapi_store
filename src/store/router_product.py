from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, orm, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from store.models import Product, Category
from store.schemas import ProductSchema

router = APIRouter(
    tags=['Product']
)


@router.post('product/add_product')
async def add_product(new_product: ProductSchema, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Product).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get('/products')
async def get_products(session: AsyncSession = Depends(get_async_session)):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


@router.get('/{category_name}/products')
async def get_products_by_category(category_name: str,
                                   session: AsyncSession = Depends(get_async_session)):
    query = select(Product).join(Category).where(Category.title == category_name)
    result = await session.execute(query)
    return result.scalars().all()
