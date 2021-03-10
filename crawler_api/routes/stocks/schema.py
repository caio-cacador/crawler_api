from collections import namedtuple
from crawler_api.routes.stocks.exception import BadRequest

StocksSchema = namedtuple('StocksSchema', ['region'])


def get_stocks_schema(request_args) -> StocksSchema:
    region = request_args.get('region')
    if not region:
        raise BadRequest("O argumento 'region' é obrigatório.")

    return StocksSchema(region=region)
