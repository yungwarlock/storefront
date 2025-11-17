import logging

from liquid import Environment
from liquid.extra import BlockTag
from liquid.extra import ExtendsTag

from werkzeug import Request, Response
from werkzeug.serving import make_server

from storefront.loaders import PathLoader
from storefront.models import Product, Store

logger = logging.getLogger(__name__)

PORT = 8000


env = Environment(loader=PathLoader("examples"))
env.add_tag(BlockTag)
env.add_tag(ExtendsTag)


class StorefrontApp:
    def __init__(self, host: str) -> None:
        self.host, self.port = host.split(":")

    def get_context(self):
        product = Product(
            id="12",
            price=102.4,
            name="Hello",
            description="Hello",
        )
        store = Store(
            id="12",
            title="EverFresh",
            description="Example Storefront",
        )

        return {
            "store": store,
            "products": [product],
        }

    def start_server(self):
        @Request.application
        def app(request: Request) -> Response:
            if not request.method == "GET":
                return Response("", 405)

            context = self.get_context()
            try:
                template = env.get_template(request.path).render(**context)
                return Response(
                    template,
                    200,
                    mimetype="text/html",
                )
            except Exception as e:
                print(e)
                return Response("", 404)

        server = make_server(
            self.host,
            int(self.port),
            app,
            threaded=True,
            processes=1,
        )

        server.serve_forever()
