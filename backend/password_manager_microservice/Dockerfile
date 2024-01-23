FROM python:3.10-slim

EXPOSE 8002

WORKDIR /code
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY password_manager.py ./
COPY password.db ./

CMD [ "python", "./password_manager.py" ]