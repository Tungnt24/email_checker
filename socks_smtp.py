import socket
import socks

from smtplib import SMTP

class ProxySMTP(SMTP):

    def __init__(self,
            host='',
            port=0,
            local_hostname=None,
            timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            source_address=None,
            proxy_type=None,
            proxy_addr=None,
            proxy_port=None):

        self.proxy_type=proxy_type
        self.proxy_addr=proxy_addr
        self.proxy_port=proxy_port

        if self.proxy_type:
            self._get_socket = self.socks_get_socket

        super(ProxySMTP, self).__init__(host, port, local_hostname, timeout, source_address)

    def socks_get_socket(self, host, port, timeout):
        if self.debuglevel>0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socks.create_connection((host, port),
                timeout=timeout,
                source_address=self.source_address,
                proxy_type=self.proxy_type,
                proxy_addr=self.proxy_addr,
                proxy_port=self.proxy_port)
