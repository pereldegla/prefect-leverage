FROM python:3.11.4-slim-bullseye
USER root

# Add Dependencies for PySpark
RUN apt-get update
COPY requirements.txt /packages/requirements.txt

WORKDIR /packages
RUN pip install -r requirements.txt

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV PYTHONHASHSEED=1