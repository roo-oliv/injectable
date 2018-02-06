.. _injectable:

Injectable
==========

.. |build| image:: https://travis-ci.org/allrod5/injectable.svg?branch=master
    :target: https://travis-ci.org/allrod5/injectable
    :scale: 100%
    :align: middle
.. |coverage| image:: https://coveralls.io/repos/github/allrod5/injectable/badge.svg?branch=master
    :target: https://coveralls.io/github/allrod5/injectable?branch=master
    :scale: 100%
    :align: middle

|build| |coverage|

Injectable provides an **@autowired** decorator to enable easy and clean dependency injection:

* *Zero setup*: start using it is as simple as decorating the function

* *Autowiring*: injection is transparent to the function

* *Zero boilerplate*: get to function-relevant code right away

* *Support for lazy injection*: circular dependencies are no longer a problem

* *Manually supply dependencies with ease*: using mocked dependencies for testing is easy

**turn this:**

.. code:: python

    def __init__(self, *, model: Model = None, service: Service = None):
        if model is None:
            model = Model()

        if service is None:
            service = Service()

        self.model = model
        self.service = service
        # actual code

**into this:**

.. code:: python

    @autowired()
    def __init__(self, *, model: Model, service: Service):
        self.model = model
        self.service = service
        # actual code

**or this:**

.. code:: python

    class Example:
        def __init__(self, *, lazy_service: Service = None):
            self._service = lazy_service

        @property
        def service(self) -> Service:
            if self._service is None:
                self._service = Service()

            return self._service

        # actual code

**into this:**

.. code:: python

    class Example:
        @autowired(lazy=True)
        def __init__(self, *, lazy_service: Service):
            self.service = service

        # actual code

.. _install:

Install
-------

.. code:: bash

    pip install injectable

.. _usage:

Usage
-----

Just annotate a function with *@autowired*:

.. code:: python

    from injectable import autowired

    class Printer:
        def print_something(self):
            print("Something")

    @autowired()
    def foo(*, printer: Printer):
        printer.print_something()

    foo()
    # Something

.. _how-works:

How does this work?
~~~~~~~~~~~~~~~~~~~

**@autowired** decorator uses type annotations to decide whether or not
to inject the dependency. Some conditions may be observed:

* Only Keyword-Only arguments can be autowired:
    .. code:: python

        @autowired()
        def foo(not_injectable: MyClass, not_injectable_either: MyClass = None,
                *, injectable_kwarg: MyClass):
            ...

* If a default value is provided, the argument will **not** be autowired:
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
    ``TypeError`` raised during initialization of the annotated function.

.. _lazy-init:

Lazy initialize dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a number of reasons why one may want to lazy initialize dependencies.
Common use cases for this are circular dependencies and forward declarations.

**@autowired** decorator takes optional parameter ``lazy`` which when set to ``True``
will force lazy initialization of all injectable dependencies:

.. code:: python

    @autowired(lazy=True)
    def foo(*, a: CircularDependantClass, b: 'ForwardDeclaredClass'):
        ...

It is also possible to keep eager initialization as default and specify lazy
initialization per dependency by using :function:`injectable.lazy` in the annotated
type:

.. code:: python

    @autowired()
    def foo(*, a: MustEagerInit, b: lazy(MustLazyInit)):
        ...

.. _specify-injectables:

Cherry picking arguments for autowiring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If no parameters are passed into **@autowired** decorator then it will consider every
keyword-only argument that does not have a default value to be an injectable
argument. This can be undesired because situations like this can happen:

.. code:: python

    @autowired()
    def foo(*, injectable_dependency: MyClass, not_injectable: ClassWithoutNoArgsContructor):
        ...

    # This will raise a TypeError as parameter `not_injectable` cannot be autowired

This is solved by naming which arguments shall be autowired:

.. code:: python

    @autowired(['injectable_dependency'])
    def foo(*, injectable_dependency: MyClass, not_injectable: ClassWithoutNoArgsContructor):
        ...

    # This will run just fine and only `injectable_dependecy` will be autowired
