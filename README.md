# 🚀 Distributed URL Shortener System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

---

## 📌 Overview

A scalable URL Shortener system built using Flask, MySQL, and Redis that demonstrates real-world backend system design concepts.

It implements caching, rate limiting, analytics tracking, and containerized deployment using Docker.

The system reduces database load and improves redirection performance using Redis caching.

---

## 🛠️ Tech Stack

- Flask (Python)
- MySQL
- Redis
- HTML, CSS, JavaScript
- Docker, Docker Compose
- Nginx (configured for load balancing design)
- REST API

---

## 📂 System Architecture

Client → Flask API  
↓  
Redis Cache (cache-aside strategy)  
↓ (cache miss)  
MySQL Database (source of truth)

Key points:
- Redis used for fast URL lookup
- MySQL stores persistent data
- Stateless Flask backend
- Nginx prepared for horizontal scaling

---

## 📁 Project Structure

url-shortener/  
│  
├── app.py  
├── db.py  
├── redis_client.py  
├── requirements.txt  
├── .dockerignore  
├── docker-compose.yml  
├── nginx.conf  
├── Dockerfile  
├── test_redis.py  
│  
├── templates/  
│   ├── index.html  
│   ├── dashboard.html  
│  
├── static/  
│   ├── qrcodes/  
│   ├── style.css  
│   └── script.js  
│  
├── database/  
│   └── init.sql  
│  
└── README.md  

---

## ⚙️ Features

### 🔗 URL Shortening
- Base62 short code generation
- Custom alias support
- Duplicate URL detection
- 30-day expiry support

### ⚡ Redis Caching
- Cache-aside pattern implementation
- Faster redirects for frequently used URLs
- Reduced database load

### 🚦 Rate Limiting
- Redis-based fixed-window algorithm
- 10 requests per minute per IP
- Prevents abuse and overload

### 📊 Analytics
- Total click tracking
- Unique visitors (IP-based)
- IP address logging
- User-agent tracking

### 🧾 QR Code Generation
- Auto-generated QR code for each short URL
- Easy sharing and scanning

### 🐳 Docker Setup
- Flask service
- MySQL service
- Redis service
- Docker Compose orchestration

### 🌐 Load Balancing (Design Only)
- Nginx configured for horizontal scaling
- Stateless backend design prepared for scaling

---

## 🚀 API Endpoints

### POST /shorten

Request:
{
  "url": "https://example.com",
  "alias": "optional_code"
}

Response:
{
  "short_url": "http://127.0.0.1:5000/abc123",
  "code": "abc123",
  "original_url": "https://example.com",
  "qr_url": "/static/qrcodes/abc123.png"
}

---

### GET /<short_code>

- Redirects to original URL
- Updates click analytics
- Logs request metadata

---

### GET /stats/<short_code>

{
  "short_code": "abc123",
  "long_url": "https://example.com",
  "clicks": 10,
  "unique_visitors": 5,
  "created_at": "...",
  "last_accessed": "...",
  "expiry_date": "..."
}

---

### GET /cache-stats

Returns Redis cache statistics.

---

### GET /dashboard

Displays:
- Top 10 URLs
- Total URLs created
- Total clicks
- Cache stats

---

## 🧠 System Design Concepts

- Cache-aside pattern (Redis)
- Stateless backend architecture
- Separation of cache and database
- Rate limiting using Redis counters
- Analytics tracking system
- Containerized multi-service setup

---

## 📈 Key Learnings

- Backend system design fundamentals
- Redis caching strategies
- Database schema design
- Rate limiting techniques
- Docker orchestration
- REST API design

---

## 🐳 Run Locally

Clone repository:
git clone https://github.com/KhushpreetKaur10/url-shortener.git
cd url-shortener

Start services:
docker-compose up --build

Open:
http://127.0.0.1:5000

---

## 🔮 Future Improvements

- Async analytics with queue system (Celery/Kafka)
- Sliding window rate limiting
- Kubernetes deployment
- Prometheus monitoring
- Cloud deployment (AWS/GCP)
- Authentication system

---

## 👩‍💻 Author

Khushpreet Kaur  
GitHub: https://github.com/KhushpreetKaur10
