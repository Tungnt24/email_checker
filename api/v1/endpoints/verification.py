from fastapi import APIRouter
from api.v1.endpoints.schema import VerificationResponse, VerificationBase
from utils.validate import (
    valid_domain,
    valid_email_format,
    is_disposable_domain
)
from workers.tasks import verify_email, verify_email_without_proxy
from workers.redis_client import RedisClient

router = APIRouter()


@router.post(
    "/verification", response_model=VerificationResponse, response_model_exclude_unset=True
)
async def email_checker(verify: VerificationBase):
    email = verify.email
    _, _, domain = email.partition("@")
    redis = RedisClient()
    exists = redis.get_email(email=email)
    if exists:
        return VerificationResponse(
            email=email, status="valid", reason="The email address is valid."
        )

    if not valid_email_format(email):
        return VerificationResponse(
            email=email,
            status="invalid",
            reason="The email address format is not valid.",
        )

    if is_disposable_domain(domain):
        return VerificationResponse(
            email=email,
            status="invalid",
            reason="It's a disposable email address.",
            disposable=True,
        )
    valid, mx_exchanger = valid_domain(domain)
    if not valid:
        return VerificationResponse(
            email=email, status="invalid", reason=f"{domain} does not exist."
        )

    if "l.google.com" in mx_exchanger:
        verify = verify_email_without_proxy.delay(email)
        result = verify.get()
    else:
        verify = verify_email.delay(email)
        result = verify.get()
    return VerificationResponse(
        email=email, status=result.get("result"), reason=result.get("message")
    )
