from decimal import Decimal
from typing import Optional
from pydantic import Field
from src.projeto_api_tdd.schemas.base import BaseSchemaMixin, OutSchema

class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase):
    ...

class ProductOut(ProductIn, OutSchema):
    ...

class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")

class ProductUpdateOut(ProductOut):
    ...
