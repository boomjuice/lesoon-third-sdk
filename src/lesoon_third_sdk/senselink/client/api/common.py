import datetime
import typing as t

from lesoon_third_sdk.senselink.client.api.base import SenseLinkBaseAPI


class CommonApi(SenseLinkBaseAPI):

    def aes_decrypt(self, ciphers: t.List[str]):
        """
        将 AES 密文还原为明文，适用于人员身份证号、手机号、邮箱等。
        https://link.bi.sensetime.com/docs/95
        Args:
            ciphers：需要解密的字符串集合, 最大支持50条数据，无法解密或解密失败将返回 null

        """

        data = {'list': ciphers}
        return self._post('/api/v3/decrypt', data=data)
