import streamlit as st
import pandas as pd

from Controllers import ChatController, LlmController

def Chat(chat_id: int, title: str, chat_controller: ChatController, llm_controller: LlmController) -> None:
    messages = chat_controller.get_messages(chat_id)
    if 'file_key' not in st.session_state:
        st.session_state.file_key = 0
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    chat_container = st.container()
    with chat_container:
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    with st.bottom:
        st.divider()
        uploaded_file = st.file_uploader(
            "Прикрепите CSV файл для анализа",
            type=["csv"],
            key=st.session_state['file_key'],
            accept_multiple_files=False
        )

        if uploaded_file is not None:
            if prompt := st.chat_input("Опишите, что хотите"):
                st.session_state.uploaded_file = uploaded_file
                
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)

                messages.append({"role": "user", "content": prompt})

                df = pd.read_csv(uploaded_file)
                df_json = df.to_json(orient='records') 
                df_info = f"Вот данные из файла в формате JSON: {df_json}"

                st.session_state['file_key'] += 1
                st.rerun()

    if st.session_state.get("is_generated"):
        with chat_container:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""

                # for chunk in llm_controller.generate_response(messages, df_info):
                #     full_response += chunk
                #     response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

        messages.append({"role": "assistant", "content": full_response})
        # chat_controller.update_messages(chat_id, messages)
