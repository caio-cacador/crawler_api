import os
from collections import namedtuple
from time import sleep
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from crawler_api.routes.stocks.exception import BadRequest, CrawlerError

DRIVER_PATH = os.path.join(os.getcwd(), '../geckodriver')
CrawlerResult = namedtuple('CrawlerResult', ['symbol', 'name', 'price'])
CRAWLER_URL = 'https://finance.yahoo.com/screener/new'


class Crawler:

    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        self._table_build_filters_id = 'screener-criteria'
        self._remove_filter_id = '[data-test=\"remove-filter\"]'
        self._button_add_another_filter_xpath = '//span[text()=\"Add another filter\"]'
        self._filter_menu_css = '[data-test=\"filter-menu\"]'
        self._filter_region_xpath = "//span[text()='Region']"
        self._btn_close_filter_menu_xpath = "//span[text()='Close']"
        self._btn_filter_add = 'filterAdd'
        self._add_region = 'add region'
        self._dropdown_menu = 'dropdown-menu'
        self._select_region_xpath = '//span[text()=\"{}\"]'
        self._btn_stock_filter = '[data-test=\"find-stock\"]'
        self._btn_table_next_xpath = '//span[text()=\"Next\"]'
        self._result_table_id = 'scr-res-table'
        self._result_table_row = 'tr'
        self._column_symbol = "td[aria-label=\"Symbol\"]"
        self._column_name = "td[aria-label=\"Name\"]"
        self._column_price = "td[aria-label=\"Price (Intraday)\"]"
        self._show_limit_rows = '[data-test=\"showRows-select-selected\"]'
        self._show_100_rows = '//span[text()=\"Show 100 rows\"]'

        self._driver = Firefox(options=options, executable_path=DRIVER_PATH)
        self._driver.get(CRAWLER_URL)

    def _get_element_by(self, by: By, str_: str, element=None):
        element = element if element else self._driver
        return WebDriverWait(element, 30).until(EC.presence_of_element_located((by, str_)))

    def _wait_result_table_load(self):
        for i in range(5):
            try:
                result_table = self._get_element_by(by=By.ID, str_=self._result_table_id)
                result_rows = result_table.find_elements_by_tag_name(self._result_table_row)
                for row in result_rows[1:]:
                    self._get_element_by(by=By.CSS_SELECTOR, element=row, str_=self._column_price).text
                break
            except Exception:
                if i == 10:
                    raise Exception
                sleep(1)


    def _remove_all_filters(self, table_build_filters):
        # deleta todos os filtros
        filters_to_remove = table_build_filters.find_elements_by_css_selector(self._remove_filter_id)

        for filter_ in reversed(filters_to_remove):
            filter_.click()

        # abre menu de filtro
        self._get_element_by(by=By.XPATH, str_=self._button_add_another_filter_xpath,
                             element=table_build_filters).click()

    def _set_region_filter(self, filter_menu, table_build_filters, region: str):
        # escolhe o filtro da regiao
        self._get_element_by(by=By.XPATH, element=filter_menu, str_=self._filter_region_xpath).click()

        # fecha o menu de filtro
        self._get_element_by(by=By.XPATH, element=filter_menu, str_=self._btn_close_filter_menu_xpath).click()

        filters_options = table_build_filters.find_elements_by_class_name(self._btn_filter_add)
        for filter in filters_options:
            if self._add_region in filter.text.lower():
                # clica para adicionar um filtro de região
                filter.click()

                # menu de opções de filtro
                menu_options = self._get_element_by(by=By.ID, str_=self._dropdown_menu)

                # seleciona a regiao
                try:
                    self._get_element_by(by=By.XPATH, str_=self._select_region_xpath.format(region.capitalize()),
                                         element=menu_options).click()
                except TimeoutException:
                    self._driver.close()
                    raise BadRequest('A região requisitada não foi encontrada.')
                sleep(2)

    def _set_row_limit(self):
        # altera a tabela para exibir 100 linhas
        menu_show_rows = self._get_element_by(by=By.CSS_SELECTOR, str_=self._show_limit_rows)
        menu_show_rows.click()
        sleep(1)
        self._get_element_by(by=By.XPATH, str_=self._show_100_rows, element=menu_show_rows).click()

    def _get_button_next(self):
        span = self._get_element_by(by=By.XPATH, str_=self._btn_table_next_xpath)
        button = span.find_element_by_xpath("./../..")
        return button

    def filter_stock_info(self, region: str) -> List[CrawlerResult]:
        result = []
        try:
            # obtem a tabela de montar os filtros
            table_build_filters = self._get_element_by(by=By.ID, str_=self._table_build_filters_id)

            self._remove_all_filters(table_build_filters)

            # menu de filtro
            filter_menu = self._get_element_by(by=By.CSS_SELECTOR, str_=self._filter_menu_css, element=table_build_filters)

            self._set_region_filter(table_build_filters=table_build_filters, filter_menu=filter_menu, region=region)

            # realiza o filtro
            self._get_element_by(element=table_build_filters, by=By.CSS_SELECTOR, str_=self._btn_stock_filter).click()

            self._set_row_limit()

            while True:

                # pega as linhas das tabelas
                self._wait_result_table_load()
                result_table = self._get_element_by(by=By.ID, str_=self._result_table_id)

                if result_table:
                    result_rows = result_table.find_elements_by_tag_name(self._result_table_row)

                    # ignora a primeira linha que é o cabeçalho da tabela
                    for row in result_rows[1:]:

                        result.append(CrawlerResult(
                            symbol=self._get_element_by(by=By.CSS_SELECTOR, element=row, str_=self._column_symbol).text,
                            name=self._get_element_by(by=By.CSS_SELECTOR, element=row, str_=self._column_name).text,
                            price=self._get_element_by(by=By.CSS_SELECTOR, element=row, str_=self._column_price).text
                        ))

                if self._get_button_next().is_enabled():
                    self._get_button_next().click()
                    self._wait_result_table_load()
                else:
                    break

            self._driver.close()
            return result

        except BadRequest as e:
            raise e
        except Exception as e:
            self._driver.close()
            raise CrawlerError(e.description)
