from storefront.models.base_class import LiquidDropModel
from storefront.models.product import Product
from storefront.models.collection import Collection
from storefront.models.category import Category


class Store(LiquidDropModel):
    id: str
    title: str
    description: str
    products: list[Product] = []
    collections: list[Collection] = []
    categories: list[Category] = []
