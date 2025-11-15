from models.base_class import LiquidDropModel


class Product(LiquidDropModel):
    id: str
    name: str
    description: str
    price: float

    # Custom properties (will also be automatically exposed)
    @property
    def formatted_price(self) -> str:
        """A custom property exposed to Liquid."""
        return f"${self.price:.2f}"

    @property
    def url(self) -> str:
        """Another example property."""
        return f"/products/{self.id}"
