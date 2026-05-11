# Задание № 2. API-пайплайн: данные $\rightarrow$ LLM $\rightarrow$ результат

## Запуск

Перед запуском скрипта необходимо выполнить:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

В скрипте `main.py` можно указать число новостей, которое необходимо обработать, в моём случае это 15:
```py
if __name__ == "__main__":
    main(15)
```
Если необходимо обработать все новости из входного файла, то в аргументах `main` ничего не указывайте либо укажите `None`:
```py
if __name__ == "__main__":
    main()
```

Для запуска скрипта вызовите:
```sh
python main.py
```

## Выбор LLM

В качестве нейронной сети для выполнения работы была выбрана модель `openai/gpt-oss-120b:free` из Open Router, данная модель имеет следующие характеристики: <br>
+ **Число параметров**: 120 миллиардов
+ **Контекстное окно**: 131.1 тысяч токенов
+ **Максимальный выход**: 131.1 тысяч токенов
+ **Скорость генерации**: 22 токена в секунду
+ **Время отклика**: 0.86 секунд
+ **Цена**: бесплатно

## Подключение к модели

Для подключения к модели необходимо перейти на этот [сайт](https://openrouter.ai/openai/gpt-oss-120b:free) и получить API ключ. Этот ключ нужно вставить в `.env` файл:
```env
OPEN_ROUTER_API_KEY=your-open-router-api-key
```

## Задача проекта

Скрипт main.py отправляет запрос LLM с целью получить краткие выдержки новостей из входного CSV-файла, в результате генерируется TXT-файл указанными `n` краткими содержаниями

## Работа main.py

### Подключение к модели

Загружается ключ из `.env`, подключается к модели:
```py
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    )
    MODEL_ID = "openai/gpt-oss-120b:free"
```

### Извлечение входных данных

Находится местоположение входного файла `input.csv` и создаётся data frame:
```py
    current_directory = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_directory, "input.csv")
    output_file = os.path.join(current_directory, "output.txt")
    df = pd.read_csv(input_file)
```
`input.csv` был взят [отсюда](https://www.kaggle.com/datasets/hadasu92/cnn-articles-after-basic-cleaning) и имеет следующую структуру:
| | Index | Author | Date published | Category | Section | Url | Headline | Description | Keywords | Second headline | Article text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Описание** | Индекс в таблице | Автор статьи | Дата публикации | Категория статьи | Секция статьи | URL адрес источника | Заголовок статьи | Описание | Ключевые слова | Второй заголовок | Текст статьи |
| **Пример** | 0 | 	Jacopo Prisco, CNN | 2021-07-15 02:46:59 | news | world | https://www.cnn.com... | There's a shortage of truckers... | The e-commerce boom has exacerbated... | world, There's a shortage of... | There's a shortage of truckers... | (CNN)Right now, there's a shortage of truck drivers... |

### Запрос к модели

Извлечённая новость отправляется модели, которая после обработки выдаёт результат краткого содержания, который записывается в выходной файл `output.txt`:
```py
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
```

## Пример запрос-ответа

Пример запроса:
```json
{
    "role": "system", 
    "content": "Ты — ассистент, который делает краткие и емкие пересказы новостей. Пиши только суть, без лишних фраз, на русском. Ответ возвращать строго в формате JSON. JSON содержит ключи: 'summary' (текст) и topic' (категория новости)"
},
{
    "role": "user", 
    "content": "Сделай краткое содержание этой новости:
    
    There's a shortage of truckers, but TuSimple thinks it has a solution: no driver needed - CNN
     (CNN)Right now, there's a shortage of truck drivers in the US and worldwide, exacerbated by the e-commerce boom brought on by the pandemic. One solution to the problem is autonomous trucks, and several companies are in a race to be the first to launch one. Among them is San Diego-based TuSimple.Founded in 2015, TuSimple has completed about 2 million miles of road tests with its 70 prototype trucks across the US, China and Europe..."
}
```

Пример ответа:
```json
{
    "topic": "Транспорт и технологии",
    "summary": "Транспортный дефицит водителей грузовиков усиливается ростом e‑commerce. Компания TuSimple разрабатывает полностью автономные грузовики, уже протестировала 2 млн миль на 70 прототипах в США, Китае и Европе и планирует запуск авто‑труб в 2024 году совместно с Navistar и Traton. Трассы будут заранее картографированы, что позволить покрыть 80 % грузоперевозок на 10 % коридоров. Стоимость автономного модуля – $50 000, что дешевле расходов на водителя. При полном автономном режиме машины смогут ехать круглосуточно, ускоряя доставку и сокращая смертельные случаи, связанные с людскими ошибками."
}
```

Вывод:
```txt
----- НОВОСТЬ №1: 15-07-2021 -----
 [Транспорт и технологии] Транспортный дефицит водителей грузовиков усиливается ростом e‑commerce. Компания TuSimple разрабатывает полностью автономные грузовики, уже протестировала 2 млн миль на 70 прототипах в США, Китае и Европе и планирует запуск авто‑труб в 2024 году совместно с Navistar и Traton. Трассы будут заранее картографированы, что позволить покрыть 80 % грузоперевозок на 10 % коридоров. Стоимость автономного модуля – $50 000, что дешевле расходов на водителя. При полном автономном режиме машины смогут ехать круглосуточно, ускоряя доставку и сокращая смертельные случаи, связанные с людскими ошибками.
==================================
```