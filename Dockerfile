FROM python:3.12.3-slim AS base

WORKDIR /tg_bot

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3

COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root

FROM base as final

RUN apt-get update && \
    apt-get install -y cron --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL org.opencontainers.image.source=https://github.com/allig4t0r/tg_bot

COPY . .
COPY --from=builder /tg_bot/.venv ./.venv

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]