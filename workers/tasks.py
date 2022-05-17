from workers.celery_app import celery_app
from settings import ProxyConfig
from utils.validate import verify_with_proxy, verify_without_proxy
import concurrent.futures


@celery_app.task
def verify_email(email: str):
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(ProxyConfig.PROXIES)) as executor:
        futures = []
        for proxy in ProxyConfig.PROXIES:                                       
            host, _, port = proxy.partition(":")
            futures.append(executor.submit(verify_with_proxy, email, host, port))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result.get('deliverable'):
                return result
    return result


@celery_app.task
def verify_email_without_proxy(email: str):
    result = verify_without_proxy(email)
    return result