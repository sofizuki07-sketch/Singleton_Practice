import unittest
from unittest.mock import patch
from provider import CbrClient

# Фейковые данные (как будто мы уже скачали их с сайта)
FAKE_JSON = {
    "Valute": {
        "GBP": {"ID": "R01035", "Name": "Фунт стерлингов Соединенного королевства", "Nominal": 1, "Value": 113.2069},
    }
}


class TestCbrClient(unittest.TestCase):

    # Эта строчка заменяет реальный запрос в интернет на фейковый
    @patch('requests.get')
    def test_invalid_id_returns_none(self, mock_get):
        # Настраиваем фейковый ответ
        mock_get.return_value.json.return_value = FAKE_JSON

        client = CbrClient(['R9999'], delay=0)
        result = client.get_currencies()

        self.assertEqual(result, [{'R9999': None}])

    @patch('requests.get')
    def test_valid_id_gbp_returns_data(self, mock_get):
        mock_get.return_value.json.return_value = FAKE_JSON

        client = CbrClient(['R01035'], delay=0)
        result = client.get_currencies()

        self.assertEqual(len(result), 1)
        self.assertIn('GBP', result[0])

        name, value_tuple = result[0]['GBP']
        self.assertEqual(name, "Фунт стерлингов Соединенного королевства")

        full_value = float(f"{value_tuple[0]}.{value_tuple[1]}")
        self.assertTrue(0 < full_value < 999)


if __name__ == '__main__':
    unittest.main()