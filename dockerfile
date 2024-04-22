FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]
