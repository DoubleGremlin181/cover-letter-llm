FROM python:3.10-slim

RUN pip install poetry==1.8.4

WORKDIR /app
COPY . /app

RUN poetry install
RUN poetry run playwright install --with-deps chromium

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py"]
