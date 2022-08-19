FROM python:3.8.8
WORKDIR /app
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY app /app

CMD ["python","main.py"]
