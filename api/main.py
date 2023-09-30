from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from api.database import get_async_session
from api.models import *
from api.schemas import *

app = FastAPI(title="Restaurant API", description="Restaurant Api Presentation")
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["Home Page"], summary="Home Page link")
async def home_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(Category)
    query1 = select(Product)
    result = await session.execute(query)
    result1 = await session.execute(query1)
    return templates.TemplateResponse("index.html", {"request": request, "title": result.scalars().all(),
                                                     "prod": result1.scalars().all()})


async def get_category_or_404(idNumber: int, session: AsyncSession = Depends(get_async_session)) -> Category:
    select_query = (select(Category).options(selectinload(Category.products)).where(Category.id == idNumber))
    result = await session.execute(select_query)
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return category


async def get_product_or_404(idNumber: int, session: AsyncSession = Depends(get_async_session)) -> Product:
    select_query = (select(Product).where(Product.id == idNumber))
    result = await session.execute(select_query)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return product


@app.post("/category", tags=["Operations"], summary="Add Category", status_code=status.HTTP_201_CREATED)
async def add_category(category_create: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    category = Category(**category_create.model_dump())
    session.add(category)
    await session.commit()
    return category


@app.post("/product", tags=["Operations"], summary="Add Product", response_model=ProductCreate,
          status_code=status.HTTP_201_CREATED)
async def add_product(product_create: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    return product


@app.get("/categories", tags=["Operations"], summary="Show Categories", response_model=list[CategoryRead],
         status_code=status.HTTP_200_OK)
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    select_query = select(Category)
    result = await session.execute(select_query)
    return result.scalars().all()


@app.get("/products", tags=["Operations"], summary="Show Products", response_model=list[ProductRead],
         status_code=status.HTTP_200_OK)
async def get_products(session: AsyncSession = Depends(get_async_session)):
    select_query = select(Product)
    result = await session.execute(select_query)
    return result.scalars().all()


@app.delete("/categories/{id}", tags=["Operations"], summary="Delete Category", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category: Category = Depends(get_category_or_404),
                          session: AsyncSession = Depends(get_async_session)):
    await session.delete(category)
    await session.commit()


@app.delete("/products/{id}", tags=["Operations"], summary="Delete Product", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product: Product = Depends(get_product_or_404),
                         session: AsyncSession = Depends(get_async_session)):
    await session.delete(product)
    await session.commit()


@app.patch("/categories/{id}", tags=["Operations"], summary="Update Category", response_model=CategoryRead,
           status_code=status.HTTP_202_ACCEPTED)
async def update_category(category_update: CategoryPartialUpdate, category: Category = Depends(get_category_or_404),
                          session: AsyncSession = Depends(get_async_session)) -> Category:
    category_update_dict = category_update.model_dump(exclude_unset=True)
    for key, value in category_update_dict.items():
        setattr(category, key, value)
    session.add(category)
    await session.commit()
    return category


@app.patch("/products/{id}", tags=["Operations"], summary="Update Product", response_model=ProductRead,
           status_code=status.HTTP_202_ACCEPTED)
async def update_product(product_update: ProductPartialUpdate, product: Product = Depends(get_category_or_404),
                         session: AsyncSession = Depends(get_async_session)) -> Product:
    product_update_dict = product_update.model_dump(exclude_unset=True)
    for key, value in product_update_dict.items():
        setattr(product, key, value)
    session.add(product)
    await session.commit()
    return product


@app.post("/product/manual", tags=["Operations"], summary="Create Product Manually", response_model=ProductBase,
          status_code=status.HTTP_202_ACCEPTED)
async def update_product(title: str, content: str, price: float, category_id: int,
                         session: AsyncSession = Depends(get_async_session)) -> Product:
    product_base_dict = Product(title=title, content=content, price=price, category_id=category_id)
    session.add(product_base_dict)
    await session.commit()
    return product_base_dict


@app.post("/category/manual", tags=["Operations"], summary="Create Category Manually", response_model=CategoryBase,status_code=status.HTTP_202_ACCEPTED)
async def update_category(Title: Annotated[str,Query(description="Please Insert Value:")], session: AsyncSession = Depends(get_async_session)) -> Category:
    category_base_dict = Category(title=Title)
    session.add(category_base_dict)
    await session.commit()
    return category_base_dict
