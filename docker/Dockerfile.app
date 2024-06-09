FROM public.ecr.aws/lambda/python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY .env /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

ENV POSTGRES_HOST=host.docker.internal

ENTRYPOINT ["python", "-m", "src.app.cli"]

