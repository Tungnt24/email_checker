import re
import dns.resolver as resolver
from settings import Config
from verifier import Verifier

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def valid_email_format(email: str):
    if re.fullmatch(regex, email):
        return True
    return False


def is_disposable_domain(domain: str):
    if domain in Config.DISPOSABLE_DOMAIN:
        return True
    return False


def valid_domain(domain: str):
    try:
        resolver.resolve(domain, "MX")
        return True
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers):
        return False
