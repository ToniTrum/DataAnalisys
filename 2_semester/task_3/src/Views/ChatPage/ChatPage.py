import streamlit as st

from src.Controllers.AuthController import AuthController
from .Sidebar import Sidebar


def ChatPage(auth_controller: AuthController) -> None:
    Sidebar(auth_controller)
    st.title("Чат")