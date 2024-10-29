import hashlib

from urllib.parse import urlparse


def hash_string(input_string: str) -> str:
    """Hash a string using SHA256."""
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()


def get_domain(url: str) -> str:
    """Extract the domain from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc


def get_path(url: str) -> str:
    """Extract the path from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.path
