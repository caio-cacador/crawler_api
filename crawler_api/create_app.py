from flask import Flask

# from routes.main_route import health_blueprint
from crawler_api.core_models.root_object import RootObject
from routes.stocks.route import stocks_blueprint


def get_app(helper: RootObject):

    app = Flask(__name__)
    app.config['helper'] = helper

    # app.register_blueprint(health_blueprint)
    app.register_blueprint(stocks_blueprint)

    return app
