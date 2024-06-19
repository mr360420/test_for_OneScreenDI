from datetime import datetime
import json
from decimal import Decimal
from functools import reduce

from pydantic import BaseModel, Field, Json, field_validator


class Service(BaseModel):
    name: str
    price: float


class Item(BaseModel):
    name: str
    sku: int


class Posting(BaseModel):
    delivery_schema: str
    order_date: datetime
    posting_number: str
    warehouse_id: int


class Operation(BaseModel):
    operation_id: int
    operation_type: str
    operation_date: datetime
    operation_type_name: str
    delivery_charge: int
    return_delivery_charge: int
    accruals_for_sale: float
    sale_commission: float
    amount: float
    type: str
    posting: Posting
    items: list[Item]
    services: list[Service]


class ClassForLoad(BaseModel):
    operation_id: int = Field(serialization_alias='operation_id')
    operation_date: datetime = Field(serialization_alias='operation_date')
    posting_number: str = Field(serialization_alias='posting_number')
    sku: Json = Field(serialization_alias='sku')
    # article: str = Field(serialization_alias='article')
    type_operation: str = Field(serialization_alias='type_operation')
    delivery_schema: str = Field(serialization_alias='delivery_schema ')
    name: str | None = Field(serialization_alias='name')
    price: Decimal | None = Field(serialization_alias='price')
    count_item: int = Field(serialization_alias='count_item')
    total_price: Decimal | None = Field(serialization_alias='total_price')
    quantity: int = Field(serialization_alias='quantity')

    @field_validator('sku', mode='before')
    @classmethod
    def create_json_of_items(cls, sku):
        future_json = [item.model_dump() for item in sku]
        return json.dumps(future_json)

    @field_validator('quantity', mode='before')
    @classmethod
    def create_quantity_of_items(cls, quantity):
        future = [item.model_dump() for item in quantity]
        result = [i.keys for i in future]
        return len(set(result))

    @field_validator('total_price', mode='before')
    @classmethod
    def create_total_price_of_service(cls, total_price):
        if not total_price:
            return None
        future_result = [service.price for service in total_price]
        return sum(future_result, 0)
