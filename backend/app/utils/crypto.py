"""
AI Native 研发平台 - Crypto Utility

用于敏感信息的加密和解密
"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as PBKDF2
from app.config import Config


class CryptoUtil:
    """加密工具类"""

    _fernet = None

    @classmethod
    def _get_fernet(cls):
        """获取Fernet实例（单例模式）"""
        if cls._fernet is None:
            # 从配置获取密钥，如果没有则生成新的
            secret_key = getattr(Config, 'SECRET_KEY', None)
            if not secret_key:
                secret_key = os.urandom(32)

            # 使用PBKDF2从密钥派生加密密钥
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'ai_agent_hub_salt',  # 固定盐值，实际应用中应存储
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode() if isinstance(secret_key, str) else secret_key))
            cls._fernet = Fernet(key)
        return cls._fernet

    @classmethod
    def encrypt(cls, plaintext: str) -> str:
        """
        加密文本

        Args:
            plaintext: 明文

        Returns:
            加密后的base64字符串
        """
        if not plaintext:
            return None
        fernet = cls._get_fernet()
        encrypted = fernet.encrypt(plaintext.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')

    @classmethod
    def decrypt(cls, ciphertext: str) -> str:
        """
        解密文本

        Args:
            ciphertext: 加密的base64字符串

        Returns:
            解密后的明文
        """
        if not ciphertext:
            return None
        try:
            fernet = cls._get_fernet()
            encrypted = base64.urlsafe_b64decode(ciphertext.encode('utf-8'))
            decrypted = fernet.decrypt(encrypted)
            return decrypted.decode('utf-8')
        except Exception:
            # 解密失败返回None
            return None

    @classmethod
    def mask_token(cls, token: str, show_chars: int = 4) -> str:
        """
        遮罩token显示（只显示前几个字符）

        Args:
            token: 原始token
            show_chars: 显示的字符数

        Returns:
            遮罩后的token
        """
        if not token:
            return None
        if len(token) <= show_chars:
            return token
        return token[:show_chars] + '...' + '*' * (len(token) - show_chars)

    @classmethod
    def is_encrypted(cls, value: str) -> bool:
        """
        检查值是否已被加密

        Args:
            value: 待检查的值

        Returns:
            是否为加密值
        """
        if not value:
            return False
        try:
            # 尝试base64解码
            decoded = base64.urlsafe_b64decode(value.encode('utf-8'))
            # 加密后的数据应该有一定的长度
            return len(decoded) > 32
        except Exception:
            return False
