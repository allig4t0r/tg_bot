import logging
from outline_vpn.outline_vpn import OutlineVPN, OutlineServerErrorException, OutlineLibraryException

import misc.config as config

logger = logging.getLogger(__name__)

class OutlineServer(object):
    def __init__(self, api_url: str = config.OUTLINE_API_URL, cert_sha256: str = config.OUTLINE_CERT) -> None:
        self.api_url = api_url
        self.cert_sha256 = cert_sha256
        self.outline = None
    def __enter__(self):
        try:
            self.outline = OutlineVPN(api_url=self.api_url,
                                      cert_sha256=self.cert_sha256)
            logger.info("OUTLINE: connected to server "
                        f"{self.outline.get_server_information().get('hostnameForAccessKeys')} successfully")
            return self.outline
        except OutlineServerErrorException as e:
            logger.exception(f"OUTLINE: some weird server error, {e}")
        except OutlineLibraryException as e:
            logger.exception(f"OUTLINE: some weird library error, {e}")
    def __exit__(self, exc_type, exc_value, traceback):
        if self.outline:
            logger.debug("OUTLINE: connection to "
                         f"{self.outline.get_server_information().get('hostnameForAccessKeys')} was closed")
            self.outline.session.close()


# OutlineKey(key_id='36', name='Митя', password='aslkfhaslkdj', port=123, 
#            method='chacha20-ietf-poly1305', 
#            access_url='ss://abcdeg@123123123:123/?outline=1', 
#            used_bytes=333193160, data_limit=None)