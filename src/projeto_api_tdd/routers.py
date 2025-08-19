from fastapi import APIRouter
from src.projeto_api_tdd.controllers.product import router as product

api_router = APIRouter()
api_router.include_router(product, prefix="/products")
