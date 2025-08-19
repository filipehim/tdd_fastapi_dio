from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid

from bson import Decimal128, Binary
from bson.binary import STANDARD
from pydantic import BaseModel, Field

class CreateBaseModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def to_mongo(self) -> dict[str, Any]:
        """Converte os campos para tipos compatíveis com BSON (MongoDB)."""
        mongo_dict = self.dict()

        for key, value in mongo_dict.items():
            if isinstance(value, Decimal):
                mongo_dict[key] = Decimal128(str(value))
            elif isinstance(value, uuid.UUID):
                mongo_dict[key] = Binary.from_uuid(value, uuid_representation=STANDARD)

        return mongo_dict
