"""
AI Native 研发平台 - Password Utilities
"""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    使用 SHA-256 + salt 哈希密码
    """
    # 生成随机 salt
    salt = secrets.token_hex(16)

    # 使用 PBKDF2 进行密码哈希
    iterations = 100000
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    ).hex()

    # 返回格式: salt$hash$iterations
    return f"{salt}${password_hash}${iterations}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    try:
        parts = hashed_password.split('$')
        if len(parts) != 3:
            return False

        salt, stored_hash, iterations_str = parts
        iterations = int(iterations_str)

        # 使用相同的 salt 和 iterations 计算哈希
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations
        ).hex()

        return secrets.compare_digest(computed_hash, stored_hash)
    except Exception:
        return False
