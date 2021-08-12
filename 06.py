from dataclasses import dataclass
from typing import Protocol, Optional, Dict

import redis


class Backend(Protocol):
    def get(self, key: str) -> Optional[bytes]: ...
    def set(self, key: str, value: bytes) -> None: ...


class RedisBackend(Backend):
    def __init__(self) -> None:
        self.redis = redis.Redis()

    def get(self, key: str) -> Optional[bytes]:
        return self.redis.get(key)

    def set(self, key: str, value: bytes) -> None:
        self.redis.set(key, value)


class InMemoryBackend(Backend):
    def __init__(self) -> None:
        self.backend: Dict[str, bytes] = dict()

    def get(self, key: str) -> Optional[bytes]:
        return self.backend.get(key)

    def set(self, key: str, value: bytes) -> None:
        self.backend[key] = value


class Storage:
    def __init__(self, backend: Backend):
        self.backend = backend

    def get(self, key: str) -> Optional[bytes]:
        return self.backend.get(key)

    def set(self, key: str, value: bytes) -> None:
        self.backend.set(key, value)


@dataclass
class User:
    id: int
    first_name: str
    last_name: str


if __name__ == '__main__':
    backend = InMemoryBackend()
    storage = Storage(backend)
    user = User(1, 'Алексей', 'Мозолев')
    storage.set('id::1', user)
    first = storage.get('id::1')
