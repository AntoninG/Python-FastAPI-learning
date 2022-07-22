"""
Defines hashing utils classes to encrypt and decrypt data
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(password: str, hashed_password: str):
        return pwd_context.verify(password, hashed_password)
