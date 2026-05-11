import streamlit as st

from Presenter import ChatPresenter, LlmPresenter
from .Chat import Chat


def ChatList(user_id: str, chat_presenter: ChatPresenter, llm_presenter: LlmPresenter) -> None:
    chats = chat_presenter.get_user_chat_list(user_id)

    if not chats:
        st.sidebar.info("У вас пока нет чатов")
        return
    
    chat_pages = []
    for chat in chats:
        def create_page(
                chat_id: int, title: str, user_chat_id: int, 
                chat_presenter: ChatPresenter, llm_presenter: LlmPresenter
            ) -> Chat:
            return Chat(chat_id, title, user_chat_id, chat_presenter, llm_presenter)

        chat_pages.append(st.Page(
            lambda chat=chat: create_page(
                chat["chat_id"], chat["title"], chat["id"],
                chat_presenter, llm_presenter
            ),
            title=chat["title"],
            url_path=f"/{chat['id']}",
        ))

    pages = st.navigation({"Чаты:": chat_pages})
    pages.run()