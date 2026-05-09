from typing import List, Dict, Any
import streamlit as st

from Models import ChatModel, UserChatModel

class ChatController:
    def __init__(self, chat_model: ChatModel, user_chat_model: UserChatModel) -> None:
        self.chat_model = chat_model
        self.user_chat_model = user_chat_model

    def get_user_chat_list(self, user_id: str) -> List[Dict[str, Any]]:
        return self.user_chat_model.get_user_chat_list(user_id)
    
    def get_messages(self, chat_id: int) -> List[Dict[str, Any]]:
        return self.chat_model.get_messages(chat_id)
    
    def create_new_chat(self, user_id: str) -> int:
        chats = self.user_chat_model.find_user_chat_by_title(user_id)
        if chats:
            return chats[0]["chat_id"]
        
        chat_id = self.chat_model.create_empty_chat()
        self.user_chat_model.link_chat_to_user(user_id, chat_id)
        return chat_id
    
    def choose_chat(self, chat_id: int) -> None:
        st.session_state["current_chat_id"] = chat_id

    def update_title(self, user_chat_id: int, new_title: str) -> None:
        self.user_chat_model.update_chat_title(user_chat_id, new_title)