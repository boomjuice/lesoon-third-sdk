import datetime
import typing as t

from lesoon_third_sdk.senselink.client.api.base import SenseLinkBaseAPI


class EventApi(SenseLinkBaseAPI):
    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def list_identity_records(self,
                              date_time_from: t.Union[str, datetime.datetime],
                              date_time_to: t.Union[str, datetime.datetime],
                              order: int = 0,
                              page: int = 1,
                              size: int = 20):
        """
        查询某段时间内后台接收到的识别记录
        https://link.bi.sensetime.com/docs/29
        Args:
            date_time_from: 查询起始时间，默认为当日零点，精确到秒
            date_time_to: 查询结束时间，默认为当日23:59:59，精确到秒
            order: 排序方式，0-按记录入库时间由近到远返回，1-按识别记录id升序
            page: 页号（默认为1）
            size: 每页数据条数（默认为20）,最大100

        """

        if isinstance(date_time_from, datetime.datetime):
            date_time_from = date_time_from.strftime(self.DATE_TIME_FORMAT)
        if isinstance(date_time_to, datetime.datetime):
            date_time_to = date_time_to.strftime(self.DATE_TIME_FORMAT)

        params = {
            'date_time_from': date_time_from,
            'date_time_to': date_time_to,
            'order': order,
            'page': page,
            'size': size
        }
        return self._get('/api/v3/record/list', params=params)
