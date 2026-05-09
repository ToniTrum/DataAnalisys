import streamlit as st

from Controllers import ChatController, LlmController
from .Chat import Chat


def ChatList(user_id: str, chat_controller: ChatController, llm_controller: LlmController) -> None:
    chats = chat_controller.get_user_chat_list(user_id)

    if not chats:
        st.sidebar.info("У вас пока нет чатов")
        return
    
    chat_pages = []
    for chat in chats:
        def create_page(chat_id: int, title: str, chat_controller: ChatController, llm_controller: LlmController) -> Chat:
            return Chat(chat_id, title, chat_controller, llm_controller)

        chat_pages.append(st.Page(
            lambda chat=chat: create_page(chat["chat_id"], chat["title"], chat_controller, llm_controller),
            title=chat["title"],
            url_path=f"/{chat['id']}",
        ))

    pages = st.navigation({"Чаты:": chat_pages})
    pages.run()