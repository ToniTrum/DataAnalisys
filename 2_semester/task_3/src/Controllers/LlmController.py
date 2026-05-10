import pandas as pd
import streamlit as st
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_classic.agents.agent_types import AgentType


class LlmController:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model=st.secrets["OPEN_ROUTER_MODEL_ID"],
            api_key=st.secrets["OPEN_ROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
        self.model_id = st.secrets["OPEN_ROUTER_MODEL_ID"]

    def generate_response(self, df: pd.DataFrame, user_context: str) -> Any:
        agent = create_pandas_dataframe_agent(
            self.llm,
            df,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            allow_dangerous_code=True,
        )
        
        response = agent.invoke({"input": user_context})
        return response["output"]