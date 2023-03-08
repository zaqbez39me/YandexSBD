FROM python:3.7-alpine3.12 as builder

RUN python3 -m venv /app
RUN /app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /app/bin/pip install -Ur /mnt/requirements.txt

FROM python:3.7-alpine3.12 as app

WORKDIR /app

COPY --from=builder /app /app
COPY . .

EXPOSE 8000

CMD /app/bin/python -m alembic upgrade head && /app/bin/uvicorn app.main:app --host=0.0.0.0 --port=8080