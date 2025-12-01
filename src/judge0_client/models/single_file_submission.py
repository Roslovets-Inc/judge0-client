from typing import Self, Mapping
from pydantic import BaseModel, Field
from .base_submission import BaseSubmission
from ..utils.base64_utils import base64_encode
from ..utils.zip_utils import create_encoded_zip


class SingleFileSubmission(BaseSubmission, BaseModel):
    """Request model for creating a single-file submission in Judge0."""

    source_code: str = Field(description="Program’s source code")
    language_id: int = Field(description="Programming language ID")
    additional_files: Mapping[str, str | bytes] | None = Field(
        default=None,
        description="Additional files that should be available alongside the source code (encoded zip)"
    )

    def encode_to_base64(self) -> Self:
        return self.model_copy(update={
            "source_code": base64_encode(self.source_code),
            "stdin": base64_encode(self.stdin) if self.stdin else self.stdin,
            "expected_output": base64_encode(self.expected_output) if self.expected_output else self.expected_output,
            "additional_files": create_encoded_zip(self.additional_files) if self.additional_files else None
        })
