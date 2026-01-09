FROM python:3.13-slim

WORKDIR /generator

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/generator

CMD ["python", "main.py"]