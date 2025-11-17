from typing import List

from pydantic import BaseModel

from storefront.models.product import Product


class CartItem(BaseModel):
    product: Product


class User(BaseModel):
    id: str
    name: str
    cart: List[CartItem]
