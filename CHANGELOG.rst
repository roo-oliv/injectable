Changelog
=========

3.0.0 (2020-04-12)
------------------

* Drop support for autowiring without previous initialization of the InjectionContainer
* Refactor `@autowired` decorator for working with the `Autowired` type annotation
* Added `@injectable` decorator for registering injectables to the InjectionContainer
* Support for qualifiers, groups and namespaces
* Added `Autowired` type annotation for marking parameters for autowiring
* Added `inject` and `inject_multiple` as service locators
* Added InjectionContainer for registering injectables
* Official support for Python 3.7 and 3.8
* Official support for Ubuntu, Windows and MacOS
* Drop Python 3.4 and 3.5 official support
* General code refactoring
* Official documentation
* Added usage examples

2.0.0 (2018-02-24)
------------------

* Drop Python 3.3 official support

1.1.2 (2018-02-24)
------------------

* Support for dependencies of classes without signature
* Fix bug of builtin types not being accepted for injectable dependencies

1.1.1 (2018-02-23)
------------------

* Statically infer dependency's constructor suitability for injection instead of using
    trial instantiation
* Fix bug of raising `TypeError` when injectable fails on the trial dependency
    instantiation which can happen when the dependency does provide a default
    constructor with no arguments but the running environment (possibly a test suite
    environment) will make the instantiation fail

1.1.0 (2018-02-10)
------------------

* Enable the use of `@autowired` decorator without parenthesis

1.0.1 (2018-02-10)
------------------

* Fixes required dependency `lazy_object_proxy` not being installed when installing
    injectable through pip

1.0.0 (2018-02-06)
------------------

* First stable release

0.2.0 (2018-02-06)
------------------

* Support for lazy dependency initialization
* Support for type annotations with strings

0.1.1 (2018-02-05)
------------------

* Python 3.3 and 3.4 support

0.1.0 (2018-02-05)
------------------

* First beta release
