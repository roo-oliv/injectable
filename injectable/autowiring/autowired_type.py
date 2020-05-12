from typing import Union, TypeVar, Sequence

import typing_inspect

from injectable.autowiring.autowiring_utils import (
    sanitize_if_forward_ref,
    is_sequence,
    is_raw_sequence,
)
from injectable.injection.inject import inject, inject_multiple

T = TypeVar("T")


class _Autowired:
    def __init__(
        self,
        dependency: Union[T, str],
        *,
        namespace: str = None,
        group: str = None,
        exclude_groups: Sequence[str] = None,
        lazy: bool = False,
    ):
        optional = False
        multiple = False

        if typing_inspect.is_optional_type(dependency):
            dependency = typing_inspect.get_args(dependency, evaluate=True)[0]
            optional = True
        elif typing_inspect.is_union_type(dependency):
            raise TypeError(
                "Autowired Union can only be used to indicate"
                " optional autowiring in the forms 'Union[T, None]' or"
                " 'Optional[T]'"
            )

        if is_sequence(typing_inspect.get_origin(dependency) or dependency):
            subscripted_types = typing_inspect.get_args(dependency, evaluate=True)
            if subscripted_types == typing_inspect.get_args(Sequence):
                raise TypeError("Type not defined for Autowired list")
            subscripted_type = subscripted_types[0]
            if typing_inspect.is_optional_type(subscripted_type):
                raise TypeError(
                    "List of Optional is invalid for autowiring. Use"
                    " 'Autowired(Optional[List[...]])' instead."
                )
            elif typing_inspect.is_union_type(subscripted_type):
                raise TypeError("Only one type should be defined for Autowired list")
            dependency = subscripted_type
            multiple = True
        elif is_raw_sequence(dependency):
            if len(dependency) != 1:
                raise TypeError(
                    "Only one type should be defined for Autowired"
                    f" {dependency.__class__.__qualname__}"
                )
            dependency = dependency[0]
            multiple = True

        self.optional = optional
        self.multiple = multiple
        self.dependency = sanitize_if_forward_ref(dependency)
        self.namespace = namespace
        self.group = group
        self.exclude_groups = exclude_groups
        self.lazy = lazy

    def inject(self) -> T:
        if self.multiple:
            return inject_multiple(
                self.dependency,
                namespace=self.namespace,
                group=self.group,
                exclude_groups=self.exclude_groups,
                lazy=self.lazy,
                optional=self.optional,
            )
        return inject(
            self.dependency,
            namespace=self.namespace,
            group=self.group,
            exclude_groups=self.exclude_groups,
            lazy=self.lazy,
            optional=self.optional,
        )


class Autowired:
    """
    Autowired type annotation marks a parameter to be autowired for injection.

    Autowired parameters must be last in declaration if there are others which aren't
    autowired. Also, autowired parameters must not be given default values.

    This type annotation does not performs the function autowiring by itself. The
    function must be decorated with :meth:`@autowired <injectable.autowired>` for
    autowiring.


    :param dependency: class, base class or qualifier of the dependency to be used
            for lookup among the registered injectables. Can be wrapped in a typing
            sequence, e.g. ``List[...]``, to inject a list containing all matching
            injectables. Can be wrapped in a optional, e.g. ``Optional[...]``, to
            inject None if no matches are found to inject. ``Optional[List[...]]`` is
            valid and will inject an empty list if no matches are found to inject.
    :param namespace: (optional) namespace in which to look for the dependency.
            Defaults to :const:`injectable.constants.DEFAULT_NAMESPACE`.
    :param group: (optional) group to filter out other injectables outside of this
            group. Defaults to None.
    :param exclude_groups: (optional) list of groups to be excluded. Defaults to
            None.
    :param lazy: (optional) when True will return an instance which will
            automatically initialize itself when first used but not before that.
            Defaults to False.

    Usage::

      >>> from injectable import Autowired, autowired
      >>>
      >>> @autowired
      ... def foo(arg: Autowired("qualifier")):
      ...     ...
    """

    # fake signature to conform return type to be the same as the dependency arg
    def __new__(
        cls,
        dependency: Union[T, str],
        *,
        namespace: str = None,
        group: str = None,
        exclude_groups: Sequence[str] = None,
        lazy: bool = False,
    ) -> T:
        return _Autowired(
            dependency,
            namespace=namespace,
            group=group,
            exclude_groups=exclude_groups,
            lazy=lazy,
        )
