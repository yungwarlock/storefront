from typing import List

from pydantic import BaseModel

from models.product import Product


class Collection(BaseModel):
    title: str
    description: str
    products: List[Product]
