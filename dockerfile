FROM python:3.11-slim

COPY ./app /home/app

WORKDIR /home/app

RUN pip install -r /home/app/requirements.txt

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.API.app:app", "--bind", "0.0.0.0:8000"]