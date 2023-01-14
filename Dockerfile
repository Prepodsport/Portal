# Pull base image
FROM python:3.11.0-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /Users/Evgen/PycharmProjects/Portal

# Install dependencies
COPY ./requirements.txt .

# Copy project
COPY . .