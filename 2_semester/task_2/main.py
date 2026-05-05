import pandas as pd
import os
import json
from openai import OpenAI
from dotenv import load_dotenv


def get_summary(text: str, client: OpenAI, MODEL_ID: str) -> str:
    """
    Возвращает краткое содержание новости

    
    :param text: Текст новости
    :type text: str

    :param client: Клиент OpenAI
    :type client: OpenAI

    :param MODEL_ID: Идентификатор модели
    :type MODEL_ID: str


    :return: Краткое содержание новости или сообщение об ошибке
    :rtype: str
    """
    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=[
                    {
                        "role": "system", 
                        "content": "Ты — ассистент, который делает краткие и емкие пересказы новостей. Пиши только суть, без лишних фраз, на русском. Ответ возвращать строго в формате JSON. JSON содержит ключи: 'summary' (текст) и topic' (категория новости)"
                    },
                    {
                        "role": "user", 
                        "content": f"Сделай краткое содержание этой новости:\n\n{text}"
                    }
                ],
                response_format={"type": "json_object"}
            )

            data_json = response.choices[0].message.content.strip()
            data = json.loads(data_json)

            return f"[{data.get('topic', 'Новости')}] {data.get('summary', 'Error')}"
        except Exception as e:
            print(f"Error: {e}")

def main(n: int | None = None) -> None:
    """
    Выполняет запросы к LLM с целью получения краткой выжимки новостей

    
    :param n: Количество новостей для обработки
    :type n: int | None
    """

    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    )
    MODEL_ID = "openai/gpt-oss-120b:free"

    current_directory = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_directory, "input.csv")
    output_file = os.path.join(current_directory, "output.txt")
    df = pd.read_csv(input_file)

    if n is None:
        n = len(df)
    print(f"Starting processing. Total news: {n}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for index, row in df.head(n).iterrows():
            print(f"Processing news {index + 1}/{n}")

            text = row["Headline"] + "\n" + row["Article text"]
            result = get_summary(text, client, MODEL_ID)
            date = pd.to_datetime(row["Date published"]).strftime('%d-%m-%Y')
            
            headline = f"----- НОВОСТЬ №{index + 1}: {date} -----\n"
            f.write(headline)
            f.write(f" {result}\n")
            f.write("=" *( len(headline) - 1) + "\n\n")

    print("FINISH!!!")

if __name__ == "__main__":
    main(15)