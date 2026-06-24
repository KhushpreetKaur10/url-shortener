from flask import request, jsonify
from services.rate_limit_service import is_allowed

def check_rate_limit():
    ip = request.remote_addr

    if not is_allowed(ip):
        return jsonify({
            "status": "error",
            "message": "Rate limit exceeded"
        }), 429
