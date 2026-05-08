import streamlit as st

from Controllers import AuthController


def LoginButton(email: str, password: str, auth_controller: AuthController) -> None:
    button = st.button("Войти")

    if button:
        auth_controller.login(email, password)