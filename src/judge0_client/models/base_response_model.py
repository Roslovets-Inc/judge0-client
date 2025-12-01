from typing import Self
from pydantic import BaseModel
import httpx


class BaseResponseModel(BaseModel):
    """Detailed information about submission execution."""

    @classmethod
    def from_response(cls, resp: httpx.Response) -> Self:
        return cls.model_validate(resp.json())
