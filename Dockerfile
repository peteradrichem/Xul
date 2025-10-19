# syntax=docker/dockerfile:1
FROM python:3.9-slim-bullseye AS test

LABEL org.opencontainers.image.authors="Peter.Adrichem@gmail.com"
LABEL description="Xul Dockerfile"
LABEL version="2.0"

# Environment.
ENV \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

# System packages.
RUN \
    --mount=type=cache,target=/var/cache/apt \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install --no-install-recommends -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old

# Recent pip and wheel.
RUN pip install --upgrade pip wheel

# Create workdir
WORKDIR /app

# Install Xul package.
RUN \
    --mount=target=. \
    python -m venv /opt/venv \
    && pip install -e .[test]
