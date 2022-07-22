"""
Requests bodies accepted by the app
"""

from password_validator import PasswordValidator
from pydantic import BaseModel, EmailStr, constr, validator


# pylint: disable=too-few-public-methods
class CreateArticleRequest(BaseModel):
    title: constr(strip_whitespace=True, min_length=2, max_length=150)
    content: constr(strip_whitespace=True, min_length=10, max_length=1000)


class CreateUserRequest(BaseModel):
    """
    HTTP body request expected to create a user.
    Property email is expected to be between 8 and 30 chars, with digits, upper
    and lower case letters, symbols and no spaces
    """
    name: str
    email: EmailStr
    password: str

    @validator('password')
    def password_must_be_valid(cls, value):  # pylint: disable=no-self-argument
        password_schema = PasswordValidator() \
            .min(8) \
            .max(30) \
            .has().digits() \
            .has().letters() \
            .has().symbols() \
            .has().uppercase() \
            .has().lowercase() \
            .has().no().spaces()

        if password_schema.validate(value):
            return value

        raise ValueError(
            'must be a valid password (8 to 30 chars, with digits, upper and '
            'lower case, symbols and no spaces)')


class PasswordVerifyRequest(BaseModel):
    password: str
