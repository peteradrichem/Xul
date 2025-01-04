# syntax=docker/dockerfile:1
FROM python:3.9-slim-bullseye AS test

LABEL org.opencontainers.image.authors="Peter.Adrichem@gmail.com"
LABEL description="Xul Dockerfile"
LABEL version="1.0"

# Packages.
RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install --no-install-recommends -y \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Recent pip, setuptools and wheel.
RUN pip install --upgrade pip setuptools wheel

# Create workdir
WORKDIR /app

# Install package.
COPY pyproject.toml ./
COPY src src
COPY docs docs
RUN pip install .[test]

# Copy test script.
COPY test.sh ./
