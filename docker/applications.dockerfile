FROM python:3.11

WORKDIR /app

COPY ../app/requirements.txt .
RUN pip install asyncpg --only-binary=:all:
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]