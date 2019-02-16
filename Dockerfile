FROM python:3.7-slim-stretch

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN python3 setup.py install

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "kelly_criterion_service.kelly_criterion_service:app"]
