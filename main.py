from liquid import render

from liquid import Environment
from liquid.extra import BlockTag
from liquid.extra import ExtendsTag

from storefront.models import Product, Store
from storefront.nextjs_loader import FileSystemLoader


env = Environment(loader=FileSystemLoader("examples"))
env.add_tag(BlockTag)
env.add_tag(ExtendsTag)


def main():
    product = Product(
        id="12",
        price=102.4,
        name="Hello",
        description="Hello",
    )
    store = Store(id="12", title="EverFresh", description="Example Storefront")

    print(render("Hello, {{ product.formatted_price }}!", product=product))
    print(env.get_template("index").render(product=product, store=store))
    print(
        env.get_template("categories/1/products/2").render(product=product, store=store)
    )


if __name__ == "__main__":
    main()
