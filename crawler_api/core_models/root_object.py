from crawler_api.core_models.stocks_cache import StocksCacheService


class RootObject:

    def __init__(self):
        self.stocks_cache_service = StocksCacheService()