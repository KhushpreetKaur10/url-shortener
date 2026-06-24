from flask import Blueprint, jsonify
from db import get_db
from observability.metrics import get_metrics
from redis_client import redis_client

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/metrics")
def metrics():
    return jsonify(get_metrics())


@stats_bp.route("/cache-stats")
def cache_stats():
    return jsonify({"keys": redis_client.dbsize()})


@stats_bp.route("/stats/<short_code>")
def stats(short_code):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT long_url, clicks, created_at, last_accessed, expiry_date
        FROM urls WHERE short_code=%s
    """, (short_code,))

    result = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(DISTINCT ip_address)
        FROM analytics WHERE short_code=%s
    """, (short_code,))

    unique_visitors = cursor.fetchone()[0]

    db.close()

    if not result:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "long_url": result[0],
        "clicks": result[1],
        "created_at": str(result[2]),
        "last_accessed": str(result[3]),
        "expiry_date": str(result[4]),
        "unique_visitors": unique_visitors
    })
