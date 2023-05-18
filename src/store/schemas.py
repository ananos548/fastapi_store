from pydantic.main import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_id: int

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    category_id: int
    title: str

    class Config:
        orm_mode = True
