from fastapi import APIRouter
from schema import VerificationResponse, VerificationBase
from utils import (
    valid_domain,
    valid_email_format,
    is_disposable_domain
)
from workers.tasks import verify_email
router = APIRouter()


@router.post(
    "/verification", response_model=VerificationResponse, response_model_exclude_unset=True
)
async def email_checker(verify: VerificationBase):
    email = verify.email
    _, _, domain = email.partition("@")
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

    if not valid_domain(domain):
        return VerificationResponse(
            email=email, status="invalid", reason=f"{domain} does not exist."
        )

    result = verify_email.delay(email)
    if result["deliverable"]:
        return VerificationResponse(
            email=email, status="valid", reason="The email address is valid."
        )
    return VerificationResponse(
        email=email, status="invalid", reason="The mailbox doesn't exist."
    )
