from typing import Protocol, Optional

import redis


class Backend(Protocol):
    def get(self, key: str) -> Optional[bytes]: ...
    def set(self, key: str, value: bytes) -> None: ...


class Storage:
    def __init__(self, backend: Backend):
        self.backend = backend

    def get(self, key: str) -> Optional[bytes]:
        return self.backend.get(key)

    def set(self, key: str, value: bytes) -> None:
        self.backend.set(key, value)


if __name__ == '__main__':
    backend = redis.Redis()
    storage = Storage(backend)
    storage.set('id::1', b'42')
    first = storage.get('id::1')
