from fastapi import APIRouter
from schema import VerifyResponse, VerifyBase
from utils import valid_email_format, is_disposable_domain, extract_mx_record, verify_email

router = APIRouter()

@router.post("/verify", response_model=VerifyResponse, response_model_exclude_unset=True)
async def email_checker(verify: VerifyBase):
    email = verify.email
    _, _, domain = email.partition('@')
    if not valid_email_format(email):
        return VerifyResponse(email=email,
                      status="invalid",
                      reason="The email address format is not valid"
                      )

    if is_disposable_domain(domain):
        return VerifyResponse(email=email,
                      status="invalid",
                      reason="It's a disposable email address",
                      disposable=True)
    
    if await verify_email(domain, email):
        return VerifyResponse(email=email,
                        status="valid",
                        reason="The email address is valid")
    return VerifyResponse(email=email,
                        status="invalid",
                        reason="The mailbox doesn't exist.")
