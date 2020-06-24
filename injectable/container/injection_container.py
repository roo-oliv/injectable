import os
import warnings
from runpy import run_path
from typing import Dict, Optional, Callable
from typing import Set

from pycollect import PythonFileCollector

from injectable.container.injectable import Injectable
from injectable.container.namespace import Namespace
from injectable.common_utils import get_caller_filepath
from injectable.constants import DEFAULT_NAMESPACE


class InjectionContainer:
    """
    InjectionContainer globally manages injection namespaces and the respective
    injectables registries.

    This class shouldn't be used directly and will be removed from the injectable's
    public API in the future.

    Invoking :func:`load_injection_container` is the only necessary action before
    injecting dependencies. Attempting to call an autowired function before invoking
    :func:`load_injection_container` will log a warning indicating that the injection
    container is empty.

    This class is not meant to be instantiated and will raise an error if instantiation
    is attempted.

    .. deprecated:: 3.4.0
        This class will be removed from the public API in the future.
    """

    LOADING_DEFAULT_NAMESPACE: Optional[str] = None
    LOADING_FILEPATH: Optional[str] = None
    LOADED_FILEPATHS: Set[str] = set()
    NAMESPACES: Dict[str, Namespace] = {}

    def __new__(cls):
        raise NotImplementedError("InjectionContainer must not be instantiated")

    @classmethod
    def load(
        cls, search_path: str = None, *, default_namespace: str = None,
    ):
        """
        Loads injectables under the search path to the :class:`InjectionContainer`
        under the designated namespaces.

        :param search_path: (optional) path under which to search for injectables. Can
                be either a relative or absolute path. Defaults to the caller's file
                directory.
        :param default_namespace: (optional) designated namespace for registering
                injectables which does not explicitly request to be addressed in a
                specific namespace. Defaults to
                :const:`injectable.constants.DEFAULT_NAMESPACE`.

        Usage::

          >>> from injectable import InjectionContainer
          >>> InjectionContainer.load()

        .. note::

            This method will not scan any file more than once regardless of being
            called successively. Multiple invocations to different search paths will
            add found injectables to the :class:`InjectionContainer` without clearing
            previously found ones.

        .. deprecated:: 3.4.0
            This method will be removed from the public API in the future. Use
            :func:`load_injection_container` instead.
        """
        warnings.warn(
            "Using 'load' directly from the 'InjectionContainer' is deprecated."
            " Use 'load_injection_container' instead. This class will be removed from"
            " the injectable's public API in the future.",
            DeprecationWarning,
            2,
        )
        cls.LOADING_DEFAULT_NAMESPACE = default_namespace or DEFAULT_NAMESPACE
        cls.NAMESPACES[default_namespace] = Namespace()
        if search_path is None:
            search_path = os.path.dirname(get_caller_filepath())
        elif not os.path.isabs(search_path):
            caller_path = os.path.dirname(get_caller_filepath())
            search_path = os.path.normpath(os.path.join(caller_path, search_path))
        cls._link_dependencies(search_path)
        cls.LOADING_DEFAULT_NAMESPACE = None

    @classmethod
    def _register_injectable(
        cls,
        klass: type,
        filepath: str,
        qualifier: str = None,
        primary: bool = False,
        namespace: str = None,
        group: str = None,
        singleton: bool = False,
    ):
        unique_id = f"{klass.__qualname__}@{filepath}"
        injectable = Injectable(klass, unique_id, primary, group, singleton)
        namespace_entry = cls._get_namespace_entry(
            namespace or cls.LOADING_DEFAULT_NAMESPACE
        )
        namespace_entry.register_injectable(injectable, klass, qualifier)

    @classmethod
    def _register_factory(
        cls,
        factory: Callable,
        filepath: str,
        dependency: Optional[type] = None,
        qualifier: str = None,
        primary: bool = False,
        namespace: str = None,
        group: str = None,
        singleton: bool = False,
    ):
        unique_id = f"{factory.__qualname__}@{filepath}"
        injectable = Injectable(factory, unique_id, primary, group, singleton)
        namespace_entry = cls._get_namespace_entry(
            namespace or cls.LOADING_DEFAULT_NAMESPACE
        )
        namespace_entry.register_injectable(injectable, dependency, qualifier)

    @classmethod
    def _get_namespace_entry(cls, namespace: str) -> Namespace:
        if namespace not in cls.NAMESPACES:
            cls.NAMESPACES[namespace] = Namespace()
        return cls.NAMESPACES[namespace]

    @classmethod
    def _link_dependencies(cls, search_path: str):
        files = cls._collect_python_files(search_path)
        for file in files:
            if not cls._contains_injectables(file):
                continue
            if file.path in cls.LOADED_FILEPATHS:
                continue
            cls.LOADING_FILEPATH = file.path
            run_path(file.path)
            cls.LOADED_FILEPATHS.add(file.path)
            cls.LOADING_FILEPATH = None

    @classmethod
    def load_dependencies_from(cls, absolute_search_path: str, default_namespace: str):
        files = cls._collect_python_files(absolute_search_path)
        cls.LOADING_DEFAULT_NAMESPACE = default_namespace
        for file in files:
            if not cls._contains_injectables(file):
                continue
            if file.path in cls.LOADED_FILEPATHS:
                continue
            cls.LOADING_FILEPATH = file.path
            run_path(file.path)
            cls.LOADED_FILEPATHS.add(file.path)
            cls.LOADING_FILEPATH = None
        cls.LOADING_DEFAULT_NAMESPACE = None

    @classmethod
    def _collect_python_files(cls, search_path) -> Set[os.DirEntry]:
        collector = PythonFileCollector()
        return collector.collect(search_path)

    @classmethod
    def _contains_injectables(cls, file_entry: os.DirEntry) -> bool:
        with open(file_entry) as file:
            source = file.read()
        # TODO: Consider the use of ast.parse for this
        return any(
            usage in source
            for usage in [
                "@injectable",
                "injectable(",
                "@injectable_factory",
                "injectable_factory(",
            ]
        )
