FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim


COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
