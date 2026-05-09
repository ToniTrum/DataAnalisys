import streamlit as st
import pandas as pd
import io
import contextlib
from openai import OpenAI

class LlmController:
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=st.secrets["OPEN_ROUTER_API_KEY"],
        )
        self.model_id = st.secrets["OPEN_ROUTER_MODEL_ID"]

    def execute_python(self, code: str, df: pd.DataFrame) -> str:
        local_vars = {"df": df, "pd": pd, "plt": None}
        output = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(output):
                exec(code, {}, local_vars)
            return f"Результат выполнения:\n{output.getvalue()}"
        except Exception as e:
            return f"Ошибка при выполнении кода: {str(e)}"

    def analyze_data(self, df: pd.DataFrame, user_prompt: str) -> str:
        buffer = io.StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()
        
        system_prompt = f"""
            Ты — эксперт-аналитик данных. В твоем распоряжении объект `df` (pandas DataFrame).
            Вот информация о колонках:
            {df_info}
            
            Твоя задача: написать Python-код для анализа, выполнить его и на основе результата сделать выводы.
            Используй функцию `python_interpreter` для запуска кода.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        tools = [{
            "type": "function",
            "function": {
                "name": "python_interpreter",
                "description": "Выполняет Python код для анализа pandas DataFrame 'df'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Код на Python"}
                    },
                    "required": ["code"]
                }
            }
        }]

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                code_to_run = eval(tool_call.function.arguments)['code']
                st.info(f"Агент выполняет код:\n```python\n{code_to_run}\n```")
                
                result = self.execute_python(code_to_run, df)
                
                messages.append(response_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "python_interpreter",
                    "content": result
                })
            
            final_response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages
            )
            return final_response.choices[0].message.content
        
        return response_message.content