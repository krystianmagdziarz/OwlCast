import hashlib

from urllib.parse import urlparse


def hash_string(s:str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def get_domain(url: str) -> str:
    return urlparse(url).netloc


def get_path(url: str) -> str:
    return urlparse(url).path
