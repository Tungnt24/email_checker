from workers.celery_app import celery_app
from settings import Config
from verifier import Verifier


@celery_app.task
def verify_email(email: str):
    result = {'deliverable': False, 'full_inbox': False}
    for proxy in Config.PROXIES:
        print("A")
        host, _, port = proxy.partition(":")
        print(host, port)
        socks_verifier = Verifier(
            source_addr="<>",
            proxy_type="socks4",
            proxy_addr=host,
            proxy_port=port)
        result = socks_verifier.verify(email)
        if result['deliverable']:
            print(result)
            return result
    return result