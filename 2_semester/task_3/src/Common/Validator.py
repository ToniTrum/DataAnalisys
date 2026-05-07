import re

class Validator:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Валидация электронной почты

        :param email: электронная почта
        :type email: str

        :return: проходит ли валидацию
        :rtype: bool
        """

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Валидация пароля

        :param password: пароль
        :type password: str

        :return: проходит ли валидацию
        :rtype: bool
        """

        password_regex = r'^[a-zA-Z0-9_-]{8,}$'
        return bool(re.match(password_regex, password))