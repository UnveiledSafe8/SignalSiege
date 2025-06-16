FROM python:3.11-slim

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /home/app

WORKDIR /home/app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.API.app:app", "--bind", "0.0.0.0:8000"]