from datetime import timedelta, datetime

from crawler_api.crawler.crawler import Crawler


class StocksCacheService:
    """
    Serviço responsável por gerenciar o cache de stocks por região
    """

    def __init__(self, minutes_to_expire: int = None, seconds_to_expire: int = None):
        self._stocks_cache = {}
        self._minutes_to_expire = minutes_to_expire if minutes_to_expire else 3
        self._seconds_to_expire = seconds_to_expire if seconds_to_expire else 13

    def get_stocks(self, region: str):

        if self._stocks_cache.get(region) and self._stocks_cache[region]['expire_in'] >= datetime.utcnow():
            stocks = self._stocks_cache[region]['stocks']
        else:
            crawler = Crawler()
            stocks = crawler.filter_stock_info(region)
            self._stocks_cache.update({
                region: {
                    'stocks': stocks,
                    'expire_in': datetime.utcnow() + timedelta(minutes=self._minutes_to_expire,
                                                               seconds=self._seconds_to_expire)
                }
            })

        return stocks
