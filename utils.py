import re
import dns.resolver
import smtplib
from settings import Config
import socket

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
        dns.resolver.resolve(domain, "MX")
        return True
    except dns.resolver.NXDOMAIN:
        return False


def extract_mx_record(domain: str) -> list:
    answers = dns.resolver.resolve(domain, "MX")
    return [answer.exchange for answer in answers]



def verify_email(domain: str, email: str, timeout=20):
    mx_records = extract_mx_record(domain)
    host = mx_records[-1].to_text()[:-1]
    try:
        smtp = smtplib.SMTP(host, timeout=timeout)
        status, _ = smtp.ehlo()
        if status >= 400:
            smtp.quit()
            print(f'{host} answer: {status} - {_}\n')
            return False
        smtp.mail('')
        status, _ = smtp.rcpt(email)
        if status >= 400:
            print(f'{host} answer: {status} - {_}\n')
            result = False
        if status >= 200 and status <= 250:
            result = True

        print(f'{host} answer: {status} - {_}\n')
        smtp.quit()

    except smtplib.SMTPServerDisconnected:
        print(f'Server does not permit verify user, {host} disconnected.\n')
    except smtplib.SMTPConnectError:
        print(f'Unable to connect to {host}.\n')
    except socket.timeout as e:
        print(f'Timeout connecting to server {host}: {e}.\n')
        return None
    except socket.error as e:
        print(f'ServerError or socket.error exception raised {e}.\n')
        return None 
    except Exception as e:
        return False
