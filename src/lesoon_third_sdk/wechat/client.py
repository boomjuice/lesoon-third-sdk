import logging

from dingtalk.core.utils import json_loads
from wechatpy.client import WeChatClient as _Client

from lesoon_third_sdk.wechat.api import WechatOAuth2

logger = logging.getLogger(__name__)


class WeChatClient(_Client):
    oauth2 = WechatOAuth2()

    def _decode_result(self, res):
        try:
            result = json_loads(res.content.decode('utf-8', 'ignore'),
                                strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            logger.debug('Can not decode response as JSON', exc_info=True)
            return res
        return result
