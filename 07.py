from dataclasses import dataclass
from typing import Protocol, Optional, Dict, TypeVar, Generic

import redis

T = TypeVar('T')


class Backend(Protocol[T]):
    def get(self, key: str) -> Optional[T]: ...
    def set(self, key: str, value: T) -> None: ...


# class RedisBackend(Backend):
#     def __init__(self) -> None:
#         self.redis = redis.Redis()
#
#     def get(self, key: str) -> Optional[T]:
#         return self.redis.get(key)
#
#     def set(self, key: str, value: T) -> None:
#         self.redis.set(key, value)


class InMemoryBackend(Backend[T]):
    def __init__(self) -> None:
        self.backend: Dict[str, T] = dict()

    def get(self, key: str) -> Optional[T]:
        return self.backend.get(key)

    def set(self, key: str, value: T) -> None:
        self.backend[key] = value


class Storage:
    def __init__(self, backend: Backend[T]):
        self.backend = backend

    def get(self, key: str) -> Optional[T]:
        return self.backend.get(key)

    def set(self, key: str, value: T) -> None:
        self.backend.set(key, value)


@dataclass
class User:
    id: int
    first_name: str
    last_name: str


@dataclass
class Comment:
    id: int
    text: str


if __name__ == '__main__':
    # не умеет выводить тип. надо указать руками
    backend: Backend[User] = InMemoryBackend()
    storage = Storage(backend)
    user = User(1, 'Алексей', 'Мозолев')
    comment = Comment(1, 'Вы некомпетентны')
    storage.set('id::1', user)
    storage.set('id::2', comment)
