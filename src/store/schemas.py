from pydantic.main import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int
    quantity: int
    category_id: int

    class Config:
        orm_mode = True
