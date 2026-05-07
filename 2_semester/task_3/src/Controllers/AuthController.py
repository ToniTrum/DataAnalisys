import streamlit as st
import extra_streamlit_components as stx
from gotrue import Session, User
from datetime import datetime, timedelta

from src.Common.Validator import Validator
from src.Models.UserModel import UserModel


class AuthController:
    def __init__(self, user: UserModel) -> None:
        self.user = user
        self.cookie_manager = stx.CookieManager()

    def _set_session_state(self, user: User) -> None:
        st.session_state["is_logged_in"] = True
        st.session_state["user_id"] = user.id
        st.session_state["user_email"] = user.email

    def _save_session_cookies(self, session: Session) -> None:
        if session:
            self.cookie_manager.set(
                cookie="supabase-access-token", 
                val=session.access_token,
                expires_at=datetime.now() + timedelta(days=7),
                key="set_access"   
            )
            self.cookie_manager.set(
                cookie="supabase-refresh-token", 
                val=session.refresh_token,
                expires_at=datetime.now() + timedelta(days=7),
                key="set_refresh"
            )

    def login(self, email: str, password: str) -> None:
        if not email or not password:
            st.error("Введите электронную почту и пароль")
            return

        result = self.user.sign_in(email, password)

        if isinstance(result, Exception):
            st.error(f"Ошибка входа:\n{result}")
        elif result.session:
            self._save_session_cookies(result.session)
            self._set_session_state(result.user)

            st.success("Успешный вход!")

    def check_auto_login(self) -> bool:
        if st.session_state.get("is_logged_in"):
            return True
        
        cookies = self.cookie_manager.get_all()
        access_token = cookies.get("supabase-access-token")
        refresh_token = cookies.get("supabase-refresh-token")

        if access_token and refresh_token:
            result = self.user.set_session(access_token, refresh_token)
            if not isinstance(result, Exception) and result.user:
                self._set_session_state(result.user)
                return True
        
        return False

    def register(self, email: str, password: str) -> None:
        if not Validator.is_valid_email(email):
            st.error("Введите корректную электронную почту")
            return
        
        if not Validator.is_valid_password(password):
            st.error("Введите корректный пароль. Пароль должен состоять исключительно из латинских букв, арабских цифр, нижнего подчёркивания и тире, также он должен быть не менее 8 символов.")
            return

        result = self.user.sign_up(email, password)

        if isinstance(result, Exception):
            st.error(f"Ошибка регистрации:\n{result}")
        elif result.user:
            self._save_session_cookies(result.session)
            self._set_session_state(result.user)

            st.success("Регистрация успешна!")

    def logout(self) -> None:
        self.user.sign_out()

        self.cookie_manager.delete("supabase-access-token", key="delete_access")
        self.cookie_manager.delete("supabase-refresh-token", key="delete_refresh")

        st.session_state["is_logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["user_email"] = None

        st.rerun()
