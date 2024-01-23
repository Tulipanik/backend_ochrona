FROM python:3.10-slim

EXPOSE 8004

WORKDIR /code
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY user_data_manager.py ./
COPY fragile_data.db ./
COPY .env ./

CMD [ "python", "./user_data_manager.py" ]