# 🚀 URL Shortener Service (Scalable Backend System)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-FF6F00?style=for-the-badge&logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Project-Active-brightgreen?style=for-the-badge)

---

## 📌 Overview

A production-style URL Shortener API built using Flask and MySQL with caching, analytics, and expiry handling.  
This project simulates real-world backend systems used in scalable link management platforms.

---

## 🛠️ Tech Stack

Backend: Flask (Python)  
Database: MySQL  
Frontend: HTML, CSS, JavaScript (basic UI)  
Caching: Python Dictionary (Redis-like simulation)  
Concepts: REST API, DBMS, System Design, OOP  

---

## 📂 Project Structure

```text
url-shortener/
│
├── app.py
├── db.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── database/
│   └── url_shortener.sql
│
└── screenshots/
    └── demo.png
```

---

## 🚀 API Endpoints

### 1. Shorten URL

POST /shorten

Request:
```json
{
  "url": "https://example.com",
  "alias": "optional_custom_name"
}
```

Response:
```json
{
  "code": "abc123",
  "original_url": "https://example.com",
  "short_url": "http://localhost:5000/abc123"
}
```

---

### 2. Redirect URL

GET /<short_code>

Redirects user to original URL  
Updates click analytics  

---

### 3. Stats API

GET /stats/<short_code>

Response:
```json
{
  "short_code": "abc123",
  "long_url": "https://example.com",
  "clicks": 10,
  "created_at": "2026-01-01",
  "last_accessed": "2026-01-02",
  "expiry_date": "2026-02-01"
}
```

---

## ⚙️ How It Works

- User submits a long URL  
- System checks if URL already exists  
- If not, generates a unique short code  
- Stores mapping in MySQL  
- Caches result for faster access  
- Redirects users using short URL  
- Tracks analytics on each click  

---

## 🧠 Key Engineering Highlights

- Cache layer reduces database load  
- Idempotent URL mapping prevents duplication  
- Expiry system simulates real-world lifecycle  
- Clean REST API design  
- Separation of cache and database layers  
- Efficient redirect handling  

---

## 📈 Future Improvements

- Replace in-memory cache with Redis  
- Add analytics dashboard (React frontend)  
- Dockerize application  
- Deploy on cloud (AWS / Render)  
- Add authentication system  
- Generate QR codes for short URLs  

---

## ⭐ Why this project matters

- Backend system design thinking  
- REST API development skills  
- Database design and management  
- Caching and performance optimization  
- Scalable architecture understanding  
- Real-world analytics system design  

---

## 🧪 Run Locally

pip install flask mysql-connector-python  
python app.py  

Open:  
http://localhost:5000/

---

## 👨‍💻 Author

Khushpreet Kaur  

GitHub: (https://github.com/KhushpreetKaur10)
