"""
In this example you'll see how to injection of coroutines work in both possible
scenarios: (i) when the autowired function is not async; and (ii) when the autowired
function is async.

We declare a class ``AsyncService`` and a factory for the ``Something`` qualifier, both
producing coroutines in different ways.

In our ``AsyncInjectables`` example class ask for ``AsyncService`` and ``Something`` to
be injected in our ``__init__`` method, which isn't async.

You can see at the ``AsyncInjectables::__init__`` that neither of the async functions,
``AsyncService::__init__`` and ``async_something_factory``, are awaited and we end up
setting our instance members with coroutines and not with the actual classes we asked
for.

Now, in the ``AsyncInjectables::run`` method we invoke and await the async method
``AsyncInjectables::async_method`` in which we also asked for `AsyncService`` and
``Something`` to be injected. Since ``AsyncInjectables::async_method`` is an actual
coroutine function then the async functions, ``AsyncService::__init__`` and
``async_something_factory``, are both awaited and now we end up with the actual
classes we asked for set in our instance members.

.. note::

    All injection coroutines are asynchronously gathered and awaited at the same time
    regardless of parameters order or type.
"""
# sphinx-start
import asyncio

from examples import Example
from examples.async_injectables.async_service import AsyncService
from injectable import autowired, Autowired, load_injection_container


class AsyncInjectables(Example):
    @autowired
    def __init__(
        self,
        async_service: Autowired(AsyncService),
        something_async: Autowired("Something"),
    ):
        self.async_service = async_service
        self.something_async = something_async

    @autowired
    async def async_method(
        self,
        async_service: Autowired(AsyncService),
        something_async: Autowired("Something"),
    ):
        self.async_service = async_service
        self.something_async = something_async

    def run(self):
        print(type(self.async_service))
        # <class 'coroutine'>

        print(type(self.something_async))
        # <class 'coroutine'>

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_method())
        # AsyncService::__init__ awaited and returned
        # async_something_factory for 'Something' awaited and returned

        print(type(self.async_service))
        # <class '<run_path>.AsyncService'>

        print(type(self.something_async))
        # <class '<run_path>.Something'>


def run_example():
    load_injection_container()
    example = AsyncInjectables()
    example.run()


if __name__ == "__main__":
    run_example()
