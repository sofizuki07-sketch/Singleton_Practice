""" Класс визуализации полученных с ЦБ данных """

class CurrenciesLst():

    def __init__(self):
        self.__cur_lst = [{
            'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')
        }, {
            'KZT': ('Казахстанских тенге', '19,8264')
        }, {
            'TRY': ('Турецких лир', '33,1224')
        }]

    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        currencies = []
        for el in self.__cur_lst:
            currencies.append(str(el.keys()))

        print(currencies)
        # fruits = ['apple', 'blueberry', 'cherry', 'orange']
        # counts = [40, 100, 30, 55]
        # bar_labels = ['red', 'blue', '_red', 'orange']
        # bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

        # ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        # ax.set_ylabel('fruit supply')
        # ax.set_title('Fruit supply by kind and color')
        # ax.legend(title='Fruit color')

        # plt.show()

        # обращается к атрибуту __cur_lst, преобразовывать значения курсов валют в нужный формат и выводить эти данные в файл

        # self.__cur_lst

