import smtplib

import dns.resolver as resolver
from wrapt_timeout_decorator import *

from utils.socks_smtp import ProxySMTP
from utils.contants import HANDLE_ERROR, PROXY


handle_unrecognised = lambda a: dict(
    message=f"Unrecognised error: {a}", deliverable=False
)

class SMTPRecepientException(Exception):
    def __init__(self, code, response):
        self.code = code
        self.response = response


class UnknownProxyError(Exception):
    def __init__(self, proxy_type):
        self.msg = f"The proxy type {proxy_type} is not known\n Try one of socks4, socks5 or http"


class TimeoutError(Exception):
    pass


class Verifier:
    def __init__(self, source_addr, proxy_type=None, proxy_addr=None, proxy_port=None):

        if proxy_type:
            try:
                self.proxy_type = PROXY[proxy_type]
                print(self.proxy_type)
            except KeyError:
                raise UnknownProxyError(proxy_type)
        else:
            self.proxy_type = None
        self.source_addr = source_addr
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port

    @timeout(5, timeout_exception=TimeoutError, use_signals=False)
    def deliver(self, exchange: str, address: str):
        with ProxySMTP(
            host=exchange[:-1],
            port=25,
            proxy_addr=self.proxy_addr,
            proxy_port=self.proxy_port,
        ) as smtp:
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
        lookup = {"deliverable": False, "full_inbox": False, "result": None, "message": None}
        _, _, domain = email.partition("@")
        mail_exchangers = self.extract_mx_record(domain)
        try:
            deliverable = self.deliver(mail_exchangers[-1], email)
            if deliverable:
                lookup.update({
                    "deliverable": deliverable,
                    "result": "Valid",
                    "message": "The email address is valid."
                })
                return lookup
        except SMTPRecepientException as err:
            kwargs = HANDLE_ERROR.get(err.code, handle_unrecognised)(err.response)
            lookup = {**lookup, **kwargs}
        except (
            smtplib.SMTPServerDisconnected,
            smtplib.SMTPConnectError,
            TimeoutError,
        ):
            lookup.update({
                "deliverable": False,
                "result": "Unknown",
                "message": "Invalid response from the SMTP server."
            })
            return lookup
        if not lookup.get("deliverable"):
            lookup.update({
                        "result": "Invalid",
                        "message": "The mailbox doesn't exist."
                    })
        return lookup
