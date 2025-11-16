from storefront.models.base_class import LiquidDropModel


class Store(LiquidDropModel):
    id: str
    title: str
    description: str
