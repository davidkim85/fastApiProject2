from sqlalchemy import Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    products: Mapped[list[Product]] = relationship("Product", cascade="all, delete")
