import re
import dns.resolver
from smtplib import SMTP
from settings import Config

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def valid_email_format(email: str):
    if re.fullmatch(regex, email):
        return True
    return False


def is_disposable_domain(domain: str):
    if domain in Config.DISPOSABLE_DOMAIN:
        return True
    return False


def extract_mx_record(domain: str) -> list:
    answers = dns.resolver.resolve(domain, 'MX')
    return [answer.exchange for answer in answers]


def verify_email(domain: str, email: str):
    mx_records = extract_mx_record(domain)
    
    with SMTP(host=mx_records[-1].to_text()[:-1], port=25) as smtp:
        smtp.helo(domain)
        smtp.mail("<>")
        code, msg = smtp.rcpt(email)
        if code == 250:
            return True
        return False