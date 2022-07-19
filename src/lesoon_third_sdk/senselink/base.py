import typing as t

from flask import Flask
from lesoon_common.exceptions import ConfigError

from lesoon_third_sdk.senselink.client import SenseLinkClient


class SenseLink:
    # 此属性不作使用，只作展示使用
    _CONFIG = {'APP_KEY': '', 'APP_SECRET': ''}

    def __init__(self, app: Flask = None, config: dict = None):
        self.config: t.Dict[str, t.Any] = config or {}
        if app:
            self.init_app(app)
        if not self.config:
            raise ConfigError('缺乏启动配置')

    def init_app(self, app: Flask):
        self.config = app.config.get('SENSELINK', {})

    def create_client(self) -> SenseLinkClient:
        return SenseLinkClient(app_key=self.config['APP_KEY'],
                               app_secret=self.config['APP_SECRET'])
