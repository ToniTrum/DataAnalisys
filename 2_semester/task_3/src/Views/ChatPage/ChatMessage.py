import streamlit as st
import pandas as pd
from typing import Dict, Any


def ChatMessage(message: Dict[str, Any]) -> None:
    role = message["role"]
    if role == "user":
        with st.chat_message("user"):
            st.markdown(f"`{message['table_name']}`:")
            st.write(pd.DataFrame(message["table"]))
            st.divider()
            st.markdown(message["content"])
    if role == "assistant":
        with st.chat_message("assistant"):
            for plot in message["plots"]:
                st.plotly_chart(plot, width="stretch")
            st.markdown(message["content"])
