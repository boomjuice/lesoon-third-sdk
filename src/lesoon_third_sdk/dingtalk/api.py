import base64
import hashlib
import hmac
import time

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.client.api.user import User


class SnsApi(DingTalkBaseAPI):

    @staticmethod
    def gen_signature(ts, sec):
        sign = base64.b64encode(
            hmac.new(sec.encode(), ts.encode(),
                     digestmod=hashlib.sha256).digest()).decode()
        return sign

    def get_userinfo_by_code(self, tmp_auth_code: str):
        ts = str(int(round(time.time()))) + '000'
        sec = self._client.app_secret
        sign = self.gen_signature(ts, sec)
        return self._post(
            '/sns/getuserinfo_bycode',
            data={
                'tmp_auth_code': tmp_auth_code,
            },
            params={
                'accessKey': self._client.app_key,
                'timestamp': ts,
                'signature': sign,
            },
        )


class UserApi(User):

    def get_by_mobile(self, mobile: str):
        return self._post('/topapi/v2/user/getbymobile', {'mobile': mobile})
