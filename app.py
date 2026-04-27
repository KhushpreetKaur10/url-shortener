from flask import Flask, request, jsonify, redirect, render_template
import string
import random
from datetime import datetime, timedelta
from db import get_db

app = Flask(__name__)

# -----------------------------
# CACHE (simulate Redis)
# -----------------------------
cache = {}


# -----------------------------
# Helper: generate short code
# -----------------------------
def generate_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(7))


# -----------------------------
# Validate URL
# -----------------------------
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")


# -----------------------------
# HOME (Frontend)
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# 1. CREATE SHORT URL
# -----------------------------
@app.route('/shorten', methods=['POST'])
def shorten():

    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400

    long_url = data['url']
    alias = data.get('alias')

    # validate URL
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    db = get_db()
    cursor = db.cursor()

    # -----------------------------
    # STEP 1: check if URL exists
    # -----------------------------
    cursor.execute(
        "SELECT short_code FROM urls WHERE long_url=%s",
        (long_url,)
    )
    existing = cursor.fetchone()

    if existing:
        response = {
            "message": "URL already exists. Returning existing short link. Alias ignored.",
            "code": existing[0],
            "original_url": long_url,
            "short_url": f"http://localhost:5000/{existing[0]}"
        }

        db.close()
        return jsonify(response)

    # -----------------------------
    # STEP 2: alias handling
    # -----------------------------
    if alias:

        if not alias.isalnum():
            db.close()
            return jsonify({"error": "Alias must be alphanumeric"}), 400

        cursor.execute(
            "SELECT short_code FROM urls WHERE short_code=%s",
            (alias,)
        )

        if cursor.fetchone():
            db.close()
            return jsonify({"error": "Alias already exists"}), 409

        short_code = alias

    else:
        short_code = generate_code()

    # -----------------------------
    # STEP 3: expiry
    # -----------------------------
    expiry_date = datetime.now() + timedelta(days=30)

    # -----------------------------
    # STEP 4: insert into DB
    # -----------------------------
    cursor.execute(
        "INSERT INTO urls (long_url, short_code, expiry_date) VALUES (%s, %s, %s)",
        (long_url, short_code, expiry_date)
    )
    db.commit()
    db.close()

    # -----------------------------
    # STEP 5: cache store
    # -----------------------------
    cache[short_code] = long_url

    return jsonify({
        "code": short_code,
        "original_url": long_url,
        "short_url": f"http://localhost:5000/{short_code}"
    })


# -----------------------------
# 2. REDIRECT (CACHE + DB + EXPIRY)
# -----------------------------
@app.route('/<short_code>')
def redirect_url(short_code):

    # -----------------------------
    # CACHE CHECK
    # -----------------------------
    if short_code in cache:
        long_url = cache[short_code]

        # still verify expiry (important fix)
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT expiry_date FROM urls WHERE short_code=%s",
            (short_code,)
        )
        result = cursor.fetchone()
        db.close()

        if result and result[0] and datetime.now() > result[0]:
            return jsonify({"error": "URL expired"}), 410

    else:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT long_url, expiry_date FROM urls WHERE short_code=%s",
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

        cache[short_code] = long_url
        db.close()

    # -----------------------------
    # UPDATE ANALYTICS
    # -----------------------------
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE urls SET clicks = clicks + 1, last_accessed = NOW() WHERE short_code=%s",
        (short_code,)
    )

    db.commit()
    db.close()

    return redirect(long_url)


# -----------------------------
# 3. STATS API
# -----------------------------
@app.route('/stats/<short_code>')
def stats(short_code):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT long_url, clicks, created_at, last_accessed, expiry_date "
        "FROM urls WHERE short_code=%s",
        (short_code,)
    )

    result = cursor.fetchone()
    db.close()

    if result:
        return jsonify({
            "short_code": short_code,
            "long_url": result[0],
            "clicks": result[1],
            "created_at": str(result[2]),
            "last_accessed": str(result[3]),
            "expiry_date": str(result[4])
        })

    return jsonify({"error": "Not found"}), 404


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)