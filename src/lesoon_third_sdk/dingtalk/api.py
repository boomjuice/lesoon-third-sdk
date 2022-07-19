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
from dingtalk.client.base import BaseClient
from dingtalk.core.utils import to_text


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

    def get_roster_meta(self):
        """
        调用本接口获取员工花名册的元数据，包括花名册分组、字段等。

        """
        return self._post('/topapi/smartwork/hrm/roster/meta/get',
                          data={'agentid': self._client.agent_id})

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

    def listdimission(self, userid_list=()):
        """
        批量获取员工离职信息
        根据传入的staffId列表，批量查询员工的离职信息

        Args:
            userid_list: 员工id

        """
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        return self._post('topapi/smartwork/hrm/employee/listdimission',
                          {'userid_list': userid_list})


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

        return self._post('/topapi/attendance/getupdatedata',
                          data={
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

    def get_att_columns(self):
        """
        调用本接口获取企业智能考勤报表中的列信息。
        通过获取列信息中的ID值，可以根据列的ID查询考勤智能报表中该列的统计数据，企业可以自主选择需要哪些列值来参与薪酬的计算。
        https://open-dev.dingtalk.com/apiExplorer?spm=ding_open_doc.document.0.0.37d97176mkmyxZ#/?devType=org&api=dingtalk.oapi.attendance.getattcolumns

        """
        return self._post('/topapi/attendance/getattcolumns')

    def get_column_val(self, userid: str, column_id_list: t.List[str],
                       from_date: t.Union[str, datetime.datetime],
                       to_date: t.Union[str, datetime.datetime]):
        """
        该接口用于获取钉钉智能考勤报表的列值数据，
        其中包含了一定时间段内报表某一列的所有数据，以及相关的列信息，可以供指定的ISV进行使用。

        """
        if isinstance(from_date, datetime.datetime):
            from_date = from_date.strftime(self.DATE_TIME_FORMAT)
        if isinstance(to_date, datetime.datetime):
            to_date = to_date.strftime(self.DATE_TIME_FORMAT)
        column_id_list = ','.join(column_id_list)
        return self._post('/topapi/attendance/getcolumnval',
                          data={
                              'userid': userid,
                              'column_id_list': column_id_list,
                              'from_date': from_date,
                              'to_date': to_date
                          })

    def get_leave_time_by_names(self, userid: str, leave_names: t.List[str],
                                from_date: t.Union[str, datetime.datetime],
                                to_date: t.Union[str, datetime.datetime]):
        """
        调用本接口根据假期名称和用户ID获取钉钉智能考勤报表的假期数据，
        其中包含了一定时间段内报表假期列的所有数据，由于假期列是一个动态列，因此需要根据假期名称获取数据

        """
        if isinstance(from_date, datetime.datetime):
            from_date = from_date.strftime(self.DATE_TIME_FORMAT)
        if isinstance(to_date, datetime.datetime):
            to_date = to_date.strftime(self.DATE_TIME_FORMAT)
        leave_names = ','.join(leave_names)
        return self._post('/topapi/attendance/getleavetimebynames',
                          data={
                              'userid': userid,
                              'leave_names': leave_names,
                              'from_date': from_date,
                              'to_date': to_date
                          })


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


class YiDaApi(DingTalkBaseAPI):
    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def search_form_datas(
            self,
            app_type: str,
            system_token: str,
            user_id: str,
            form_uuid: str,
            language: str = 'zh_CN',
            search_field_json: str = None,
            current_page=1,
            page_size=10,
            originator_id: str = None,
            create_from_time_gmt: t.Union[str, datetime.datetime] = None,
            create_to_time_gmt: t.Union[str, datetime.datetime] = None,
            modified_from_time_gmt: t.Union[str, datetime.datetime] = None,
            modified_to_time_gmt: t.Union[str, datetime.datetime] = None,
            dynamic_order: str = None):
        data = {
            'appType': app_type,
            'systemToken': system_token,
            'userId': user_id,
            'formUuid': form_uuid,
            'language': language,
            'currentPage': current_page,
            'pageSize': page_size,
            'dynamicOrder': dynamic_order
        }
        if search_field_json:
            data['searchFieldJson'] = search_field_json
        if originator_id:
            data['originatorId'] = originator_id

        if create_to_time_gmt:
            if isinstance(create_from_time_gmt, datetime.datetime):
                create_from_time_gmt = create_from_time_gmt.strftime(
                    self.DATE_TIME_FORMAT)
            data['createFromTimeGMT'] = create_from_time_gmt

        if create_to_time_gmt:
            if isinstance(create_to_time_gmt, datetime.datetime):
                create_to_time_gmt = create_to_time_gmt.strftime(
                    self.DATE_TIME_FORMAT)
            data['createToTimeGMT'] = create_to_time_gmt

        if modified_from_time_gmt:
            if isinstance(modified_from_time_gmt, datetime.datetime):
                modified_from_time_gmt = modified_from_time_gmt.strftime(
                    self.DATE_TIME_FORMAT)
            data['modifiedFromTimeGMT'] = modified_from_time_gmt

        if modified_to_time_gmt:
            if isinstance(modified_to_time_gmt, datetime.datetime):
                modified_to_time_gmt = modified_to_time_gmt.strftime(
                    self.DATE_TIME_FORMAT)
            data['modifiedToTimeGMT'] = modified_to_time_gmt
        return self._post('/v1.0/yida/forms/instances/search', data=data)


class OAuth2(DingTalkBaseAPI):

    def get_user_access_token(self, code: str, refresh_code: str = None):
        """
        调用本接口获取用户token
        https://open.dingtalk.com/document/orgapp-server/obtain-user-token
        Args:
            code: 授权码
            refresh_code: 刷新码

        Returns:

        """
        data = {
            'clientId': self._client.app_key,
            'clientSecret': self._client.app_secret,
            'code': code,
            'grantType': 'authorization_code',
        }
        if refresh_code:
            data['refreshToken'] = refresh_code
            data['grantType'] = 'refresh_token'

        return self._post('/v1.0/oauth2/userAccessToken', data=data)

    def get_user_contact(self, access_token: str, unionId: str = 'me'):
        """
        调用本接口获取企业用户通讯录中的个人信息。
        Args:
            access_token: 个人用户的accessToken
            unionId:用户的unionId
        Returns:

        """
        headers = {'x-acs-dingtalk-access-token': access_token}
        return self._get(f'/v1.0/contact/users/{unionId}', headers=headers)
