import random
from datetime import datetime, timedelta

class Order:
    def __init__(self, city_id: int, product_id: int, user_id: int, quantity: int, created_at: datetime):
        self.city_id = city_id
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.created_at = created_at

    def __str__(self):
        return f"City: {self.city_id}; Product: {self.product_id}; User: {self.user_id}; Quantity: {self.quantity}; Created at: {self.created_at}"

    def __repr__(self):
        return f"City: {self.city_id}; Product: {self.product_id}; User: {self.user_id}; Quantity: {self.quantity}; Created at: {self.created_at}"
    
def _generate_random_datetime(start: datetime, end: datetime) -> datetime:
    """
    Генерирует случайную дату
    
    :param start: Дата начала отчёта
    :type start: datetime
    :param end: Дата конца отчёта
    :type end: datetime
    :return: Случайная дата
    :rtype: datetime
    """

    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))

    return start + timedelta(seconds=random_seconds)

def _generate_random_quantity(max_quantity: int) -> int:
    """
    Генерирует случайное количество
    
    :param max_quantity: Максимальное количество
    :type max_quantity: int
    :return: Случайное количество
    :rtype: int
    """

    return random.randint(1, max_quantity)

def generate_random_order(city_id: int, product_id: int, user_id: int) -> Order:
    """
    Генерирует случайный заказ
    
    :param city_id: ID города
    :type city_id: int
    :param product_id: ID продукта
    :type product_id: int
    :param user_id: ID пользователя
    :type user_id: int
    :return: Случайный заказ
    :rtype: Order
    """

    quantity = _generate_random_quantity(10)
    created_at = _generate_random_datetime(datetime(2020, 12, 31), datetime.now())

    return Order(city_id, product_id, user_id, quantity, created_at)

if __name__ == '__main__':
    print(generate_random_order(1, 1, 1))