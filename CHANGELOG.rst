Changelog
=========

4.0.0 (2024-07-12)
------------------
* Drop support for Python versions 3.6, 3.7 and 3.8
* Comply with PEP-593 and support typing.Annotated

3.4.7 (2021-08-15)
------------------

* Fix injectable crashing when relative imports are used in files containing injectables.

3.4.6 (2021-03-20)
------------------

* Fix ``testing.register_injectables`` not creating the namespace when it doesn't exist
  yet

3.4.5 (2021-03-11)
------------------

* Fix opening of UTF-8 files & allow for user set encoding

3.4.4 (2020-07-29)
------------------

* Fix ``inject`` return type hint

3.4.3 (2020-06-24)
------------------

* Fix Injectable failing to resolve complex/entangled imports

3.4.2 (2020-05-22)
------------------

* Fix optional injection bug when the namespace is empty

3.4.1 (2020-05-11)
------------------

* Fix the use of named args by the caller breaking autowired functions injection

3.4.0 (2020-05-09)
------------------

* Deprecate ``InjectionContainer::load`` in favor of ``load_injection_container``.
* Change default namespace name from ``"_GLOBAL"`` to ``"DEFAULT_NAMESPACE"``.
* Fix minor quirks with Python 3.7 and 3.8.
* Add tons of unit tests.
* Add ``reset_injection_container`` utility to ``injectable.testing``.

3.3.0 (2020-04-20)
------------------

* Include the ``injectable.testing`` utilities to ease mocking injectables.

3.2.1 (2020-04-19)
------------------

* ``InjectionContainer::load`` is more resilient against duplicated injectables
  registering

3.2.0 (2020-04-15)
------------------

* Support for optional injection in declarative fashion: ``Autowired(Optional[...])``

3.1.4 (2020-04-15)
------------------

* Fix ``Autowired(List[...])`` not working with qualifiers

3.1.3 (2020-04-15)
------------------

* Fix Windows injectables not being loaded.

3.1.2 (2020-04-14)
------------------

* Remove unused ``inspect`` imports.

3.1.1 (2020-04-13)
------------------

* Fix bug of scanning the same module more than once when ``InjectionContainer.load()``
  is called multiple times with different relative search paths.

3.1.0 (2020-04-13)
------------------

* Added ``@injectable_factory`` decorator for declaring injectable factory methods
* Include the console output in the examples

3.0.1 (2020-04-13)
------------------

* Fix package content missing

3.0.0 (2020-04-12)
------------------

* Drop support for autowiring without previous initialization of the InjectionContainer
* Refactor ``@autowired`` decorator for working with the ``Autowired`` type annotation
* Added ``@injectable`` decorator for registering injectables to the InjectionContainer
* Support for qualifiers, groups and namespaces
* Added ``Autowired`` type annotation for marking parameters for autowiring
* Added ``inject`` and ``inject_multiple`` as service locators
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
* Fix bug of raising ``TypeError`` when injectable fails on the trial dependency
  instantiation which can happen when the dependency does provide a default
  constructor with no arguments but the running environment (possibly a test suite
  environment) will make the instantiation fail

1.1.0 (2018-02-10)
------------------

* Enable the use of ``@autowired`` decorator without parenthesis

1.0.1 (2018-02-10)
------------------

* Fixes required dependency ``lazy_object_proxy`` not being installed when installing
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
