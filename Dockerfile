FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./app/log_conf.k8s.yaml /code/app/log_conf.yaml

ENV PYTHONPATH=/code/app
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "--access-logfile", "/app-data/log/access.log", "--error-logfile", "/app-data/log/error.log", "app.api.main:app"]
