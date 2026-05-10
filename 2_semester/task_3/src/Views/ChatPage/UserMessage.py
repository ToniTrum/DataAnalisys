import streamlit as st
import pandas as pd
from typing import Dict, Any


def UserMessage(message: Dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.markdown(f"`{message['table_name']}`:")
        st.write(pd.DataFrame(message["table"]))
        st.divider()
        st.markdown(message["content"])