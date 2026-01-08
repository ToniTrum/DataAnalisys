import random
import string

class User:
    def __init__(self, login: str, email: str, age: int):
        self.login = login
        self.email = email
        self.age = age

    def __str__(self):
        return f"Login: {self.login}; Email: {self.email}; Age: {self.age}"
    
    def __repr__(self):
        return f"Login: {self.login}; Email: {self.email}; Age: {self.age}"

def _generate_random_login(min_length: int = 5, max_length: int = 100) -> str:
    """
    Генерирует случайный логин
    
    :param min_length: Минимальная длина логина
    :type min_length: int
    :param max_length: Максимальная длина логина
    :type max_length: int
    :return: Случайный логин
    :rtype: str
    """

    ALLOWED_CHARS = string.ascii_lowercase + string.digits + "_"
    length = random.randint(min_length, max_length)

    return "".join(random.choice(ALLOWED_CHARS) for _ in range(length))

def _get_random_email(login: str) -> str:
    """
    Возвращает случайную почту
    
    :param name: Логин
    :type name: str
    :return: Случайная почта
    :rtype: str
    """

    EMAIL_DOMAINS = [
        "gmail.com", "yandex.ru", "mail.ru", "outlook.com"
    ]
    domain = random.choice(EMAIL_DOMAINS)

    return f"{login}@{domain}"

def _generate_random_age() -> int:
    """
    Генерирует случайный возраст
    
    :return: Случайный возраст
    :rtype: int
    """
    return random.randint(1, 150)

def generate_random_user() -> User:
    """
    Генерирует случайного пользователя
    
    :return: Случайный пользователь
    :rtype: User
    """

    login = _generate_random_login()
    email = _get_random_email(login)
    age = _generate_random_age()

    return User(login, email, age)

if __name__ == '__main__':
    print(generate_random_user())