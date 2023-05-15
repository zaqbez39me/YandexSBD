FROM python:3.10-alpine3.17 as builder

RUN python3 -m venv /app
RUN /app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN /app/bin/pip install -Ur /mnt/requirements.txt --no-cache-dir --prefer-binary

FROM python:3.10-alpine3.17 as app

WORKDIR /app

COPY --from=builder /app /app
COPY . .

EXPOSE 8000

CMD /app/bin/uvicorn app.main:app --host=0.0.0.0 --port=8080