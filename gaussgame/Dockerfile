FROM python:3.13-slim

RUN groupadd --system --gid 1000 pythonista \
    && adduser --no-create-home --uid 1000 --gid 1000 --disabled-password --gecos Pythonista pythonista

COPY dist/tapgame-2025.1.1-py3-none-any.whl /tmp/wheels/

RUN pip install /tmp/wheels/tapgame-2025.1.1-py3-none-any.whl

USER pythonista
WORKDIR /app
VOLUME [ "/app"]

CMD [ "python", "-m", "tapgame" ]
