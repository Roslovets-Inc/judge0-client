# Judge0 Client

Asynchronous client for the Judge0 API, implemented with httpx and Pydantic.

Features:
- create submissions with optional waiting (`wait=true/false`)
- fetch result by `token`
- batch fetch results for multiple tokens
- automatic base64 encoding/decoding for string fields
- informative HTTP error handling

Install (local):
```
pip install -e .
```

Quick start (async):

```python
import asyncio
from judge0_client import Judge0Client, SingleFileSubmission


async def main() -> None:
    # Language 71 = Python 3 (for most Judge0 instances)
    req = SingleFileSubmission(
        language_id=71,
        source_code='print("Hello, Judge0!")',
    )

    async with Judge0Client(base_url="https://judge0.ce.pdn.ac.lk") as client:
        # Option 1: wait for result right away
        result = await client.create_submission(req, wait=True)
        print("STDOUT:", result.stdout)

        # Option 2: get token first and poll later
        created = await client.create_submission(req, wait=False)
        detail = await client.get_submission(created.token)
        print("STATUS:", detail.status.description)


if __name__ == "__main__":
    asyncio.run(main())
```

Client parameters:
- `base_url` — base URL of your Judge0 instance (without trailing `/`).
- `api_key` — optional token (e.g., for proxies/gateways). Added to header `X-Auth-Token`.
- `headers` — additional HTTP headers.
- `timeout` — httpx client timeout.
- `base64_encoded` — when `True` (default), the client sends requests with `base64_encoded=true` and automatically encodes/decodes string fields (`source_code`, `stdin`, `expected_output`, `stdout`, `stderr`, `compile_output`, `message`).
- `default_wait` — default value for `wait` in `create_submission`.

Models:
- `SubmissionRequest` — data for creating a submission.
- `SubmissionResponse` — creation response without waiting (contains `token`).
- `SubmissionDetail` — detailed execution result (stdout, stderr, status, etc.).
- `SubmissionStatus` — execution status (id, description).

Notes:
- Limit fields (`cpu_time_limit`, `memory_limit`) and other options are supported if available on your Judge0 instance.
- For batch retrieval use `get_submissions(tokens=[...])`.
