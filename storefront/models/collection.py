from typing import List

from pydantic import BaseModel

from storefront.models.product import Product


class Collection(BaseModel):
    title: str
    description: str
    products: List[Product]
