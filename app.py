from redis_client import redis_client
from flask import Flask, request, jsonify, redirect, render_template
import string
from datetime import datetime, timedelta
import qrcode
import os

from db import get_db

app = Flask(__name__)

# -----------------------------
# Ensure QR directory exists
# -----------------------------
QR_DIR = "static/qrcodes"
os.makedirs(QR_DIR, exist_ok=True)
os.makedirs("static/qrcodes", exist_ok=True)

BASE_URL = "http://127.0.0.1:5000"


# -----------------------------
# QR Generator
def generate_qr(short_code):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qr_dir = os.path.join(base_dir, "static", "qrcodes")

    os.makedirs(qr_dir, exist_ok=True)

    url = f"http://127.0.0.1:5000/{short_code}"
    img = qrcode.make(url)

    file_path = os.path.join(qr_dir, f"{short_code}.png")
    img.save(file_path)

    print("QR saved at:", file_path)

    return f"/static/qrcodes/{short_code}.png"


# -----------------------------
# Redis Cache Helper
# -----------------------------
def cache_url(short_code, long_url):
    redis_client.set(short_code, long_url, ex=86400)


# -----------------------------
# Rate Limiter
# -----------------------------
def check_rate_limit(ip):
    key = f"rate:{ip}"
    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 60)

    return count <= 10


# -----------------------------
# Base62 Encoding
# -----------------------------
BASE62 = string.digits + string.ascii_letters

def encode_base62(num):
    if num == 0:
        return "0"

    result = ""
    while num:
        result = BASE62[num % 62] + result
        num //= 62

    return result


# -----------------------------
# URL Validation
# -----------------------------
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Shorten URL
# -----------------------------
@app.route("/shorten", methods=["POST"])
def shorten():
    ip = request.remote_addr

    if not check_rate_limit(ip):
        return jsonify({"error": "Too many requests"}), 429

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    long_url = data["url"]
    alias = data.get("alias")

    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    db = get_db()
    cursor = db.cursor()

    # -----------------------------
    # Existing URL check
    # -----------------------------
    cursor.execute(
        "SELECT short_code FROM urls WHERE long_url=%s",
        (long_url,)
    )

    existing = cursor.fetchone()

    if existing:
        db.close()

        short_code = existing[0]

        return jsonify({
            "message": "URL already shortened earlier.",
            "code": short_code,
            "original_url": long_url,
            "short_url": f"{BASE_URL}/{short_code}",
            "qr_url": f"/static/qrcodes/{short_code}.png"
        })

    expiry_date = datetime.now() + timedelta(days=30)

    # -----------------------------
    # Custom Alias
    # -----------------------------
    if alias:

        if not alias.isalnum():
            db.close()
            return jsonify({"error": "Alias must be alphanumeric"}), 400

        cursor.execute(
            "SELECT id FROM urls WHERE short_code=%s",
            (alias,)
        )

        if cursor.fetchone():
            db.close()
            return jsonify({"error": "Alias already exists"}), 409

        short_code = alias

        cursor.execute(
            """
            INSERT INTO urls (long_url, short_code, expiry_date)
            VALUES (%s, %s, %s)
            """,
            (long_url, short_code, expiry_date)
        )

    # -----------------------------
    # Auto Generated Code
    # -----------------------------
    else:

        cursor.execute(
            """
            INSERT INTO urls (long_url, expiry_date)
            VALUES (%s, %s)
            """,
            (long_url, expiry_date)
        )

        new_id = cursor.lastrowid
        short_code = encode_base62(new_id)

        cursor.execute(
            """
            UPDATE urls
            SET short_code=%s
            WHERE id=%s
            """,
            (short_code, new_id)
        )

    # -----------------------------
    # Commit DB once
    # -----------------------------
    db.commit()
    db.close()

    # -----------------------------
    # Cache + QR (AFTER DB)
    # -----------------------------
    cache_url(short_code, long_url)
    qr_url = generate_qr(short_code)

    return jsonify({
        "short_url": f"http://127.0.0.1:5000/{short_code}",
        "code": short_code,
        "original_url": long_url,
        "qr_url": qr_url
    })


# -----------------------------
# Redirect URL
# -----------------------------
@app.route("/<short_code>")
def redirect_url(short_code):

    long_url = redis_client.get(short_code)

    db = get_db()
    cursor = db.cursor()

    if long_url:
        print(f"[CACHE HIT] {short_code}")
    else:
        print(f"[CACHE MISS] {short_code}")

        cursor.execute(
            """
            SELECT long_url, expiry_date
            FROM urls
            WHERE short_code=%s
            """,
            (short_code,)
        )

        result = cursor.fetchone()

        if not result:
            db.close()
            return jsonify({"error": "URL not found"}), 404

        long_url, expiry_date = result

        if expiry_date and datetime.now() > expiry_date:
            db.close()
            return jsonify({"error": "URL expired"}), 410

        cache_url(short_code, long_url)

    cursor.execute(
        """
        UPDATE urls
        SET clicks = clicks + 1,
            last_accessed = NOW()
        WHERE short_code=%s
        """,
        (short_code,)
    )

    cursor.execute(
        """
        INSERT INTO analytics (short_code, ip_address, user_agent)
        VALUES (%s, %s, %s)
        """,
        (short_code, request.remote_addr, request.headers.get("User-Agent"))
    )

    db.commit()
    db.close()

    return redirect(long_url)


# -----------------------------
# Stats API
# -----------------------------
@app.route("/stats/<short_code>")
def stats(short_code):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT long_url, clicks, created_at, last_accessed, expiry_date
        FROM urls
        WHERE short_code=%s
        """,
        (short_code,)
    )

    result = cursor.fetchone()

    if not result:
        db.close()
        return jsonify({"error": "Not found"}), 404

    cursor.execute(
        """
        SELECT COUNT(DISTINCT ip_address)
        FROM analytics
        WHERE short_code=%s
        """,
        (short_code,)
    )

    unique_visitors = cursor.fetchone()[0]

    db.close()

    return jsonify({
        "short_code": short_code,
        "long_url": result[0],
        "clicks": result[1],
        "unique_visitors": unique_visitors,
        "created_at": str(result[2]),
        "last_accessed": str(result[3]),
        "expiry_date": str(result[4])
    })


# -----------------------------
# Cache Stats
# -----------------------------
@app.route("/cache-stats")
def cache_stats():
    return jsonify({
        "keys_in_cache": redis_client.dbsize()
    })


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT short_code, long_url, clicks
        FROM urls
        ORDER BY clicks DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM urls")
    total_urls = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(clicks) FROM urls")
    total_clicks = cursor.fetchone()[0] or 0

    cache_keys = redis_client.dbsize()

    db.close()

    return render_template(
        "dashboard.html",
        rows=rows,
        total_urls=total_urls,
        total_clicks=total_clicks,
        cache_keys=cache_keys
    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
