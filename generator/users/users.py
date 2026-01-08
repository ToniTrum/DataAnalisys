import random
import string

class User:
    def __init__(self, login: str, email: str, age: int):
        self.login = login
        self.email = email
        self.age = age

    def __str__(self):
        return f"Login: {self.login}\nEmail: {self.email}\nAge: {self.age}"
    
    def __repr__(self):
        return f"Login: {self.login}\nEmail: {self.email}\nAge: {self.age}"

def _generate_random_login(min_length: int = 5, max_length: int = 100) -> str:
    ALLOWED_CHARS = string.ascii_lowercase + string.digits + "_"
    length = random.randint(min_length, max_length)

    return "".join(random.choice(ALLOWED_CHARS) for _ in range(length))

def _generate_random_email(name: str) -> str:
    EMAIL_DOMAINS = [
        "gmail.com", "yandex.ru", "mail.ru", "outlook.com"
    ]
    domain = random.choice(EMAIL_DOMAINS)

    return f"{name}@{domain}"

def _generate_random_age() -> int:
    return random.randint(1, 150)

def generate_random_user():
    login = _generate_random_login()
    email = _generate_random_email(login)
    age = _generate_random_age()

    return User(login, email, age)

if __name__ == '__main__':
    print(generate_random_user())