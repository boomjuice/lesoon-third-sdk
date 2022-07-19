from wechatpy.client.base import BaseWeChatAPI


class WechatOAuth2(BaseWeChatAPI):
    API_BASE_URL = 'https://api.weixin.qq.com/'

    def get_user_access_token(self,
                              code: str,
                              grant_type: str = 'authorization_code'):
        """
        通过 code 获取access_token的接口。

        Args:
            code: 临时授权码
            grant_type: authorization_code

        """
        params = {
            'appid': self._client.appid,
            'secret': self._client.secret,
            'code': code,
            'grant_type': grant_type
        }
        return self._get('sns/oauth2/access_token', params=params)

    def get_user_info(self,
                      access_token: str,
                      openid: str,
                      lang: str = 'zh_CN'):
        """
        此接口用于获取用户个人信息。开发者可通过 OpenID 来获取用户基本信息。
        特别需要注意的是，如果开发者拥有多个移动应用、网站应用和公众帐号，
        可通过获取用户基本信息中的 unionid 来区分用户的唯一性，
        因为只要是同一个微信开放平台帐号下的移动应用、网站应用和公众帐号，用户的 unionid 是唯一的。
        换句话说，同一用户，对同一个微信开放平台下的不同应用，unionid是相同的。
        Args:
            access_token:  调用凭证
            openid: 普通用户的标识，对当前开发者帐号唯一
            lang: 国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语，默认为en

        Returns:

        """
        params = {'access_token': access_token, 'openid': openid}
        return self._get('sns/userinfo', params=params)
