import streamlit as st

from src.Controllers.AuthController import AuthController


def RegisterButton(email: str, password: str, auth_controller: AuthController) -> None:
    button = st.button("Зарегистрироваться")

    if button:
        auth_controller.register(email, password)