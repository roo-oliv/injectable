import asyncio

from injectable import injectable


@injectable
class AsyncService:
    """
    Here we overwrite ``__new__`` to be async, making a call to
    ``AsyncService.__new__`` not to return an instance of ``AsyncService``
    but a coroutine instead. This is why we can declare
    ``AsyncService.__init__`` as async as Python won't automatically try
    invoking it and that's also why we need to invoke it manually inside
    the ``__new__`` method.

    Don't do this in production environments, please. This code is intended
    only to demonstrate that no matter what, the injectable framework will
    work properly.
    """

    async def __new__(cls):
        instance = super().__new__(cls)
        await instance.__init__()
        return instance

    async def __init__(self):
        await asyncio.sleep(1)
        print("AsyncService::__init__ awaited and returned")
