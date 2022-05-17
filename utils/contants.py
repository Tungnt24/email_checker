import socks

EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

PROXY = {"socks4": socks.SOCKS4, "socks5": socks.SOCKS5}

BLOCKED_KEYWORDS = [
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
    if any([keyword.encode() in response for keyword in BLOCKED_KEYWORDS]):
        return dict(
            message="Blocked by mail server", deliverable=False, host_exists=True
        )
    else:
        return dict(deliverable=False, host_exists=True)

HANDLE_ERROR = {
    550: handle_550,
    551: lambda _: dict(deliverable=False, host_exists=True),
    552: lambda _: dict(deliverable=True, host_exists=True, full_inbox=True),
    553: lambda _: dict(deliverable=False, host_exists=True),
    450: lambda _: dict(deliverable=False, host_exists=True),
    451: lambda _: dict(
        deliverable=False, message="Local error processing, try again later."
    ),
    452: lambda _: dict(deliverable=True, full_inbox=True),
    521: lambda _: dict(deliverable=False, host_exists=False),
    421: lambda _: dict(
        deliverable=False,
        host_exists=True,
        message="Service not available, try again later.",
    ),
    441: lambda _: dict(deliverable=True, full_inbox=True, host_exists=True),
}