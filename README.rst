.. _injectable:

injectable
==========

**@injectable** decorator enables exposing injectable arguments in
function parameters without worrying to initialize these dependencies
latter if the caller didn't inject them.

.. |build| image:: https://travis-ci.org/allrod5/injectable.svg?branch=master
    :target: https://travis-ci.org/allrod5/injectable
    :scale: 100%
    :align: middle
.. |coverage| image:: https://coveralls.io/repos/github/allrod5/injectable/badge.svg?branch=master
    :target: https://coveralls.io/github/allrod5/injectable?branch=master
    :scale: 100%
    :align: middle

|build| |coverage|

.. _usage:

Usage
-----

Just annotate a function with *@injectable* and worry no more
about initializing it's injectable dependencies when the caller do not
pass them explicitly:

.. code:: python

    class Printer:
        def print_something(self):
            print("Something")

    @injectable()
    def foo(*, printer: Printer):
        printer.print_something()

    foo()
    # Something

.. _how-works:

How does this work?
~~~~~~~~~~~~~~~~~~~

**@injectable** decorator uses type annotations to decide whether or not
to inject the dependency. Some conditions may be observed:

* Only Keyword-Only arguments can be injected:
    .. code:: python

        @injectable()
        def foo(not_injectable: MyClass, not_injectable_either: MyClass = None,
                *, injectable_kwarg: MyClass):
            ...

* If a default value is provided, the argument will **not** be injected:
    .. code:: python

        @injectable()
        def foo(*, injectable_kwarg: MyClass, not_injectable_kwarg: MyClass = None):
            ...

* The class must have a default constructor without arguments:
    .. code:: python

        class OkForInjection:
            def __init__(self, optional_arg=42):
                ...

        class NotSuitableForInjection:
            def __init__(self, mandatory_arg):
                ...

    Attempting to use a not suitable class for injection will result in a
    TypeError raised during initialization of the annotated function.

.. _specify-injectables:

Cherry picking arguments for injection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If no parameters are passed into **@injectable** decorator then it will consider every
keyword-only argument that does not have a default value to be an injectable
argument. This can be undesired because situations like this can happen:

.. code:: python

    @injectable()
    def foo(*, injectable_dependency: MyClass, not_injectable: ClassWithoutNoArgsContructor):
        ...

    # This will raise a TypeError as parameter `not_injectable` cannot be injected

This is solved by naming which arguments shall be injected:

.. code:: python

    @injectable(['injectable_dependency'])
    def foo(*, injectable_dependency: MyClass, not_injectable: ClassWithoutNoArgsContructor):
        ...

    # This will run just fine and only `injectable_dependecy` will be injected
