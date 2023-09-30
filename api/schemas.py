from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    title: str
    content: str
    price: float
    category_id: int

    class Config:
        from_attributes = True


class CategoryCreate(CategoryBase):
    pass


class ProductCreate(ProductBase):
    pass


class CategoryRead(CategoryBase):
    pass


class ProductRead(ProductBase):
    title: str
    content: str
    price: float


class CategoryPartialUpdate(BaseModel):
    title: str | None = None


class ProductPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    price: float | None = None
