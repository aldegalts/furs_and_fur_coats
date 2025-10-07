FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]
