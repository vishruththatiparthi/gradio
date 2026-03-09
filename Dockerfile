FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

RUN chmod +x scripts/start_services.sh

CMD ["./scripts/start_services.sh"]
