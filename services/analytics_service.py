from repositories.analytics_repo import increment_click, log_access


def track_click(cursor, short_code, ip, user_agent):
    increment_click(cursor, short_code)
    log_access(cursor, short_code, ip, user_agent)
