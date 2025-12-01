# CHANGELOG


## v0.2.0 (2025-12-01)

### Features

- Add info methods
  ([`c6f42fb`](https://github.com/Roslovets-Inc/judge0-client/commit/c6f42fb5ba6050baac513c0aecdb4fc32ac866ed))


## v0.1.1 (2025-12-01)

### Bug Fixes

- Refactor move submission encoding to `to_body` method
  ([`5a23298`](https://github.com/Roslovets-Inc/judge0-client/commit/5a23298fa732b25dcabba798ce91f58601392006))

Replaces encode_to_base64 with to_body for submission models, consolidating base64 encoding logic
  into to_body. Updates client and tests to use the new method for preparing submission payloads.


## v0.1.0 (2025-12-01)

### Bug Fixes

- Add missing tests
  ([`f4e2e80`](https://github.com/Roslovets-Inc/judge0-client/commit/f4e2e801d3536e8a071b72882afd0b090b38afc5))

### Documentation

- Update readme
  ([`9b45658`](https://github.com/Roslovets-Inc/judge0-client/commit/9b4565864d60047fdc61061bc1b864e1ead9ac50))

### Features

- Create and get submission
  ([`5603912`](https://github.com/Roslovets-Inc/judge0-client/commit/5603912e6a92059a5a8dde7c236f7758911a2c77))
