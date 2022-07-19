import base64
import hashlib
import struct
import time
import typing as t

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes
from dingtalk.storage import BaseStorage
from flask import Flask
from lesoon_common import current_app
from lesoon_common.exceptions import ConfigError
from lesoon_common.utils.base import random_alpha_numeric

from lesoon_third_sdk.dingtalk.client import AppKeyClient
from lesoon_third_sdk.dingtalk.client import NewAppKeyClient


class DingtalkCallbackCrypto:

    def __init__(self, app_key: str, token: str, aes_key: str):
        self.app_key = app_key
        self.token = token
        self.aes_key = base64.b64decode(aes_key + '=')

    def generate_signature(self, nonce: str, timestamp: str, ciphertext: str):
        """
        生成调用签名
        Args:
            nonce: 随机字符串
            timestamp: 时间戳
            ciphertext: 密文

        Returns:
            signature: str
            signature: 消息签名

        """
        sign_list = ''.join(sorted([nonce, timestamp, self.token, ciphertext]))
        return hashlib.sha1(sign_list.encode()).hexdigest()

    def decrypt(self, msg_signature: str, timestamp: str, nonce: str,
                ciphertext: str):
        """
        解密钉钉消息
        Args:
            msg_signature: 消息签名
            timestamp: 时间戳
            nonce: 随机字符串
            ciphertext: 加密消息

        Returns:
            msg: 解密数据
        """
        sign = self.generate_signature(nonce, timestamp, ciphertext)
        if sign != msg_signature:
            raise ValueError('钉钉事件回调签名验证失败')
        ciphertext = base64.b64decode(ciphertext)
        cipher = Cipher(algorithm=algorithms.AES(self.aes_key),
                        mode=modes.CBC(self.aes_key[:16]))

        decryptor = cipher.decryptor()
        decrypted_input = decryptor.update(ciphertext) + decryptor.finalize()
        pad = int(decrypted_input[-1])
        if pad > 32:
            raise ValueError('Input is not padded or padding is corrupt')
        decrypted_input = decrypted_input[:-pad]
        msg_len = struct.unpack('!i', decrypted_input[16:20])[0]

        if decrypted_input[(20 + msg_len):].decode() != self.app_key:
            raise ValueError('钉钉应用密钥不匹配!')

        return decrypted_input[20:(20 + msg_len)].decode()

    def encrypt(self, msg: str):
        """
        加密返回结果.
        具体加密方法见 https://open.dingtalk.com/document/orgapp-server/callback-overview
        Args:
            msg: 返回结果

        """
        msg_len = struct.pack('!l', len(msg))
        content = ''.join(
            (random_alpha_numeric(16), msg, self.app_key)).encode()
        content = content[:16] + msg_len + content[16:]
        cipher = Cipher(algorithm=algorithms.AES(self.aes_key),
                        mode=modes.CBC(self.aes_key[:16]))
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_input = padder.update(content) + padder.finalize()

        encryptor = cipher.encryptor()
        encrypted_input = encryptor.update(padded_input) + encryptor.finalize()
        return base64.encodebytes(encrypted_input).decode()

    def generate_response(self, msg: str):
        encrypted_msg = self.encrypt(msg)
        timestamp = str(int(time.time()))
        nonce = random_alpha_numeric(16)
        signature = self.generate_signature(nonce=nonce,
                                            timestamp=timestamp,
                                            ciphertext=encrypted_msg)
        return {
            'msg_signature': signature,
            'encrypt': encrypted_msg,
            'timeStamp': timestamp,
            'nonce': nonce
        }


class DingTalk:
    # 此属性不作使用，只作展示使用
    _CONFIG = {
        'CORP_ID': '',
        'APP_KEY': '',
        'APP_SECRET': '',
        'AGENT_ID': '',
        'CALLBACK': {
            'TOKEN': '',
            'AES_KEY': ''
        },
        # 自定义参数
        'EXTRA': {}
    }

    def __init__(self,
                 app: Flask = None,
                 config: dict = None,
                 storage: BaseStorage = None):
        self.config: t.Dict[str, t.Any] = config or {}
        self.storage = storage
        if app:
            self.init_app(app)
        if not self.config:
            raise ConfigError('缺乏启动配置')

    def init_app(self, app: Flask):
        self.config = app.config.get('DINGTALK', {})

    @property
    def extra_config(self):
        return self.config['EXTRA']

    def create_client(self) -> AppKeyClient:
        return AppKeyClient(
            corp_id=self.config['CORP_ID'],
            app_key=self.config['APP_KEY'],
            app_secret=self.config['APP_SECRET'],
            agent_id=self.config['AGENT_ID'],
            storage=self.storage,
        )

    def create_new_client(self) -> NewAppKeyClient:
        return NewAppKeyClient(
            corp_id=self.config['CORP_ID'],
            app_key=self.config['APP_KEY'],
            app_secret=self.config['APP_SECRET'],
            agent_id=self.config['AGENT_ID'],
            storage=self.storage,
        )

    def create_callback_crypto(self) -> DingtalkCallbackCrypto:
        app_key = self.config['APP_KEY']
        callback_config = self.config.get('CALLBACK')
        if not callback_config:
            raise ConfigError('配置文件中无法找到钉钉事件订阅的配置！')
        token = callback_config['TOKEN']
        aes_key = callback_config['AES_KEY']
        return DingtalkCallbackCrypto(app_key=app_key,
                                      token=token,
                                      aes_key=aes_key)
