FROM python:3.8-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./udjrequirements.txt .

RUN apt-get update -y && \
    apt-get install -y netcat-openbsd && \
    pip install --upgrade pip && \
    pip install -r udjrequirements.txt

COPY ./entrypoint.sh /code/entrypoint.sh
RUN chown -R $USER:$USER /code/entrypoint.sh
RUN chmod a+x /code/entrypoint.sh

COPY . .

CMD ["sh", "/code/entrypoint.sh"]