import re

import dns.resolver as resolver

from utils.verifier import Verifier
from settings import DomainConfig
from utils.contants import EMAIL_PATTERN
from workers.redis_client import RedisClient


def valid_email_format(email: str):
    if re.fullmatch(EMAIL_PATTERN, email):
        return True
    return False


def is_disposable_domain(domain: str):
    if domain in DomainConfig.DISPOSABLE_DOMAIN:
        return True
    return False


def valid_domain(domain: str):
    try:
        mx_records = resolver.resolve(domain, "MX")
        mx_exchangers = [answer.exchange.to_text() for answer in mx_records]
        return True, mx_exchangers[-1]
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers):
        return False


def verify_with_proxy(email, host, port):
    socks_verifier = Verifier(
        source_addr="<>", proxy_type="socks4", proxy_addr=host, proxy_port=port
    )
    result = socks_verifier.verify(email)
    if result.get("deliverable"):
        redis = RedisClient()
        redis.cache_email(email, 86400)
    elif result.get("result") == "unknown":
        redis = RedisClient()
        redis.cache_email(email, 60)
    return result


def verify_without_proxy(email):
    normal_verifier = Verifier(source_addr='<>')
    result = normal_verifier.verify(email)
    return result
