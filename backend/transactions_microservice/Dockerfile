FROM python:3.10-slim

EXPOSE 8005

WORKDIR /code
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY transactions_manager.py ./
COPY transactions.db ./

CMD [ "python", "./transactions_manager.py" ]