def log_access(cursor, short_code, ip, user_agent):
    cursor.execute("""
        INSERT INTO analytics (short_code, ip_address, user_agent)
        VALUES (%s, %s, %s)
    """, (short_code, ip, user_agent))


def increment_click(cursor, short_code):
    cursor.execute("""
        UPDATE urls
        SET clicks = clicks + 1,
            last_accessed = NOW()
        WHERE short_code=%s
    """, (short_code,))
