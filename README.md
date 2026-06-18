# 🚀 Distributed URL Shortener System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

---

## 📌 Overview

A scalable URL Shortener system built using Flask, MySQL, and Redis that simulates real-world backend architecture.

Features:
- Fast URL redirection using Redis caching
- Custom alias support
- Rate limiting using Redis
- Click analytics tracking
- QR code generation
- Docker-based multi-service setup

---

## 🛠️ Tech Stack

- Flask (Python)
- MySQL
- Redis
- HTML, CSS, JavaScript
- Docker, Docker Compose
- Nginx (for load balancing design)
- REST API, System Design concepts

---

## 📂 Architecture

Client → Flask API → Redis Cache → MySQL Database

Includes:
- Redis caching layer
- MySQL persistent storage
- Rate limiting via Redis
- Analytics logging
- QR code generator

---

## ⚙️ Features

### 🔗 URL Shortening
- Base62 short code generation
- Custom alias support
- Duplicate URL detection

### ⚡ Redis Caching
- Cache-aside strategy
- Faster redirects
- Reduced DB load

### 🚦 Rate Limiting
- Redis fixed-window algorithm
- 10 requests per minute per IP

### 📊 Analytics
- Click tracking
- Unique visitors
- IP and user-agent logging

### 🧾 QR Code Generation
- Auto-generated QR for each short URL

### 🐳 Docker Setup
- Flask service
- MySQL service
- Redis service
- Docker Compose orchestration

### 🌐 Load Balancing Design
- Nginx configured for horizontal scaling
- Stateless backend design

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
- Logs user activity

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
Returns Redis cache usage statistics

---

### GET /dashboard
- Top 10 URLs
- Total URLs created
- Total clicks
- Cache stats

---

## 🧠 System Design Concepts

- Cache-aside pattern using Redis
- Stateless backend architecture
- Separation of cache and DB
- Rate limiting system
- Analytics logging system
- Containerized microservices

---

## 📈 Key Learnings

- Backend system design basics
- Redis caching strategies
- Database schema design
- Rate limiting techniques
- Docker orchestration
- REST API design

---

## 🐳 Run Locally

docker-compose up --build

Open:
http://127.0.0.1:5000

---

## 🔮 Future Improvements

- Async analytics (queue system)
- Sliding window rate limiter
- Kubernetes deployment
- Prometheus monitoring
- Cloud deployment (AWS/GCP)
- Authentication system

---

## 👨‍💻 Author

Khushpreet Kaur  
GitHub: https://github.com/KhushpreetKaur10
