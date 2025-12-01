from typing import Self, Literal, Mapping
from pydantic import BaseModel, Field
from .base_submission import BaseSubmission
from ..utils.base64_utils import base64_encode
from ..utils.zip_utils import create_encoded_zip


class MultiFileSubmission(BaseSubmission, BaseModel):
    """Request model for creating a multi-file submission in Judge0."""

    language_id: Literal[89] = Field(default=89, description="Programming language ID")
    additional_files: Mapping[str, str | bytes] = Field(
        description="Scripts to run and compile and additional files"
    )

    def encode_to_base64(self) -> Self:
        if "run" not in self.additional_files:
            raise ValueError("run script should be present in additional files")
        return self.model_copy(update={
            "stdin": base64_encode(self.stdin) if self.stdin else self.stdin,
            "expected_output": base64_encode(self.expected_output) if self.expected_output else self.expected_output,
            "additional_files": create_encoded_zip(self.additional_files)
        })
