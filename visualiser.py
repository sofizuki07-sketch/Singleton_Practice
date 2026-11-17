""" Модуль визуализации полученных с ЦБ данных """
import matplotlib.pyplot as plt
from typing import Any

class CurrenciesLst:
    """Класс для визуализации курсов валют, полученных от CbrClient."""

    def __init__(self, currencies_data: list[dict[str, Any]]) -> None:
        """
        Инициализация визуализатора.
        :param currencies_data: Список словарей с курсами валют, полученный от CbrClient.
        """
        self._currencies_data = currencies_data

    def visualize_currencies(self, save_path: str = 'currencies.jpg') -> None:
        """
        Строит столбчатую диаграмму курсов валют и сохраняет её в файл.
        :param save_path: Имя файла для сохранения графика (по умолчанию 'currencies.jpg').
        """
        codes = []
        rates = []

        # 1. Парсим данные из формата CbrClient
        for item in self._currencies_data:
            for code, info in item.items():
                # Пропускаем валюты, которые не были найдены (None)
                if info is None:
                    continue

                # info — это кортеж вида ('Имя', ('113', '2069')) или ('Имя', ('53', '0000'), 100)
                name = info[0]
                value_parts = info[1] # Берем целую и дробную часть

                # Склеиваем строки в число с плавающей точкой
                rate = float(f"{value_parts[0]}.{value_parts[1]}")

                codes.append(code)
                rates.append(rate)

        # Если вдруг данных вообще нет (например, все ID были неправильными)
        if not codes:
            print("Нет данных для отображения графика.")
            return

        # 2. Строим график (Bar Chart)
        fig, ax = plt.subplots(figsize=(10, 6)) # Задаем размер графика

        # Отрисовываем столбцы
        bars = ax.bar(codes, rates, color='skyblue', edgecolor='black')

        # 3. Настраиваем подписи и заголовок
        ax.set_ylabel('Курс (в рублях)', fontsize=12)
        ax.set_title('Курсы валют к рублю (по данным ЦБ РФ)', fontsize=14)
        ax.grid(axis='y', linestyle='--', alpha=0.7) # Сетка для красоты

        # Добавляем значения над каждым столбиком
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4), ha='center', va='bottom')

        # 4. Сохраняем график и закрываем его
        plt.savefig(save_path, format='jpg', dpi=300, bbox_inches='tight') # Сохраняем в jpg
        plt.close(fig) # Важно: закрываем фигуру, чтобы очистить память!

        print(f"График успешно сохранен в файл: {save_path}")