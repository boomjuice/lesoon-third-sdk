import datetime
import typing as t

from lesoon_third_sdk.senselink.client.api.base import SenseLinkBaseAPI


class AttendanceApi(SenseLinkBaseAPI):
    DATE_FORMAT = '%Y-%m-%d'

    def get_record(self,
                   date_from: t.Union[str, datetime.datetime],
                   date_to: t.Union[str, datetime.datetime],
                   department_id: int = None,
                   user_id: int = None,
                   status: int = None,
                   page: int = 1,
                   size: int = 20):
        """
        查询员工考勤记录，支持按员工id或部门id查询
        https://link.bi.sensetime.com/docs/105
        Args:
            date_from: 查询的开始日期， 默认是当天
            date_to: 查询的结束日期， 默认是当天
            department_id: 部门id
            user_id: 员工id
            status: 考勤状态（1:正常；2：迟到；3：早退；4：迟到早退；
                    5：工作日加班；6：节假日加班；7：缺勤；8：漏打卡；127：无状态）
            page: 页号（默认为1）
            size: 每页数据条数（默认为20）,最大100

        """

        if isinstance(date_from, datetime.datetime):
            date_from = date_from.strftime(self.DATE_FORMAT)
        if isinstance(date_to, datetime.datetime):
            date_to = date_to.strftime(self.DATE_FORMAT)

        params = {
            'dateFrom': date_from,
            'dateTo': date_to,
            'page': page,
            'size': size
        }
        if department_id:
            params['departmentId'] = department_id
        if user_id:
            params['userId'] = user_id
        if status:
            params['status'] = status
        return self._get('/api/v3/attendance/record', params=params)
