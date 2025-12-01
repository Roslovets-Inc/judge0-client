import base64

from judge0_client.utils.base64_utils import base64_encode, base64_decode


def test_base64_encode_roundtrip_unicode():
    original = "Hello world! 🚀"
    encoded = base64_encode(original)
    # Sanity: encoded is valid base64 ASCII
    assert isinstance(encoded, str)
    assert encoded == base64.b64encode(original.encode("utf-8")).decode("ascii")
    # decode using library util (should be inverse when there are no NULs)
    assert base64_decode(encoded) == original


def test_base64_decode_removes_null_bytes():
    # bytes with NULs inside
    raw = b"abc\x00def\x00"
    encoded = base64.b64encode(raw).decode("ascii")
    # our decoder removes NULs and decodes utf-8
    assert base64_decode(encoded) == "abcdef"
