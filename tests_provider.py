import unittest
from provider import CbrClient

class TestCbrClient(unittest.TestCase):

    def test_invalid_id_returns_none(self):
        """Проверяем, что при неправильном ID возвращается None."""
        client = CbrClient(['R9999'], delay=0)
        result = client.get_currencies()
        self.assertEqual(result, [{'R9999': None}])

    def test_valid_id_gbp_returns_data(self):
        """Проверяем корректный ID (GBP): название и диапазон значений."""
        client = CbrClient(['R01035'], delay=0)
        result = client.get_currencies()

        self.assertEqual(len(result), 1)
        self.assertIn('GBP', result[0])

        name, value_tuple = result[0]['GBP']
        self.assertEqual(name, "Фунт стерлингов")

        full_value = float(f"{value_tuple[0]}.{value_tuple[1]}")
        self.assertTrue(0 < full_value < 999)

if __name__ == '__main__':
    unittest.main()