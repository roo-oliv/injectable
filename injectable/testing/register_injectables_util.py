from typing import Optional, Collection

from injectable import InjectionContainer
from injectable.container.injectable import Injectable
from injectable.constants import DEFAULT_NAMESPACE


def register_injectables(
    injectables: Collection[Injectable],
    klass: Optional[type] = None,
    qualifier: Optional[str] = None,
    namespace: str = None,
    propagate: bool = False,
):
    """
    Utility function to manually register injectables in a given namespace for the
    provided class and/or qualifier.

    At least one of ``klass`` or ``qualifier`` parameters need to be defined. Otherwise
    a :class:`ValueError` will be raised.

    :param injectables: a collection of injectables to register.
    :param klass: (optional) the class for which the injectables will be registered.
            This parameter is optional as long as ``qualifier`` is provided. Injectables
            registering won't be propagated to base classes unless otherwise specified
            by the ``propagate`` parameter. Defaults to None.
    :param qualifier: (optional) the qualifier for which the injectables will be
            registered. This parameter is optional as long as ``klass`` is provided.
            Defaults to None.
    :param namespace: (optional) namespace in which the injectable will be registered.
            Defaults to :const:`injectable.constants.DEFAULT_NAMESPACE`.
    :param propagate: (optional) When True injectables registering will be propagated
            to base classes of ``klass`` recursively. Setting this parameter to True
            and not specifying the parameter ``klass`` will raise a :class:`ValueError`.
            Defaults to False.

    Usage::

      >>> from injectable import Injectable
      >>> from injectable.testing import register_injectables
      >>> injectable = Injectable(constructor=lambda: 42)
      >>> register_injectables({injectable}, qualifier="foo")

    .. versionadded:: 3.3.0
    """
    if not klass and not qualifier:
        raise ValueError(
            "At least one of 'klass' or 'qualifier' parameters must to be defined"
        )
    if propagate and not klass:
        raise ValueError(
            "When 'propagate' is True the parameter 'klass' must be defined"
        )
    namespace = InjectionContainer.NAMESPACES[namespace or DEFAULT_NAMESPACE]
    for injectable in injectables:
        namespace.register_injectable(injectable, klass, qualifier, propagate)
