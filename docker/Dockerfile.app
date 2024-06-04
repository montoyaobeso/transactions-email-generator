FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY .env /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

ENTRYPOINT ["python", "-m", "src.app.main"]