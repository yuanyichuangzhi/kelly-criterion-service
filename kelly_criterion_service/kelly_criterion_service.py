import logging
from functools import lru_cache
import pkg_resources

from flask import Flask, redirect, Response
from flasgger import Swagger

from .kelly_criterion_view import KellyCriterionView
from .config import SWAGGER_CONFIG


log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def tos():
    license = \
        pkg_resources.resource_string(__name__, '../LICENSE')
    return Response(license, mimetype='text/plain')


def create_endpoints(flask_app: Flask) -> None:
    log.info("Creating API Endpoints")
    flask_app.add_url_rule('/', 'index', lambda: redirect('apidocs'))

    flask_app.add_url_rule('/tos', 'tos', tos)

    flask_app.add_url_rule(
        '/v1/kelly_criterion',
        view_func=KellyCriterionView.as_view('kelly_criterion'),
        methods=['POST'])


def main() -> Flask:
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(process)d] [%(levelname)s] '
               '%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z')
    global log
    log = logging.getLogger('')
    log.info(f"Starting Kelly Criterion Service")

    flask_app = Flask(__name__)
    flask_app.config['SWAGGER'] = SWAGGER_CONFIG

    Swagger(flask_app)
    create_endpoints(flask_app)

    return flask_app


app = main()
