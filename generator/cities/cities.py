import csv
from pathlib import Path

def get_cities(cities_csv: str) -> list[str]:
    """
    Возвращает список городов России
    
    :param cities_csv: Название csv файла с городами
    :type cities_csv: str
    :return: Список городов России
    :rtype: list[str]
    """

    BASE_DIR = Path(__file__).resolve().parent

    with open(BASE_DIR / cities_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        cities = [city[9] for city in reader if city[9] != '']
        return cities
    
    return []

if __name__ == '__main__':
    print(get_cities('city.csv'))