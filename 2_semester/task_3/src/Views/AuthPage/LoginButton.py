import streamlit as st

from Presenter import AuthPresenter


def LoginButton(email: str, password: str, auth_presenter: AuthPresenter) -> None:
    button = st.button("Войти")

    if button:
        auth_presenter.login(email, password)