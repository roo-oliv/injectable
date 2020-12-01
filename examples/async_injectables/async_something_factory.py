import asyncio

from injectable import injectable_factory


@injectable_factory(qualifier="Something")
async def async_something_factory():
    await asyncio.sleep(1)
    print("async_something_factory for 'Something' awaited and returned")
    return type("Something", (object,), {})()
