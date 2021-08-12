import redis


class Storage:
    def __init__(self, backend):
        self.backend = backend

    def get(self, key):
        return self.backend.get(key)

    def set(self, key, value):
        self.backend.set(key, value)


if __name__ == '__main__':
    backend = redis.Redis()
    storage = Storage(backend)
    storage.set('id::1', 42)
    first = storage.get('id::1')
