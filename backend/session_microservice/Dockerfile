FROM python:3.10-slim

EXPOSE 8003

WORKDIR /code
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY session.py ./
COPY session.db ./

CMD [ "python", "./session.py" ]