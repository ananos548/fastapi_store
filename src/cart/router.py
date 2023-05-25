from fastapi import APIRouter, Depends
from fastapi import Request
from sqlalchemy import select, orm, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import join
from sqlalchemy.sql.operators import and_

from auth.models import User
from cart.models import Cart
from cart.schema import CartSchema
from database import get_async_session
from store.models import Product
from utils import current_user

router = APIRouter(
    tags=['Cart']
)


@router.post('/cart/add')
async def add_to_cart(cart: CartSchema, user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    existing_cart = await session.execute(
        select(Cart).where(and_(Cart.user_id == user.id, Cart.product_id == cart.product_id)))
    existing_cart = existing_cart.scalar_one_or_none()
    if existing_cart:
        existing_cart.quantity += cart.quantity
        await session.commit()
    else:
        stmt = insert(Cart).values(user_id=user.id, **cart.dict())
        await session.execute(stmt)
        await session.commit()

    return {"status": "success"}


@router.delete('/cart/{product_id}')
async def remove_from_cart(cart: CartSchema, user: User = Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)):
    delete_stmt = delete(Cart).where(and_(Cart.user_id == user.id, Cart.product_id == cart.product_id))

    existing_cart = await session.execute(
        select(Cart).where(and_(Cart.user_id == user.id, Cart.product_id == cart.product_id))
    )
    cart_scalar = existing_cart.scalar_one_or_none()

    if cart_scalar:
        current_quantity = cart_scalar.quantity
        if cart.quantity == 0:
            await session.execute(delete_stmt)
        if cart.quantity >= current_quantity:
            await session.execute(delete_stmt)
        else:
            update_stmt = update(Cart).where(and_(Cart.user_id == user.id, Cart.product_id == cart.product_id)).values(
                quantity=current_quantity - cart.quantity
            )
            await session.execute(update_stmt)

        await session.commit()
        return {"status": "success"}


@router.post('/cart/clear')
async def cart_clear(user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    delete_stmt = delete(Cart).where(Cart.user_id == user.id)
    print(delete_stmt)
    await session.execute(delete_stmt)
    await session.commit()
    return {"status": "success"}



@router.get('/cart/checkout')
async def checkout_cart(user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    # Получение продуктов в корзине
    query = select(Product, Product.price, Cart.id).select_from(
        join(Cart, Product)
    ).where(Cart.user_id == user.id)
    result = await session.execute(query)
    products = result.scalars().all()
    # Получение количества продуктов в корзине
    cart_quantity = await session.execute(select(Cart).where(Cart.user_id == user.id))
    carts = cart_quantity.scalars().all()
    # Формирование данных о продуктах
    product_data = []
    for product, cart in zip(products, carts):
        product_data.append({
            'product_id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': cart.quantity
        })
    # Вычисление общей стоимости
    total_price = sum(cart.quantity * product.price for cart, product in zip(carts, products))
    return {'product_data': product_data, 'total_price': total_price}
