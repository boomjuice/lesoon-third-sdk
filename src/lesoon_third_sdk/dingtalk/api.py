import base64
import hashlib
import hmac
import time

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.client.api.employeerm import Employeerm
from dingtalk.client.api.user import User
from dingtalk.core.utils import to_text


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


class EmployeermApi(Employeerm):

    def list_v2(self, userid_list, field_filter_list=()):
        """
        批量获取员工花名册字段信息
        智能人事业务，企业/ISV根据员工id批量访问员工花名册信息

        :param userid_list: 员工id列表
        :param field_filter_list: 需要获取的花名册字段信息
        """
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        if isinstance(field_filter_list, (list, tuple, set)):
            field_filter_list = ','.join(map(to_text, field_filter_list))
        data = {'userid_list': userid_list, 'agentid': self._client.agent_id}
        if field_filter_list:
            data['field_filter_list'] = field_filter_list
        return self._post('topapi/smartwork/hrm/employee/v2/list', data)
