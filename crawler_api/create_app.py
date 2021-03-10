from flask import Flask

from crawler_api.core_models.root_object import RootObject
from crawler_api.routes.stocks.route import stocks_blueprint


def get_app(helper: RootObject):

    app = Flask(__name__)
    app.config['helper'] = helper

    app.register_blueprint(stocks_blueprint)

    return app
