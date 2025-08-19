from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from src.projeto_api_tdd.db.mongo import db_client
from src.projeto_api_tdd.models.product import ProductModel
from src.projeto_api_tdd.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from src.projeto_api_tdd.core.exceptions import NotFoundException
from bson import Decimal128, Binary
from bson.binary import STANDARD
from decimal import Decimal
import uuid
from bson import Decimal128, ObjectId, Binary
from decimal import Decimal
import uuid
from bson import Decimal128, ObjectId
from decimal import Decimal

# Funçoes ultilitarias
def normalize_bson(data: dict) -> dict:
    normalized = {}
    for key, value in data.items():
        if isinstance(value, Decimal128):
            normalized[key] = value.to_decimal()
        elif isinstance(value, ObjectId):
            normalized[key] = str(value)
        else:
            normalized[key] = value
    return normalized


def normalize_bson(data: dict) -> dict:
    normalized = {}
    for key, value in data.items():
        if isinstance(value, Decimal128):
            normalized[key] = value.to_decimal()
        elif isinstance(value, Binary):
            normalized[key] = value.as_uuid()
        elif isinstance(value, ObjectId):
            normalized[key] = str(value)
        else:
            normalized[key] = value
    return normalized

def convert_to_bson(data: dict) -> dict:
    bson_data = {}
    for key, value in data.items():
        if isinstance(value, Decimal):
            bson_data[key] = Decimal128(str(value))
        elif isinstance(value, uuid.UUID):
            bson_data[key] = Binary.from_uuid(value, uuid_representation=STANDARD)
        else:
            bson_data[key] = value
    return bson_data



class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")
        
    async def query(self) -> list[ProductOut]:
        results = await self.collection.find().to_list(length=None)
        return [ProductOut(**normalize_bson(doc)) for doc in results]

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        
        await self.collection.insert_one(product_model.to_mongo())

        return ProductOut(**product_model.model_dump())


    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f"Product not found with id: {id}")
        
        return ProductOut(**normalize_bson(result))



    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = convert_to_bson(body.model_dump(exclude_none=True))

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**normalize_bson(result))


    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
