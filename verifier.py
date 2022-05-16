import socks
import binascii
import dns.resolver as resolver
import os
from socks_smtp import ProxySMTP
import smtplib

proxy = {
    'socks4': socks.SOCKS4,
    'socks5': socks.SOCKS5
}

blocked_keywords = [
    "spamhaus",
    "proofpoint",
    "cloudmark",
    "banned",
    "blacklisted",
    "blocked",
    "block list",
    "denied",
]

def handle_550(response):
    if any([keyword.encode() in response for keyword in blocked_keywords]):
        return dict(
            message="Blocked by mail server", deliverable=False, host_exists=True
        )
    else:
        return dict(deliverable=False, host_exists=True)

handle_error = {
    550: handle_550,
    551: lambda _: dict(deliverable=False, host_exists=True),
    552: lambda _: dict(deliverable=True, host_exists=True, full_inbox=True),
    553: lambda _: dict(deliverable=False, host_exists=True),
    450: lambda _: dict(deliverable=False, host_exists=True),
    451: lambda _: dict(deliverable=False, message="Local error processing, try again later."),
    452: lambda _: dict(deliverable=True, full_inbox=True),
    521: lambda _: dict(deliverable=False, host_exists=False),
    421: lambda _: dict(deliverable=False, host_exists=True, message="Service not available, try again later."),
    441: lambda _: dict(deliverable=True, full_inbox=True, host_exists=True)
}

handle_unrecognised = lambda a: dict(message=f"Unrecognised error: {a}", deliverable=False)

class SMTPRecepientException(Exception):

    def __init__(self, code, response):
        self.code = code
        self.response = response


class UnknownProxyError(Exception):
    def __init__(self, proxy_type):
        self.msg = f"The proxy type {proxy_type} is not known\n Try one of socks4, socks5 or http"


class Verifier:

    def __init__(self,
                 source_addr,
                 proxy_type = None,
                 proxy_addr = None,
                 proxy_port = None):

        if proxy_type:
            try:
                self.proxy_type = proxy[proxy_type]
                print(self.proxy_type)
            except KeyError:
                raise UnknownProxyError(proxy_type)
        else:
            self.proxy_type = None
        self.source_addr = source_addr
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
    
    def _random_email(self, domain):
        return f'{binascii.hexlify(os.urandom(20)).decode()}@{domain}'

    def deliver(self, exchange: str, address: str):
        with ProxySMTP(host=exchange[:-1], port=25,
                proxy_addr=self.proxy_addr,
                proxy_port=self.proxy_port) as smtp:
            smtp.helo()
            smtp.mail("<>")
            test_resp = smtp.rcpt(address)
            if test_resp[0] == 250:
                deliverable = True
            elif test_resp[0] >= 400:
                raise SMTPRecepientException(*test_resp)
        return deliverable
    
    def extract_mx_record(self, domain: str) -> list:
        mx_records = resolver.resolve(domain, "MX")
        return [answer.exchange.to_text() for answer in mx_records]

    def verify(self, email):
        lookup = {
            'deliverable': False,
            'full_inbox': False,
        }
        _, _, domain = email.partition('@')
        mail_exchangers = self.extract_mx_record(domain)
        try:
            deliverable = self.deliver(mail_exchangers[-1], email)
            if deliverable:
                lookup['deliverable'] = deliverable
                return lookup
        except SMTPRecepientException as err:
            kwargs = handle_error.get(err.code, handle_unrecognised)(err.response)
            lookup = {**lookup, **kwargs}

        except smtplib.SMTPServerDisconnected as err:
            lookup['message'] = "Internal Error"
        except smtplib.SMTPConnectError as err:
            lookup['message'] = "Internal Error. Maybe blacklisted"
        return lookup
