import base64
import io
import zipfile

from judge0_client.utils.zip_utils import create_encoded_zip


def test_create_encoded_zip_and_decode_back():
    files = {
        "dir/hello.txt": "Привет",
        "root.bin": b"\x00\x01\x02",
    }
    encoded = create_encoded_zip(files)
    assert isinstance(encoded, str)

    # Decode base64 and read zip to verify contents
    data = base64.b64decode(encoded)
    with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
        names = set(zf.namelist())
        assert names == {"dir/hello.txt", "root.bin"}
        assert zf.read("dir/hello.txt").decode("utf-8") == "Привет"
        assert zf.read("root.bin") == b"\x00\x01\x02"
