from datetime import datetime, timedelta

from repositories.url_repo import (
    insert_url,
    get_by_code
)

from utils.validators import is_valid_url
from utils.url_normaliser import normalize_url
from utils.base62 import encode_base62
from observability.metrics import inc


DEFAULT_EXPIRY_DAYS = 30


def shorten_url(db, long_url, alias=None):

    long_url = normalize_url(long_url)

    if not is_valid_url(long_url):
        return {
            "status": "error",
            "code": "INVALID_URL",
            "message": "Invalid URL format"
        }

    cursor = db.cursor()

    # -------------------------------
    # CHECK SAME URL
    # -------------------------------

    cursor.execute(
        """
        SELECT short_code
        FROM urls
        WHERE long_url=%s
        """,
        (long_url,)
    )

    existing = cursor.fetchone()

    if existing:
        return {
            "status": "success",
            "code": "ALREADY_EXISTS_URL",
            "message": "URL already shortened earlier",
            "short_code": existing[0],
            "short_url": f"http://localhost/{existing[0]}"
        }

    expiry_date = datetime.utcnow() + timedelta(days=DEFAULT_EXPIRY_DAYS)

    # -------------------------------
    # CUSTOM ALIAS
    # -------------------------------

    if alias:

        alias = alias.strip().lower()

        if not alias.isalnum():
            return {
                "status": "error",
                "code": "INVALID_ALIAS",
                "message": "Alias must contain only letters and numbers"
            }

        cursor.execute(
            """
            SELECT id
            FROM urls
            WHERE short_code=%s
            """,
            (alias,)
        )

        if cursor.fetchone():
            return {
                "status": "error",
                "code": "ALIAS_EXISTS",
                "message": "Alias already exists"
            }

        insert_url(
            cursor,
            long_url,
            alias,
            expiry_date
        )

        db.commit()
        inc("urls_created")

        return {
            "status": "success",
            "code": "CREATED",
            "message": "URL shortened successfully",
            "short_code": alias,
            "short_url": f"http://localhost/{alias}"
        }

    # -------------------------------
    # AUTO GENERATED
    # -------------------------------

    cursor.execute(
        """
        INSERT INTO urls
        (long_url, expiry_date)
        VALUES (%s, %s)
        """,
        (
            long_url,
            expiry_date
        )
    )

    url_id = cursor.lastrowid

    short_code = encode_base62(url_id)

    cursor.execute(
        """
        UPDATE urls
        SET short_code=%s
        WHERE id=%s
        """,
        (
            short_code,
            url_id
        )
    )

    db.commit()
    inc("urls_created")

    return {
        "status": "success",
        "code": "CREATED",
        "message": "URL shortened successfully",
        "short_code": short_code,
        "short_url": f"http://localhost/{short_code}"
    }


def resolve_url(db, short_code):

    cursor = db.cursor()

    result = get_by_code(cursor, short_code)

    if not result:
        return None

    long_url, expiry_date = result

    if expiry_date and expiry_date < datetime.utcnow():
        return None

    return long_url