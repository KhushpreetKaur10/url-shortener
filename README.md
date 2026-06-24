# 🚀 FastLink: Distributed URL Shortening Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

---

# 📌 Overview

FastLink is a scalable URL shortening platform built using Flask, MySQL, Redis, Docker, and Nginx.

The system supports URL shortening, custom aliases, QR code generation, URL expiration, analytics tracking, Redis caching, rate limiting, and load-balanced deployment across multiple stateless application instances.

The project demonstrates backend engineering concepts including layered architecture, cache-aside caching, observability, containerization, and horizontal scalability.

---

# 🛠️ Tech Stack

- Python
- Flask
- MySQL
- Redis
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Nginx
- Gunicorn
- REST APIs

---

# 🏗️ System Architecture

```text
                 ┌─────────────┐
                 │   Client    │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │    Nginx    │
                 │Load Balancer│
                 └──────┬──────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌────────┐     ┌────────┐     ┌────────┐
   │ App 1  │     │ App 2  │     │ App 3  │
   │ Flask  │     │ Flask  │     │ Flask  │
   └────┬───┘     └────┬───┘     └────┬───┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
   ┌──────────┐                 ┌──────────┐
   │  Redis   │                 │  MySQL   │
   │  Cache   │                 │ Database │
   └──────────┘                 └──────────┘
```

### Architectural Highlights

- Stateless Flask application instances
- Nginx-based request load balancing
- Redis Cache-Aside strategy
- MySQL as source of truth
- Layered backend architecture
- Containerized deployment using Docker Compose

---

# 📁 Project Structure

```text
url-shortener/
│
├── app.py
├── db.py
├── redis_client.py
├── requirements.txt
│
├── routes/
│   ├── url_routes.py
│   └── stats_routes.py
│
├── services/
│   ├── url_service.py
│   ├── cache_service.py
│   ├── analytics_service.py
│   └── rate_limit_service.py
│
├── repositories/
│   ├── url_repo.py
│   └── analytics_repo.py
│
├── utils/
│   ├── base62.py
│   ├── validators.py
│   ├── qr_generator.py
│   └── url_normaliser.py
│
├── observability/
│   ├── logger.py
│   └── metrics.py
│
├── middleware/
│   └── rate_limiter.py
│
├── templates/
├── static/
├── database/
│
├── docker-compose.yml
├── nginx.conf
├── Dockerfile
└── README.md
```

---

# ⚙️ Features

## 🔗 URL Shortening

- Base62 short-code generation
- Custom alias support
- Duplicate URL detection
- URL normalization
- QR-code generation
- Automatic 30-day URL expiration

## ⚡ Redis Caching

- Cache-Aside caching pattern
- Cache-first URL resolution
- Database fallback on cache miss
- 3600-second (1-hour) TTL cache retention

## 🚦 Rate Limiting

- Redis-backed fixed-window algorithm
- Atomic counter operations
- TTL-based request windows
- 10 requests per minute per IP

## 📊 Analytics

Tracks:

- Click count
- Unique visitors
- IP addresses
- User-agent metadata
- Last accessed timestamp

## 📈 Observability

Application metrics:

- Cache hits
- Cache misses
- Redirect count
- URLs created

Logging:

- Cache hit events
- Cache miss events

## 🗄️ Database Optimizations

- Indexed short-code lookups
- Unique URL constraint
- Analytics event tracking
- Click aggregation

## 🐳 Containerized Deployment

- 3 Flask application instances
- 4 Gunicorn workers per instance
- Redis service
- MySQL service
- Nginx load balancer
- Docker Compose orchestration

---

# 🚀 API Endpoints

## POST /shorten

Creates a shortened URL.

### Request

```json
{
  "url": "https://example.com",
  "alias": "custom123"
}
```

### Response

```json
{
  "status": "success",
  "short_code": "custom123",
  "short_url": "http://localhost/custom123",
  "qr_url": "/static/qrcodes/custom123.png"
}
```

---

## GET /<short_code>

Redirects to the original URL.

Features:

- Redis cache lookup
- Database fallback
- Analytics tracking
- Redirect counting

---

## GET /stats/<short_code>

Returns analytics for a shortened URL.

### Example Response

```json
{
  "long_url": "https://example.com",
  "clicks": 25,
  "created_at": "...",
  "last_accessed": "...",
  "expiry_date": "...",
  "unique_visitors": 12
}
```

---

## GET /metrics

Returns application metrics.

### Example Response

```json
{
  "cache_hit": 100,
  "cache_miss": 20,
  "redirects": 80,
  "urls_created": 40
}
```

---

## GET /cache-stats

Returns Redis cache statistics.

### Example Response

```json
{
  "keys": 150
}
```

---

# 🧠 Backend Design Concepts

- Layered Architecture (Routes → Services → Repositories → Database)
- Cache-Aside Pattern
- Stateless Backend Design
- Redis-Based Rate Limiting
- Request Analytics Tracking
- Horizontal Scaling
- Reverse Proxy Load Balancing
- Containerized Deployment
- URL Normalization
- Observability and Metrics Collection

---

# 📚 Key Learnings

- REST API development
- Backend architecture design
- Redis caching strategies
- Database indexing
- Rate limiting techniques
- Analytics collection
- Docker-based deployments
- Nginx load balancing
- Observability fundamentals

---

# 🚀 Run Locally

### Clone Repository

```bash
git clone https://github.com/KhushpreetKaur10/url-shortener.git
cd url-shortener
```

### Start Services

```bash
docker-compose up --build
```

### Access Application

```text
http://localhost
```

---

# 🔮 Future Improvements

- Sliding-window rate limiting
- Background analytics processing
- Distributed caching
- Cloud deployment (AWS / Azure / GCP)
- Prometheus monitoring
- Authentication and authorization
- Kubernetes deployment

---

# 👩‍💻 Author

**Khushpreet Kaur**

GitHub: https://github.com/KhushpreetKaur10
