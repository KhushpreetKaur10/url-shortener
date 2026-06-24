def insert_url(cursor, long_url, short_code, expiry):
    cursor.execute("""
        INSERT INTO urls (long_url, short_code, expiry_date)
        VALUES (%s, %s, %s)
    """, (long_url, short_code, expiry))


def get_by_code(cursor, short_code):
    cursor.execute("""
        SELECT long_url, expiry_date
        FROM urls
        WHERE short_code=%s
    """, (short_code,))
    return cursor.fetchone()
