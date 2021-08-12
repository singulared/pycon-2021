from dataclasses import dataclass
from typing import (Protocol, Optional, Dict, TypeVar, Generic, Union,
                    TYPE_CHECKING, cast)
import redis
import pickle


T = TypeVar('T')


class Backend(Protocol[T]):
    def get(self, key: str) -> Optional[T]: ...
    def set(self, key: str, value: T) -> None: ...


class RedisBackend(Backend[T]):
    def __init__(self) -> None:
        self.redis = redis.Redis()

    def get(self, key: str) -> Optional[T]:
        value = self.redis.get(key)
        if value:
            unpickled_value = pickle.loads(value)
            if TYPE_CHECKING:
                reveal_type(value)
                reveal_type(unpickled_value)
            return cast(T, unpickled_value)
        # 10.py:25: error: Return value expected
        return None

    def set(self, key: str, value: T) -> None:
        self.redis.set(key, pickle.dumps(value))


class InMemoryBackend(Backend[T]):
    def __init__(self) -> None:
        self.backend: Dict[str, T] = dict()

    def get(self, key: str) -> Optional[T]:
        return self.backend.get(key)

    def set(self, key: str, value: T) -> None:
        self.backend[key] = value


class Storage(Generic[T]):
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
    #  backend: Backend[Union[User, Comment]] = InMemoryBackend()
    backend: Backend[Union[User, Comment]] = RedisBackend()
    storage = Storage(backend)
    user = User(1, 'Алексей', 'Мозолев')
    comment = Comment(1, 'Вы некомпетентны')
    storage.set('id::1', user)
    storage.set('id::2', comment)
    value = storage.get('id::1')
    if TYPE_CHECKING:
        reveal_type(value)
