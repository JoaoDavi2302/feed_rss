FROM python:3.14-slim

ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]