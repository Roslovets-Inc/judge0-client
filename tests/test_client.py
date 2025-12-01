import json
import base64
import asyncio
import httpx

from judge0_client import Judge0Client, SingleFileSubmission, SubmissionStatusId


def _default_headers(auth_header: str, token: str) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        auth_header: token,
    }


def test_create_submission_sends_expected_json_and_headers():
    # Prepare submission
    submission = SingleFileSubmission(
        source_code="print('Hello 🐍')",
        language_id=71,
        stdin="input",
        expected_output="output",
        additional_files={
            "a.txt": "A",
            "bin.dat": b"\x00\x01",
        },
    )
    expected_body = submission.to_body()

    # Transport handler that asserts request and returns token
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/submissions"
        # base64 flag must be true
        assert request.url.params.get("base64_encoded") == "true"

        # Headers must contain our custom auth header and defaults
        assert request.headers.get("Accept") == "application/json"
        assert request.headers.get("Content-Type") == "application/json"
        assert request.headers.get("X-API-Key") == "secret"

        # JSON body must match encoded submission
        got_body = json.loads(request.content)
        assert got_body == expected_body

        return httpx.Response(201, json={"token": "abc123"}, request=request)

    transport = httpx.MockTransport(handler)

    client = Judge0Client(
        base_url="https://api.example.com",
        auth_header="X-API-Key",
        auth_token="secret",
    )

    async def run():
        # Bypass open(); directly set mocked AsyncClient and close via aclose()
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            timeout=client.timeout,
            headers=_default_headers("X-API-Key", "secret"),
            transport=transport,
        )
        try:
            resp = await client.create_submission(submission)
            assert resp.token == "abc123"
        finally:
            await client.aclose()

    asyncio.run(run())


def test_get_submission_decodes_base64_fields():
    token = "tok-42"
    raw_detail = {
        "token": token,
        "status": {"id": SubmissionStatusId.ACCEPTED, "description": "Accepted"},
        "stdout": base64.b64encode("OK".encode()).decode(),
        "stderr": None,
        "compile_output": None,
        "message": base64.b64encode("All good".encode()).decode(),
        "time": 0.123,
        "memory": 12345,
        "exit_code": 0,
        "language_id": 71,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == f"/submissions/{token}"
        assert request.url.params.get("base64_encoded") == "true"
        assert request.headers.get("X-Auth-Token") == "tkn"
        return httpx.Response(200, json=raw_detail, request=request)

    transport = httpx.MockTransport(handler)

    client = Judge0Client(
        base_url="https://api.example.com",
        auth_header="X-Auth-Token",
        auth_token="tkn",
    )

    async def run():
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            timeout=client.timeout,
            headers=_default_headers("X-Auth-Token", "tkn"),
            transport=transport,
        )
        try:
            detail = await client.get_submission(token)

            # Base64 fields must be decoded by client
            assert detail.token == token
            assert detail.status.id == SubmissionStatusId.ACCEPTED
            assert detail.status.description == "Accepted"
            assert detail.stdout == "OK"
            assert detail.message == "All good"
            assert detail.time == 0.123
            assert detail.memory == 12345
            assert detail.exit_code == 0
            assert detail.language_id == 71
        finally:
            await client.aclose()

    asyncio.run(run())


def test_get_workers_returns_models_list():
    workers_payload = [
        {
            "queue": "q-1",
            "size": 2,
            "available": 3,
            "idle": 2,
            "working": 1,
            "paused": 0,
            "failed": 0,
        },
        {
            "queue": "q-2",
            "size": 0,
            "available": 5,
            "idle": 5,
            "working": 0,
            "paused": 0,
            "failed": 0,
        },
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/workers"
        assert request.headers.get("X-Auth-Token") == "auth"
        return httpx.Response(200, json=workers_payload, request=request)

    transport = httpx.MockTransport(handler)

    client = Judge0Client(
        base_url="https://api.example.com",
        auth_header="X-Auth-Token",
        auth_token="auth",
    )

    async def run():
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            timeout=client.timeout,
            headers=_default_headers("X-Auth-Token", "auth"),
            transport=transport,
        )
        try:
            workers = await client.get_workers()
            assert isinstance(workers, list)
            assert len(workers) == 2
            assert workers[0].queue == "q-1"
            assert workers[0].size == 2
            assert workers[1].queue == "q-2"
            assert workers[1].idle == 5
        finally:
            await client.aclose()

    asyncio.run(run())


def test_get_about_returns_model():
    about_payload = {
        "version": "v1.2.3",
        "homepage": "https://judge0.example.com",
        "source_code": "https://github.com/org/repo",
        "maintainer": "Team",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/about"
        assert request.headers.get("X-API-Key") == "k"
        return httpx.Response(200, json=about_payload, request=request)

    transport = httpx.MockTransport(handler)

    client = Judge0Client(
        base_url="https://api.example.com",
        auth_header="X-API-Key",
        auth_token="k",
    )

    async def run():
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            timeout=client.timeout,
            headers=_default_headers("X-API-Key", "k"),
            transport=transport,
        )
        try:
            about = await client.get_about()
            assert about.version == "v1.2.3"
            assert about.homepage == "https://judge0.example.com"
            assert about.source_code == "https://github.com/org/repo"
            assert about.maintainer == "Team"
        finally:
            await client.aclose()

    asyncio.run(run())


def test_get_isolate_returns_text():
    text = "isolate 1.9.0"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/isolate"
        assert request.headers.get("X-Auth-Token") == "authz"
        return httpx.Response(200, text=text, request=request)

    transport = httpx.MockTransport(handler)

    client = Judge0Client(
        base_url="https://api.example.com",
        auth_header="X-Auth-Token",
        auth_token="authz",
    )

    async def run():
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            timeout=client.timeout,
            headers=_default_headers("X-Auth-Token", "authz"),
            transport=transport,
        )
        try:
            got = await client.get_isolate()
            assert got == text
        finally:
            await client.aclose()

    asyncio.run(run())


def test_get_license_returns_text():
    license_text = "MIT License\n\nCopyright (c) ..."

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/license"
        assert request.headers.get("X-API-Key") == "sk"
        return httpx.Response(200, text=license_text, request=request)

    transport = httpx.MockTransport(handler)

    client = Judge0Client(
        base_url="https://api.example.com",
        auth_header="X-API-Key",
        auth_token="sk",
    )

    async def run():
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            timeout=client.timeout,
            headers=_default_headers("X-API-Key", "sk"),
            transport=transport,
        )
        try:
            got = await client.get_license()
            assert got == license_text
        finally:
            await client.aclose()

    asyncio.run(run())
