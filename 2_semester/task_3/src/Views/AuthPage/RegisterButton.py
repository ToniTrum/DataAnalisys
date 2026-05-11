import streamlit as st

from Presenter import AuthPresenter


def RegisterButton(email: str, password: str, auth_presenter: AuthPresenter) -> None:
    button = st.button("Зарегистрироваться")

    if button:
        auth_presenter.register(email, password)