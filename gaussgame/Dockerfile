# vytvorenie venv so vsetkymi zavislostami pre spustenie aplikacie
# FROM arm32v7/ubuntu:25.04 AS builder
# FROM --platform=linux/arm/v7 ubuntu:25.04 AS builder
FROM ubuntu:25.04 AS builder

ARG VERSION

# Inštalácia build nástrojov a systémových závislostí
RUN apt-get update && apt-get install --yes \
    build-essential \
    gfortran \
    python3-dev \
    # python3-venv \
    # python3-pip \
    libopenblas-dev \
    liblapack-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -Ls https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin bash

# create venv
ENV VENV_PATH=/app/venv
RUN uv venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# copy pyproject.toml
COPY pyproject.toml /app/


# # Inštaluj bez wheelov – build zo zdrojov (zrýchlenie vývoja)
# ENV MAKEFLAGS="-j4"
# RUN pip3 install --no-binary=numpy,numpy numpy \
#     && pip3 install pandas scipy

WORKDIR /app
