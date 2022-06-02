import logging
import random
import time

from dingtalk.client import AppKeyClient as _Client

logger = logging.getLogger(__name__)


class AppKeyClient(_Client):

    def __init__(self, *args, agent_id: int, retry_times: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent_id = agent_id
        self.retry_times = 3

    def _handle_request_except(self, e, func, *args, **kwargs):
        if e.errcode in (90005, 90006, 90007, 90008) and self.auto_retry:
            if 'retry_times' not in kwargs:
                kwargs['retry_times'] = self.retry_times
            if kwargs['retry_times']:
                kwargs['retry_times'] -= 1
                time.sleep(random.randint(10, 20))
                return func(*args, **kwargs)
        super()._handle_request_except(e, func, *args, **kwargs)
