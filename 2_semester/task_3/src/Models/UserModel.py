import streamlit as st
from supabase import create_client, Client
from gotrue import AuthResponse

class UserModel:
    def __init__(self) -> None:
        self.url = st.secrets["SUPABASE_URL"]
        self.key = st.secrets["SUPABASE_PUBLIC_KEY"]
        self.client = create_client(self.url, self.key)

    def sign_up(self, email: str, password: str) -> AuthResponse | Exception:
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            return e
        
    def sign_in(self, email: str, password: str) -> AuthResponse | Exception:
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            return e
        
    def sign_out(self) -> None | Exception:
        try:
            self.client.auth.sign_out()
            return None
        except Exception as e:
            return e
        
    def set_session(self, access_token: str, refresh_token: str) -> AuthResponse | Exception:
        try:
            return self.client.auth.set_session(access_token, refresh_token)
        except Exception as e:
            return e