=======
Caveats
=======

This is a non-exhaustive list of known caveats to the usage of this library.

Automatic dependency discovery
------------------------------

Injectable automatic dependency discovery system is inspired from Airflow's DAG automatic
discovery. So first all files in the search path are recursively read looking for any
occurrence of the following four strings: ``@injectable``, ``injectable(``,
``@injectable_factory``, and ``injectable_factory(``. Then those files are executed as
python modules so the decorators can register the injectable to the container.

This implementation leads to some issues:

* If, for any reason, the code aliases the decorators to other incompatible names or
  do not use the decorator functions directly automatic dependency will fail and those
  injectables will never be registered to the container.
* Any file containing these strings will be executed causing potential unintended
  side-effects such as file-level code outside classes and functions being executed.
* The module of each injectable class may be loaded twice: one for in this automatic
  discovery step and another by the regular application operation. This will render
  impossible to run type checks for injected objects through the use of ``type`` or
  ``isinstance`` builtin functions. If one must type check using the type's
  ``__qualname__`` attribute is a possible workaround.

Pytest and relative imports
---------------------------

As described in this issue: https://github.com/pytest-dev/pytest/issues/9007 , pytest
won't work with injectable's automatic dependency discovery system if one declares
injectables in the same file of the test itself, load the injection container during the
test and use relative imports in this file. This corner-case combination will lead to an
``AttributeError: 'AssertionRewritingHook' object has no attribute 'get_code'``.

Currently the workaround for this is either to use absolute imports in these files or to
move the declaration of injectables to any other file other than the test's file.
