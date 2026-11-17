""" Класс для скачивания и перевода в нужный формат данных из ЦБ """
import requests
from decimal import Decimal
import time

from visualiser import CurrenciesLst # Импортируем наш визуализатор


class SingletonMeta(type):
    """Метакласс для реализации паттерна Одиночка."""

    _instances = {}  # Наш созданный объект

    def __call__(cls, *args, **kwargs):

        # 1. Проверка наличие объекта этого класса в словаре _instances...
        if cls not in cls._instances:
            # 2. ...то создаем его
            cls._instances[cls] = super().__call__(*args, **kwargs)

        # 3. Если объект уже существует (или мы только что его создали), возвращаем его
        return cls._instances[cls]

class CbrClient(metaclass=SingletonMeta):
    def __init__(self, currencies_ids_lst: list[str], delay: float = 1.0 ):
        self.cur_lst = currencies_ids_lst
        self.cache = None
        self._last_request_time = 0.0
        self._delay = delay


    @property
    def cur_lst(self) -> list[str]:
        return self._cur_lst

    @cur_lst.setter
    def cur_lst(self, value: list[str]) -> None:
        if not isinstance(value, list):
            raise TypeError("currencies_ids_lst должен быть списком!") from None
        if  not all(isinstance(item, str) for item in value):
            raise TypeError("ID валют в списке должны быть строками!") from None
        self._cur_lst = value

    @property
    def cache(self) -> list | None:
        return self._cache

    @cache.setter
    def cache(self, value: list | None) -> None:
        if value is not None:
            if not isinstance(value, list):
                raise TypeError("cache сохранён с ошибкой: попробуйте позже...") from None
            if not all(isinstance(item, dict) for item in value):
                raise TypeError("cache сохранён с ошибкой: попробуйте позже...") from None
        self._cache = value

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

        current_time = time.time()
        time_passed = current_time - self._last_request_time
        if time_passed < self._delay and self.cache is not None:
            print("Повторный запрос отменён. Вывод данных с прошлого сохранения: ")
            return self.cache

        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url, timeout=10)
        # timeout = гарантия либо ответа сайта,
        # либо продолжения программы без зависания на ожидании
        response.raise_for_status() # Проверка, что сайт не упал и ответил программе

        data = response.json()
        result = []

        # будем вычислять НЕнайденные ID, оставлять на доске позора
        shame_board = set(self.cur_lst)

        # vvvv Формат изначальных данных vvvv
        # 'Valute': {'AUD': {'AUD': {'ID': 'R01010', 'NumCode': '036', ...
        # ... 'CharCode': 'AUD', 'Nominal': 1, 'Name': 'Австралийский доллар',
        # 'Value': 57.1567, 'Previous': 57.0503}, '':{}, '':{} ...  }
        valutes = data['Valute']
        for char_code, info in valutes.items():
            valute_id = info.get('ID')
            if valute_id in self.cur_lst:
                # нашли=вычеркнули из списка позорников
                shame_board.discard(valute_id)

                name = info.get('Name')
                nominal = info.get('Nominal')

                value_decimal = Decimal(str(info.get('Value')))
                value_str = f"{value_decimal:.4f}"
                value = value_str.split(".")

                if nominal == 1:
                    currency = {char_code: (name, tuple(value) ) }
                else:
                    currency = {char_code: (name, tuple(value), nominal ) }
                result.append(currency)

        for _ in shame_board:
            result.append({'R9999': None})

        self.cache = result
        self._last_request_time = current_time
        return result

if __name__ == '__main__':
    
    print("--- Проверка паттерна Одиночка ---")
    client1 = CbrClient(['R01035'])
    client2 = CbrClient(['R01335'])  # Пытаемся создать второй объект с другими данными
    print(f"client1 is client2: {client1 is client2}")
    print(f"Данные в client2: {client2.cur_lst}")  # Выведет ['R01035']

    # Получаем данные основные (фунты, тенге, лиры)
    client = CbrClient(['R01035', 'R01335', 'R01700J'])
    data = client.get_currencies()

    visualizer = CurrenciesLst(data)  # Передаем данные визуализатору
    visualizer.visualize_currencies()  # Строим и сохраняем график