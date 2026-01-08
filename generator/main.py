import psycopg2
import random

from generator.categories import get_categories
from generator.cities import get_cities
from generator.products import get_products
from generator.users import generate_random_user
from generator.orders import generate_random_order

def _get_connection() -> psycopg2.extensions.connection:
    """
    Возвращает соединение к базе данных
    
    :return: Соединение к базе данных
    :rtype: connection
    """

    return psycopg2.connect(
        host="localhost",
        port=5000,
        dbname="shop",
        user="toni",
        password="1234"
    )

def create_tables() -> None:
    """
    Создает таблицы
    """

    with open('init.sql', 'r') as f:
        sql = f.read()

    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

def fill_table_cities() -> None:
    """
    Заполняет таблицу городами
    """

    conn = _get_connection()
    cur = conn.cursor()

    for city in get_cities("city.csv"):
        cur.execute(
            "INSERT INTO cities (name) VALUES (%s) ON CONFLICT DO NOTHING",
            (city,)
        )

    conn.commit()
    cur.close()
    conn.close()

def fill_table_categories() -> None:
    """
    Заполняет таблицу категориями
    """

    conn = _get_connection()
    cur = conn.cursor()

    for category in get_categories():
        cur.execute(
            "INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING",
            (category,)
        )

    conn.commit()
    cur.close()
    conn.close()

def fill_table_products() -> None:
    """
    Заполняет таблицу продуктами
    """

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM categories")
    category_map = {name: cid for cid, name in cur.fetchall()}

    for product in get_products():
        cur.execute("""
            INSERT INTO products (name, description, price, category_id)
            VALUES (%s, %s, %s, %s)
        """, (
            product.name,
            product.description,
            product.price,
            category_map[product.category]
        ))

    conn.commit()
    cur.close()
    conn.close()

def fill_table_users(count: int = 100) -> None:
    """
    Заполняет таблицу пользователями
    
    :param count: Количество пользователей
    :type count: int
    """

    conn = _get_connection()
    cur = conn.cursor()

    for _ in range(count):
        user = generate_random_user()
        cur.execute("""
            INSERT INTO users (login, email, age)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (user.login, user.email, user.age))

    conn.commit()
    cur.close()
    conn.close()

def fill_table_orders(count: int = 100) -> None:
    """
    Заполняет таблицу заказами
    """

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""SELECT id FROM users""")
    user_ids = [id for id, in cur.fetchall()]

    cur.execute("""SELECT id FROM products""")
    product_ids = [id for id, in cur.fetchall()]

    cur.execute("""SELECT id FROM cities""")
    city_ids = [id for id, in cur.fetchall()]

    for _ in range(count):
        order = generate_random_order(
            random.choice(city_ids),
            random.choice(product_ids),
            random.choice(user_ids)
        )
        cur.execute("""
            INSERT INTO orders (city_id, product_id, user_id, quantity, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            order.city_id,
            order.product_id,
            order.user_id,
            order.quantity,
            order.created_at
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    create_tables()

    fill_table_cities()
    fill_table_categories()
    fill_table_products()
    fill_table_users()
    fill_table_orders()