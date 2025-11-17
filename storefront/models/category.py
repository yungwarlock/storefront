from storefront.models.base_class import LiquidDropModel


class Category(LiquidDropModel):
    id: str
    name: str
    handle: str
