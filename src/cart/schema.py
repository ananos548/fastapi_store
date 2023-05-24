import uuid

from pydantic.main import BaseModel


class CartSchema(BaseModel):
    # id: int
    product_id: int
    quantity: int
    # user_id: uuid.UUID

    class Config:
        orm_mode = True
