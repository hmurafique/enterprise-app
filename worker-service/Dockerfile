FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Celery broker URL will be from env
CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]
