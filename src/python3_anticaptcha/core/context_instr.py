__all__ = ("SIOContextManager", "AIOContextManager")


class SIOContextManager:

    # Context methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True


class AIOContextManager:

    # Context methods
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True
