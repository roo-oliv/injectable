from typing import TypeVar, Union, Type, List, Sequence

from injectable.errors import InjectionError
from injectable.injection.utils import (
    get_namespace_injectables,
    filter_by_group,
    resolve_single_injectable,
)

T = TypeVar("T")


def inject(
    dependency: Union[T, str],
    *,
    namespace: str = None,
    group: str = None,
    exclude_groups: Sequence[str] = None,
    lazy: bool = False,
    optional: bool = False,
) -> T:
    """
    Injects the requested dependency by instantiating a new instance of it or a
    singleton instance if specified by the injectable. Returns an instance of the
    requested dependency.

    One can use this method directly for injecting dependencies though this is not
    recommended. Use the :meth:`@autowired <injectable.autowired>` decorator and the
    :class:`Autowired <injectable.Autowired>` type annotation for dependency injection
    to be automatically wired to a function's call instead.

    Raises :class:`InjectionContainerNotLoadedError
    <injectable.errors.InjectionContainerNotLoadedError>` when invoked before
    :meth:`InjectionContainer::load <injectable.InjectionContainer.load>` is called.

    Raises
    :class:`InjectionError <injectable.errors.InjectionError>`
    when unable to resolve the requested dependency. This can be due to a variety of
    reasons: the requested dependency wasn't loaded into the container; the namespace
    isn't correct; the group isn't correct; there are multiple injectables for the
    dependency and none or multiple are marked as primary. When parameter ``optional``
    is ``True`` no error will be raised when no injectable that matches requested
    qualifier/class and group is found in the specified namespace though in ambiguous
    cases that resolving a primary injectable is impossible an error will still be
    raised.

    :param dependency: class, base class or qualifier of the dependency to be used for
            lookup among the registered injectables.
    :param namespace: (optional) namespace in which to look for the dependency. Defaults
            to the default namespace specified in
            :meth:`InjectionContainer::load <injectable.InjectionContainer.load>`
    :param group: (optional) group to filter out other injectables outside of this
            group. Defaults to None.
    :param exclude_groups: (optional) list of groups to be excluded. Defaults to None.
    :param lazy: (optional) when True will return an instance which will automatically
            initialize itself when first used but not before that. Defaults to False.
    :param optional: (optional) when True this function returns None if no injectable
            matches the qualifier/class and group inside the specified namespace instead
            of raising an :class:`InjectionError <injectable.errors.InjectionError>`.
            Ambiguous cases where resolving a primary injectable is impossible will
            still raise :class:`InjectionError <injectable.errors.InjectionError>`.
            Defaults to False.

    Usage::

      >>> from foo import Foo
      >>> from injectable import inject
      >>>
      >>> class Bar:
      ...     def __init__(self, foo: Foo = None):
      ...         self.foo = foo or inject(Foo)
    """
    matches, lookup_key, lookup_type = get_namespace_injectables(dependency, namespace)
    if not matches:
        if not optional:
            raise InjectionError(f"No injectable matches {lookup_type} '{lookup_key}'")
        return None
    if group is not None or exclude_groups is not None:
        matches = filter_by_group(
            matches,
            lookup_key=lookup_key,
            lookup_type=lookup_type,
            group=group,
            exclude_groups=exclude_groups,
        )
        if not matches:
            if not optional:
                raise InjectionError(
                    f"No injectable for {lookup_type} '{lookup_key}' matches group"
                    f" '{group}'"
                )
            return None
    injectable = resolve_single_injectable(lookup_key, lookup_type, matches)
    return injectable.get_instance(lazy=lazy)


def inject_multiple(
    dependency: Union[Type[T], str],
    *,
    namespace: str = None,
    group: str = None,
    exclude_groups: Sequence[str] = None,
    lazy: bool = False,
    optional: bool = False,
) -> List[T]:
    """
    Injects all injectables that resolves to the specified dependency. Returns a list of
    instances matching the requested dependency.

    One can use this method directly for injecting dependencies though this is not
    recommended. Use the :meth:`@autowired <injectable.autowired>` decorator and the
    :class:`Autowired <injectable.Autowired>` type annotation for dependency injection
    to be automatically wired to a function's call instead.

    Raises :class:`InjectionContainerNotLoadedError
    <injectable.errors.InjectionContainerNotLoadedError>` when invoked before
    :meth:`InjectionContainer::load <injectable.InjectionContainer.load>` is called.

    Raises
    :class:`InjectionError <injectable.errors.InjectionError>`
    when unable to resolve the requested dependency. This can be due to a variety of
    reasons: there is no injectable loaded into the container that matches the
    dependency; the namespace isn't correct; the group specifications aren't correct.
    When parameter ``optional`` is ``True`` no error will be raised when no injectable
    that matches requested qualifier/class and group is found in the specified
    namespace.

    :param dependency: class, base class or qualifier of the dependency to be used for
            lookup among the registered injectables.
    :param namespace: (optional) namespace in which to look for the dependency. Defaults
            to the default namespace specified in
            :meth:`InjectionContainer::load <injectable.InjectionContainer.load>`
    :param group: (optional) group to filter out other injectables outside of this
            group. Defaults to None.
    :param exclude_groups: (optional) list of groups to be excluded. Defaults to None.
    :param lazy: (optional) when True will returned instances will automatically
            initialize themselves when first used but not before that. Defaults to
            False.
    :param optional: (optional) when True this function returns an empty list if no
            injectable matches the qualifier/class and group inside the specified
            namespace. Defaults to False.

    Usage::

      >>> from com import AbstractService
      >>> from injectable import inject_multiple
      >>> from typing import Sequence
      >>>
      >>> class Foo:
      ...     def __init__(self, services: Sequence[AbstractService] = None):
      ...         self.services = services or inject_multiple(AbstractService)
    """
    matches, lookup_key, lookup_type = get_namespace_injectables(dependency, namespace)
    if not matches:
        if not optional:
            raise InjectionError(f"No injectable matches {lookup_type} '{lookup_key}'")
        return []
    if group is not None or exclude_groups is not None:
        matches = filter_by_group(
            matches,
            lookup_key=lookup_key,
            lookup_type=lookup_type,
            group=group,
            exclude_groups=exclude_groups,
        )
        if not matches:
            if not optional:
                raise InjectionError(
                    f"No injectable for {lookup_type} '{lookup_key}' matches group"
                    f" '{group}'"
                )
            return []
    return [inj.get_instance(lazy=lazy) for inj in matches]
