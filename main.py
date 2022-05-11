import re
import dns.resolver
from smtplib import SMTP
from fastapi import FastAPI
from schema import Verify   
app = FastAPI()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def verify_email_format(email: str):
    if re.fullmatch(regex, email):
        return True
    return False


def is_disposable_domain(domain: str):
    pass


def extract_mx_record(domain: str) -> list:
    answers = dns.resolver.query(domain, 'MX')
    return [answer.host for answer in answers]


def verify_email(host: str):
    with SMTP(host="", port=25) as smtp:
        pass

@app.post("/verify", response_model=Verify, response_model_exclude_unset=True)
async def verify(email: str):
    if not verify_email_format(email):
        return Verify(email=email,
                      status="invalid",
                      reason="The email address format is not valid"
                      )
    username, _, domain = email.partition('@')
    if is_disposable_domain(domain):
        return Verify(email=email,
                      status="invalid",
                      reason="It's a disposable email address")
    extract_mx_record(domain)
    
    return {"message": "Tomato"}

