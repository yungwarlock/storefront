from liquid import render

from liquid import Environment

from models import Product, Store
from loader import FileSystemLoader


env = Environment(loader=FileSystemLoader("examples/"))


def main():
    product = Product(
        id="12",
        name="Hello",
        description="Hello",
        price=102.4,
    )
    store = Store(id="12", title="EverFresh", description="Example Storefront")

    print(render("Hello, {{ product.formatted_price }}!", product=product))
    print(env.get_template("index").render(product=product, store=store))


if __name__ == "__main__":
    main()
