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

def verify_email(email: str):
    result = {'deliverable': False, 'full_inbox': False}
    for proxy in Config.PROXIES:
        host, _, port = proxy.partition(":")
        socks_verifier = Verifier(
            source_addr="<>",
            proxy_type="socks4",
            proxy_addr=host,
            proxy_port=port)
        result = socks_verifier.verify(email)
        if result['deliverable']:
            return result
    return result