from storefront.models.base_class import LiquidDropModel


class Product(LiquidDropModel):
    id: str
    name: str
    description: str
    price: float
    image_url: str
    category: str

    # Custom properties (will also be automatically exposed)
    @property
    def formatted_price(self) -> str:
        """A custom property exposed to Liquid."""
        return f"${self.price:.2f}"

    @property
    def handle(self) -> str:
        """A URL-friendly handle for the product."""
        return self.name.lower().replace(" ", "-")
