import streamlit as st

from Controllers import AuthController, ChatController


def RegisterButton(email: str, password: str, auth_controller: AuthController, chat_controller: ChatController) -> None:
    button = st.button("Зарегистрироваться")

    if button:
        result = auth_controller.register(email, password)
        if result:
            chat_controller.create_new_chat()