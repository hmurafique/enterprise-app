# Enterprise Fullstack Application Deployment Guide

This README offers a comprehensive, step-by-step guide for deploying the **Enterprise Fullstack Application**.
The application is composed of multiple services: Frontend (React), Backend (Flask), Authentication (Flask), Payments (Node.js), Worker (Celery), along with supporting infrastructure components such as Postgres, Redis, RabbitMQ, and Adminer.

---

## 🗂 Project Structure
```bash
enterprise-app/
├─ frontend-service/
│ ├─ Dockerfile
│ ├─ package.json
│ └─ src/...
├─ backend-service/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
├─ auth-service/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
├─ payments-service/
│ ├─ Dockerfile
│ ├─ package.json
│ └─ server.js
├─ worker-service/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ worker.py
├─ db-schemas/
│ └─ init.sql
├─ nginx/ (for containerized nginx option)
│ └─ nginx.conf
├─ docker-compose.yml
└─ .env
```

---


---

## Phase 1: Without Domain (Access via VM IP + Ports)

### 1️⃣ Create `.env` file (root directory)

### 2️⃣ Create docker-compose.yml (Without Domain)

### 3️⃣ Build & Run

```bash
docker-compose down -v
docker-compose up -d --build
docker ps
```

---

## Access Services via VM IP:

```bash
| Service     | Port  | URL                   |
| ----------- | ----- | --------------------- |
| Frontend    | 3000  | http\://<VM-IP>:3000  |
| Backend     | 8000  | http\://<VM-IP>:8000  |
| Auth        | 8001  | http\://<VM-IP>:8001  |
| Payments    | 8002  | http\://<VM-IP>:8002  |
| Adminer     | 8080  | http\://<VM-IP>:8080  |
| RabbitMQ UI | 15672 | http\://<VM-IP>:15672 |
```

---

## Phase 2: With Domain + SSL
## Option A: Host Machine Nginx (Reverse Proxy)

### 1️⃣ Install Nginx:

```bash
sudo apt update
sudo apt install nginx -y
```

---

### 2️⃣ Configure /etc/nginx/sites-available/enterprise-app:

```bash
server {
    listen 80;
    server_name frontend.mydomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name api.mydomain.com;

    location /auth/ {
        proxy_pass http://localhost:8001/;
    }

    location /backend/ {
        proxy_pass http://localhost:8000/;
    }

    location /payments/ {
        proxy_pass http://localhost:8002/;
    }
}
```

---

### 3️⃣ Enable site & reload:

```bash
sudo ln -s /etc/nginx/sites-available/enterprise-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### Optional: Add SSL using Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d frontend.mydomain.com -d api.mydomain.com
```

---

## Option B: Containerized Nginx

### 1️⃣ Add Nginx Service in docker-compose.yml:

```yml
  nginx-service:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - frontend-service
      - backend-service
      - auth-service
      - payments-service
```

---

### 2️⃣ Create nginx/nginx.conf:

```nginx
server {
    listen 80;

    server_name frontend.mydomain.com;
    location / {
        proxy_pass http://frontend-service:3000;
    }

    server_name api.mydomain.com;
    location /auth/ {
        proxy_pass http://auth-service:6000/;
    }
    location /backend/ {
        proxy_pass http://backend-service:5000/;
    }
    location /payments/ {
        proxy_pass http://payments-service:7000/;
    }
}
```

---

### 3️⃣ Run all services with containerized Nginx:

```bash
docker-compose down -v
docker-compose up -d --build
```

---
