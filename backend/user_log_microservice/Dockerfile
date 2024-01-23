FROM python:3.10-slim

EXPOSE 8001

WORKDIR /code
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY user_data_validation.py ./
COPY user_database.db ./

CMD [ "python", "./user_data_validation.py" ]