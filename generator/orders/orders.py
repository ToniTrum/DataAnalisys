import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import random
from datetime import datetime

from generator.cities import get_cities
from generator.products import get_products, Product
from generator.users import generate_random_user, User

class Order:
    def __init__(self, city: str, product: Product, user: User, quantity: int, created_at: datetime):
        self.city = city
        self.product = product
        self.user = user
        self.quantity = quantity
        self.created_at = created_at

    def __str__(self):
        return f"City: {self.city}; Product: {self.product}; User: {self.user}; Quantity: {self.quantity}; Created at: {self.created_at}"

    def __repr__(self):
        return f"City: {self.city}; Product: {self.product}; User: {self.user}; Quantity: {self.quantity}; Created at: {self.created_at}"
    
def generate_random_order() -> Order:
    city = random.choice(get_cities("city.csv"))
    product = random.choice(get_products())
    user = generate_random_user()
    quantity = random.randint(1, 10)
    created_at = datetime.now()

    return Order(city, product, user, quantity, created_at)

if __name__ == '__main__':
    print(generate_random_order())