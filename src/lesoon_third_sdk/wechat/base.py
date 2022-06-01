from lesoon_common import current_app
from lesoon_common.exceptions import ConfigError
from wechatpy.client import WeChatClient


class Wechat:
    # 此属性不作使用，只作展示使用
    _CONFIG = {'WECHAT': {'APP_ID': '', 'SECRET': ''}}

    @classmethod
    def get_app_id(cls):
        return cls._get_config()['APP_ID']

    @classmethod
    def _get_config(cls):
        config = current_app.config.get('WECHAT')
        if not config:
            raise ConfigError('无法找到配置:WECHAT')
        cls._CONFIG['WECHAT'] = config
        return config

    @classmethod
    def create_client(cls) -> WeChatClient:
        config = cls._get_config()
        return WeChatClient(appid=config['APP_ID'], secret=config['SECRET'])
