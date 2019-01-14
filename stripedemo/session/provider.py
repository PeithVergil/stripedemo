from .storage import DatabaseSession


class SessionProvider:

    def __init__(self, main):
        self.store = DatabaseSession()
        self.main = main

    async def set(self, key, val, ttl=None):
        # Run blocking call on a separate thread.
        return await self.main.run(self.store.set, key, val, ttl)

    async def get(self, key, default=None):
        # Run blocking call on a separate thread.
        return await self.main.run(self.store.get, key, default)

    async def delete(self, key):
        # Run blocking call on a separate thread.
        return await self.main.run(self.store.delete, key)

    async def exists(self, key):
        # Run blocking call on a separate thread.
        return await self.main.run(self.store.exists, key)
