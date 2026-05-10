import streamlit as st
import pandas as pd

from Controllers import ChatController, LlmController
from .ChatMessage import ChatMessage

def Chat(chat_id: int, title: str, user_chat_id: int, chat_controller: ChatController, llm_controller: LlmController) -> None:
    if 'file_key' not in st.session_state:
        st.session_state.file_key = 0
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'prompt' not in st.session_state:
        st.session_state.prompt = None

    messages = chat_controller.get_messages(chat_id)
    chat_container = st.container()
    with chat_container:
        for message in messages:
            ChatMessage(message)

    if not st.session_state.is_processing:
        with st.bottom:
            st.divider()
            uploaded_file = st.file_uploader(
                "Прикрепите CSV файл для анализа",
                type=["csv"],
                key=st.session_state['file_key'],
                accept_multiple_files=False,
            )

            if uploaded_file is not None:
                if prompt := st.chat_input("Опишите, что хотите"):                    
                    st.session_state.prompt = prompt
                    st.session_state.uploaded_file = uploaded_file
                    st.session_state.is_processing = True
                    st.session_state['file_key'] += 1

                    st.rerun()

    if st.session_state.is_processing:
        df = pd.read_csv(st.session_state.uploaded_file)
        table_name = st.session_state.uploaded_file.name
        preview_df = df.head(5).to_dict(orient="records")
        user_context = st.session_state.prompt

        with chat_container:
            messages.append({
                "role": "user", 
                "table_name": table_name,
                "table": preview_df,
                "content": user_context,
            })
            ChatMessage(messages[-1])

            if len(messages) == 1:
                title = llm_controller.generate_title(df, user_context)
                chat_controller.update_title(user_chat_id, title)

            with st.chat_message("assistant"):
                status_placeholder = st.empty()
                with status_placeholder.status("Идёт анализ...", expanded=True) as status:
                    try:
                        response = llm_controller.generate_response(df, user_context)
                        status.update(label="Анализ завершен!", state="complete", expanded=False)
                    except Exception as e:
                        status.update(label="Ошибка анализа", state="error")
                        response = f"Произошла ошибка при работе агента: {str(e)}"

        messages.append({
            "role": "assistant", 
            "content": response["content"],
            "plots": response["plots"]
        })
        chat_controller.update_messages(chat_id, messages)

        st.session_state.prompt = None
        st.session_state.uploaded_file = None
        st.session_state.is_processing = False

        st.rerun()
