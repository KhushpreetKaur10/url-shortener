metrics = {
    "cache_hit": 0,
    "cache_miss": 0,
    "redirects": 0,
    "urls_created": 0
}

def inc(metric):
    if metric in metrics:
        metrics[metric] += 1

def get_metrics():
    return metrics
