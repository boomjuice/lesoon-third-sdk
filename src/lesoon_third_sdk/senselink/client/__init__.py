from .api import AttendanceApi
from .api import CommonApi
from .api import EventApi
from .base import BaseSenseLinkClient


class SenseLinkClient(BaseSenseLinkClient):
    common = CommonApi()
    attendance = AttendanceApi()
    event = EventApi()
