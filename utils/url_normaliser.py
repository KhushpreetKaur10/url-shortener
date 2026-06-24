from urllib.parse import urlparse, urlunparse


def normalize_url(url):

    url = url.strip()

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()

    netloc = parsed.netloc.lower()

    if netloc.startswith("www."):
        netloc = netloc[4:]

    if ":" in netloc:
        host, port = netloc.split(":", 1)

        if (
            (scheme == "http" and port == "80")
            or
            (scheme == "https" and port == "443")
        ):
            netloc = host

    path = parsed.path.rstrip("/")

    if path == "":
        path = ""

    normalized = urlunparse(
        (
            scheme,
            netloc,
            path,
            "",
            "",
            ""
        )
    )

    return normalized