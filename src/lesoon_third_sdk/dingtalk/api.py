import base64
import datetime
import hashlib
import hmac
import time
import typing as t

from dingtalk.client.api.attendance import Attendance
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
        """
        根据sns临时授权码获取用户信息
        https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.sns.getuserinfo_bycode
        Args:
            tmp_auth_code: 临时授权码

        """
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
        """
        根据手机号查询专属帐号用户
        https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.v2.user.getbymobile
        Args:
            mobile: 手机号

        """
        return self._post('/topapi/v2/user/getbymobile', {'mobile': mobile})


class EmployeermApi(Employeerm):

    def list_v2(self, userid_list, field_filter_list=()):
        """
        批量获取员工花名册字段信息
        智能人事业务，企业/ISV根据员工id批量访问员工花名册信息
        https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.smartwork.hrm.employee.v2.list
        Args:
            userid_list: 员工id列表
            field_filter_list: 需要获取的花名册字段信息

        Returns:

        """
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        if isinstance(field_filter_list, (list, tuple, set)):
            field_filter_list = ','.join(map(to_text, field_filter_list))
        data = {'userid_list': userid_list, 'agentid': self._client.agent_id}
        if field_filter_list:
            data['field_filter_list'] = field_filter_list
        return self._post('/topapi/smartwork/hrm/employee/v2/list', data)


class AttendanceApi(Attendance):

    def get_update_data(self, userid: str,
                        work_date: t.Union[str, datetime.datetime]):
        """
        获取用户考勤数据
        https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.attendance.getupdatedata
        Args:
            userid: 钉钉用户ID
            work_date: 日期

        """
        if isinstance(work_date, datetime.datetime):
            work_date = work_date.strftime(self.DATE_TIME_FORMAT)

        return self._post('/topapi/attendance/getupdatedata', {
            'work_date': work_date,
            'userid': userid
        })

    def list_vacation_type(self, op_userid: str, vacation_source: str = 'all'):
        """
        获取假期类型
        https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.attendance.vacation.type.list
        Args:
            op_userid: 当前企业内拥有“OA审批”应用权限的管理员的userid
            vacation_source: 假期来源

        """
        return self._post('/topapi/attendance/vacation/type/list', {
            'op_userid': op_userid,
            'vacation_source': vacation_source
        })
