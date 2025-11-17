from liquid import render

from liquid import Environment
from liquid.extra import BlockTag
from liquid.extra import ExtendsTag

from storefront.loaders import PathLoader
from storefront.models import Product, Store, Category

from storefront.serving.serving import StorefrontApp


env = Environment(loader=PathLoader("examples"))
env.add_tag(BlockTag)
env.add_tag(ExtendsTag)


def main():
    categories = [
        Category(id="1", name="Fruits", handle="fruits"),
        Category(id="2", name="Bakery", handle="bakery"),
        Category(id="3", name="Seafood", handle="seafood"),
        Category(id="4", name="Pantry", handle="pantry"),
        Category(id="5", name="Vegetables", handle="vegetables"),
        Category(id="6", name="Coffee", handle="coffee"),
        Category(id="7", name="Dairy", handle="dairy"),
    ]
    products = [
        Product(
            id="1",
            name="Organic Avocados",
            description="A bag of 4 ripe avocados",
            price=5.99,
            image_url="https://picsum.photos/800/600",
            category="fruits",
        ),
        Product(
            id="2",
            name="Artisanal Sourdough Bread",
            description="A loaf of freshly baked sourdough bread",
            price=7.50,
            image_url="https://picsum.photos/800/600",
            category="bakery",
        ),
        Product(
            id="3",
            name="Fresh Wild Salmon",
            description="A 1lb fillet of wild-caught salmon",
            price=22.00,
            image_url="https://picsum.photos/800/600",
            category="seafood",
        ),
        Product(
            id="4",
            name="Gourmet Olive Oil",
            description="A 500ml bottle of extra virgin olive oil",
            price=15.00,
            image_url="https://picsum.photos/800/600",
            category="pantry",
        ),
        Product(
            id="5",
            name="Heirloom Tomatoes",
            description="A pint of colorful heirloom tomatoes",
            price=6.00,
            image_url="https://picsum.photos/800/600",
            category="vegetables",
        ),
        Product(
            id="6",
            name="Craft Coffee Beans",
            description="A 12oz bag of single-origin coffee beans",
            price=18.00,
            image_url="https://picsum.photos/800/600",
            category="coffee",
        ),
        Product(
            id="7",
            name="Free-Range Eggs",
            description="A dozen fresh free-range eggs",
            price=8.00,
            image_url="https://picsum.photos/800/600",
            category="dairy",
        ),
    ]

    store = Store(
        id="12",
        title="EverFresh",
        products=products,
        categories=categories,
        description="Example Storefront",
    )

    app = StorefrontApp("localhost:5000", store=store)

    app.start_server()


if __name__ == "__main__":
    main()
