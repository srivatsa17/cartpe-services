FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install gunicorn

RUN pip install -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

RUN chmod +x /app/docker/cartpe/server-entrypoint.sh
RUN chmod +x /app/docker/celery/worker-entrypoint.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cartpe.wsgi:application"]