import logging
import random
import time

from dingtalk.client import AppKeyClient as _Client
from dingtalk.core.exceptions import DingTalkClientException

from lesoon_third_sdk.dingtalk.api import AttendanceApi
from lesoon_third_sdk.dingtalk.api import EmployeermApi
from lesoon_third_sdk.dingtalk.api import SnsApi
from lesoon_third_sdk.dingtalk.api import UserApi
from lesoon_third_sdk.dingtalk.api import YiDaApi

logger = logging.getLogger(__name__)


class AppKeyClient(_Client):
    sns = SnsApi()
    user = UserApi()
    employeerm = EmployeermApi()
    attendance = AttendanceApi()

    def __init__(self, *args, agent_id: int, retry_times: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent_id = agent_id
        self.retry_times = retry_times

    def _handle_request_except(self, e, func, *args, **kwargs):
        if self.auto_retry:
            res = self._decode_result(e.response)
            if e.errcode in (
                    15,  # 钉钉远程调用异常
            ) or (e.errcode == 88  # 鉴权异常
                  and res.sub_code
                  in ('90001', '90002', '90003', '90004', '90005', '90006')):
                if 'retry_times' not in kwargs:
                    kwargs['retry_times'] = self.retry_times
                if kwargs['retry_times']:
                    kwargs['retry_times'] -= 1
                    time.sleep(random.randint(10, 20))
                    return func(*args, **kwargs)
        super()._handle_request_except(e, func, *args, **kwargs)


class NewAppKeyClient(AppKeyClient):
    API_BASE_URL = 'https://api.dingtalk.com'

    yida = YiDaApi()

    def _handle_pre_request(self, method, uri, kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'x-acs-dingtalk-access-token' in kwargs['headers']:
            raise ValueError('headers中会自动携带access_token, 无需传入')
        kwargs['headers']['x-acs-dingtalk-access-token'] = self.access_token
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        res = self._decode_result(e.response)
        if self.auto_retry:
            if res.code in ('failure.operation.requestTooFast'):
                if 'retry_times' not in kwargs:
                    kwargs['retry_times'] = self.retry_times
                if kwargs['retry_times']:
                    kwargs['retry_times'] -= 1
                    time.sleep(random.randint(10, 20))
                    return func(*args, **kwargs)
        else:
            raise DingTalkClientException(errcode=res.code,
                                          errmsg=res.message,
                                          request=e.request,
                                          response=e.response)
