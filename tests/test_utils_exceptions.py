import pytest
import httpx

from judge0_client.utils.exceptions import raise_for_status, Judge0Error


def test_raise_for_status_with_json_body():
    req = httpx.Request("GET", "https://example.com/test")
    resp = httpx.Response(400, json={"error": "Bad things"}, request=req)
    with pytest.raises(Judge0Error) as ei:
        raise_for_status(resp)
    msg = str(ei.value)
    assert "HTTP 400" in msg
    assert "Bad things" in msg


def test_raise_for_status_with_text_body():
    req = httpx.Request("POST", "https://example.com/submit")
    resp = httpx.Response(500, content=b"Internal Error", request=req)
    with pytest.raises(Judge0Error) as ei:
        raise_for_status(resp)
    msg = str(ei.value)
    assert "HTTP 500" in msg
    assert "Internal Error" in msg
