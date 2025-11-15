from liquid import render

from liquid import Environment
from liquid import FileSystemLoader

env = Environment(loader=FileSystemLoader("examples/"))


def main():
    print(render("Hello, {{ you }}!", you="World"))
    print(env.render("Hello, {{ you }}!", you="World"))
    print("Hello from storefront!")


if __name__ == "__main__":
    main()
