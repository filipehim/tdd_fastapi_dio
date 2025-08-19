from src.projeto_api_tdd.models.base import CreateBaseModel
from src.projeto_api_tdd.schemas.product import ProductIn


class ProductModel(ProductIn, CreateBaseModel):
    ...
