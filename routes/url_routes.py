from flask import Blueprint, request, jsonify, redirect
from db import get_db

from services.url_service import shorten_url, resolve_url
from services.cache_service import get_cache, set_cache
from services.analytics_service import track_click
from observability.logger import log
from observability.metrics import inc
from utils.qr_generator import generate_qr

url_bp = Blueprint("url", __name__)

BASE_URL = "http://localhost"


# ---------------------------
# SHORTEN URL
# ---------------------------
@url_bp.route("/shorten", methods=["POST"])
def shorten():
    db = get_db()

    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "URL is required"}), 400

        result = shorten_url(db, data["url"], data.get("alias"))

        if result["status"] == "error":
            return jsonify(result), 409

        # ✅ FIX: generate QR HERE (after success)
        qr_url = generate_qr(result["short_code"])
        result["qr_url"] = qr_url

        return jsonify(result), 200

    finally:
        db.close()


# ---------------------------
# REDIRECT
# ---------------------------
@url_bp.route("/<short_code>")
def redirect_url(short_code):
    db = get_db()
    cursor = db.cursor()

    try:
        long_url = get_cache(short_code)

        if long_url:
            inc("cache_hit")
            log(f"CACHE HIT {short_code}")
        else:
            inc("cache_miss")
            log(f"CACHE MISS {short_code}")

            long_url = resolve_url(db, short_code)

            if not long_url:
                return jsonify({"error": "Not found"}), 404

            set_cache(short_code, long_url)

        track_click(
            cursor,
            short_code,
            request.remote_addr,
            request.headers.get("User-Agent")
        )

        db.commit()
        inc("redirects")

        return redirect(long_url)

    finally:
        db.close()
