import typing as t

from flask import Flask
from lesoon_common import current_app
from lesoon_common.exceptions import ConfigError
from wechatpy.client import WeChatClient


class Wechat:
    # 此属性不作使用，只作展示使用
    _CONFIG = {'APP_ID': '', 'SECRET': ''}

    def __init__(self, app: Flask = None, config: dict = None):
        self.config: t.Dict[str, t.Any] = config or {}
        if app:
            self.init_app(app)
        if not self.config:
            raise ConfigError('缺乏启动配置')

    def init_app(self, app: Flask):
        self.config = current_app.config.get('WECHAT')

    def create_client(self) -> WeChatClient:
        return WeChatClient(appid=self.config['APP_ID'],
                            secret=self.config['SECRET'])
