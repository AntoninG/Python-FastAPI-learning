"""
Defines case-specific HTTP Exceptions
"""
from typing import Any

from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        headers_copy = headers
        if isinstance(headers_copy, dict):
            headers_copy = headers.copy()
            headers_copy.update({"WWW-Authenticate": "Bearer"})

        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers=headers_copy)
