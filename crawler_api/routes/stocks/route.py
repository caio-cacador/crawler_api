from typing import Dict, List
from flask import Blueprint, jsonify, request, current_app
from crawler_api.routes.stocks.exception import BadRequest, CrawlerError
from crawler_api.routes.stocks.schema import get_stocks_schema
from crawler_api.crawler.crawler import CrawlerResult

stocks_blueprint = Blueprint(name='stocks', import_name='stocks')


def format_stocks_result(stocks: List[CrawlerResult]) -> Dict:
    formatted_info = {}
    for stock in stocks:
        formatted_info.update({
            stock.symbol: {
                'symbol': stock.symbol,
                'name': stock.name,
                'price': stock.price
            }
        })

    return formatted_info


@stocks_blueprint.route('/stocks', methods=['GET'])
def stocks():
    try:
        schema = get_stocks_schema(request.args)

        helper = current_app.config['helper']
        result = helper.stocks_cache_service.get_stocks(schema.region)

        return jsonify(format_stocks_result(result)), 200

    except(BadRequest, CrawlerError) as e:
        return jsonify(e.message), e.status_code
