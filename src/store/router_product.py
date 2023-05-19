from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, or_
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


@router.get('/product/{id}')
async def product_detail(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).where(Product.id == id)
    result = await session.execute(query)
    return result.scalars().all()


@router.get('/search')
async def search(query: str, session: AsyncSession = Depends(get_async_session)):
    query_search = select(Product).filter(or_(Product.name.contains(query), Product.description.contains(query)))
    print(query_search)
    result = await session.execute(query_search)
    return result.scalars().all()
