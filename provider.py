""" Класс для скачивания и перевода в нужный формат данных из ЦБ """

import requests

class CbrClient:

    def __init__(self, currencies_ids_lst: list):
        self.cur_lst = currencies_ids_lst

    @property
    def cur_lst(self):
        return self._cur_lst

    @cur_lst.setter
    def cur_lst(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError("currencies_ids_lst должен быть списком!") from None
        if  not all(isinstance(item, str) for item in value):
            raise TypeError("ID валют в списке должны быть строками!") from None
        self._cur_lst = value

    def __del__(self):
        print(f"Объект {self.__class__.__name__} удален. Очистка памяти завершена.")
        self._cur_lst = None

    def get_currencies(self) -> list:
        """ Метод загрузки данных с ЦБ и приведения их в формат словаря из json"""


        """TODO 1(ответ): Вместо XML и перевода с помощью библиотек в json формат, используется !неофициальное!
        "зеркало" ЦБ, по ссылке которого через requests и .json() получается словарь данных о валютах и курсах.
        Официального JSON API у ЦБ нет.
        
        зеркало с JSON - https://www.cbr-xml-daily.ru/daily_json.js
        изначальная ссылка: https://www.cbr.ru/scripts/XML_daily.asp """

        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url, timeout=10)
        # timeout = гарантия либо ответа сайта,
        # либо продолжения программы без зависания на ожидании
        response.raise_for_status() # Проверка, что сайт не упал и ответил программе

        data = response.json()
        result = []
        # vvvv Формат изначальных данных vvvv
        # 'Valute': {'AUD': {'AUD': {'ID': 'R01010', 'NumCode': '036', ...
        # ... 'CharCode': 'AUD', 'Nominal': 1, 'Name': 'Австралийский доллар',
        # 'Value': 57.1567, 'Previous': 57.0503}, '':{}, '':{} ...  }
        valutes = data['Valute']
        for char_code, info in valutes.items():
            valute_id = info.get('ID')
            if valute_id in self.cur_lst:
                name = info.get('Name')
                value = info.get('Value')
                currency = {char_code: (name, str(value).replace('.', ','))}
                result.append(currency)

        return result

if __name__ == '__main__':
    # фунты стерлингов, тенге, турецкие лиры
    client = CbrClient(['R01035', 'R01335', 'R01700J'])
    print(client.get_currencies())