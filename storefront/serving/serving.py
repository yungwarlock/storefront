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
    def __init__(self, host: str, store: Store) -> None:
        self.host, self.port = host.split(":")
        self.store = store.model_dump()

    def start_server(self):
        @Request.application
        def app(request: Request) -> Response:
            if not request.method == "GET":
                return Response("", 405)

            template_path = request.path

            try:
                template = env.get_template(template_path).render(store=self.store)
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
