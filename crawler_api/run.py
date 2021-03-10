from crawler_api.core_models.root_object import RootObject
from crawler_api.create_app import get_app

app = get_app(RootObject()).run()
