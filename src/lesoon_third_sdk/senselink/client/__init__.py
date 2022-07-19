from .api import AttendanceApi
from .api import EventApi
from .base import BaseSenseLinkClient


class SenseLinkClient(BaseSenseLinkClient):
    attendance = AttendanceApi()
    event = EventApi()
