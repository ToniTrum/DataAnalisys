import streamlit as st

from src.Models.UserModel import UserModel
from src.Controllers.AuthController import AuthController
from src.Views.AuthPage.AuthPage import AuthPage
from src.Views.ChatPage.ChatPage import ChatPage

class PageManager:
    def __init__(self) -> None:
        if "user_model" not in st.session_state:
            st.session_state.user_model = UserModel()
        
        if "auth_controller" not in st.session_state:
            st.session_state.auth_controller = AuthController(st.session_state.user_model)
            
        self.auth_controller = st.session_state.auth_controller

    def render(self) -> None:
        if not st.session_state.get("is_logged_in"):
            if self.auth_controller.check_auto_login():
                st.rerun()

        if st.session_state.get("is_logged_in"):
            ChatPage(self.auth_controller)
        else:
            AuthPage(self.auth_controller)