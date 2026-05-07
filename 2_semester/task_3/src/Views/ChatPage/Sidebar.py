import streamlit as st

from src.Controllers.AuthController import AuthController

def Sidebar(auth_controller: AuthController) -> None:
    with st.sidebar:
        st.button("Выход", on_click=auth_controller.logout)

        st.title("Чаты:")
