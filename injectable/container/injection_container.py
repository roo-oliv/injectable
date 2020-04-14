import os
from importlib.util import module_from_spec, spec_from_file_location
from typing import Dict, Optional, Callable
from typing import Set

from parameters_validation import non_blank
from parameters_validation import non_null
from pycollect import PythonFileCollector, find_module_name

from injectable.container.injectable import Injectable
from injectable.container.namespace import Namespace
from injectable.utils import get_caller_filepath


class InjectionContainer:
    """
    InjectionContainer globally manages injection namespaces and the respective
    injectables registries.

    Invoking :meth:`load` is the only necessary action before injecting dependencies.
    Attempting to call an autowired function before invoking :meth:`load` will raise an
    :class:`InjectionContainerNotLoadedError
    <injectable.errors.InjectionContainerNotLoadedError>`.

    This class is not meant to be instantiated and will raise an error if instantiation
    is attempted.
    """

    LOADING_FILEPATH: Optional[str] = None
    LOADED_FILEPATHS: Set[str] = set()
    CONTEXT: Dict[str, Namespace] = {}
    DEFAULT_NAMESPACE: str

    def __new__(cls):
        raise TypeError("InjectionContainer must not be instantiated")

    @classmethod
    def load(
        cls,
        search_path: non_blank(str) = None,
        *,
        default_namespace: non_blank(str) = None,
    ):
        """
        Loads injectables under the search path to the :class:`InjectionContainer`
        under the designated namespaces.

        This method will not scan any file more than once regardless of being
        called successively. Multiple invocations to different search paths will
        add found injectables to the :class:`InjectionContainer` without clearing
        previously found ones.

        :param search_path: (optional) path under which to search for injectables. Can
                be either a relative or absolute path. Defaults to the caller's file
                directory.
        :param default_namespace: (optional) designated namespace for registering
                injectables which does not explicitly request to be addressed in a
                specific namespace. Defaults to '_GLOBAL'.

        Usage::

          >>> from injectable import InjectionContainer
          >>> InjectionContainer.load()
        """
        cls.DEFAULT_NAMESPACE = default_namespace or "_GLOBAL"
        cls.CONTEXT[default_namespace] = Namespace()
        if search_path is None:
            search_path = os.path.dirname(get_caller_filepath())
        elif not os.path.isabs(search_path):
            caller_path = os.path.dirname(get_caller_filepath())
            search_path = os.path.abspath(os.path.join(caller_path, search_path))
        cls._link_dependencies(search_path)

    @classmethod
    def _register_injectable(
        cls,
        klass: non_null(type),
        qualifier: non_blank(str) = None,
        primary: bool = False,
        namespace: non_blank(str) = None,
        group: non_blank(str) = None,
        singleton: bool = False,
    ):
        injectable = Injectable(klass, primary, group, singleton)
        namespace_entry = cls._get_namespace_entry(namespace or cls.DEFAULT_NAMESPACE)
        namespace_entry.register_injectable(injectable, klass, qualifier)

    @classmethod
    def _register_factory(
        cls,
        factory: non_null(Callable),
        dependency: non_null(type),
        qualifier: non_blank(str) = None,
        primary: bool = False,
        namespace: non_blank(str) = None,
        group: non_blank(str) = None,
        singleton: bool = False,
    ):
        injectable = Injectable(factory, primary, group, singleton)
        namespace_entry = cls._get_namespace_entry(namespace or cls.DEFAULT_NAMESPACE)
        namespace_entry.register_injectable(injectable, dependency, qualifier)

    @classmethod
    def _get_namespace_entry(cls, namespace: str) -> Namespace:
        if namespace not in cls.CONTEXT:
            cls.CONTEXT[namespace] = Namespace()
        return cls.CONTEXT[namespace]

    @classmethod
    def _link_dependencies(cls, search_path: str):
        files = cls._collect_python_files(search_path)
        for file in files:
            if not cls._contains_injectables(file):
                continue
            if file.path in cls.LOADED_FILEPATHS:
                continue
            cls.LOADING_FILEPATH = file.path
            cls._register_injectables(file)
            cls.LOADED_FILEPATHS.add(file.path)
            cls.LOADING_FILEPATH = None

    @classmethod
    def _collect_python_files(cls, search_path) -> Set[os.DirEntry]:
        collector = PythonFileCollector()
        return collector.collect(search_path)

    @classmethod
    def _contains_injectables(cls, file_entry: os.DirEntry) -> bool:
        with open(file_entry) as file:
            source = file.read()
        # TODO: Evaluate the use of ast.parse for this
        return any(
            usage in source
            for usage in [
                "@injectable",
                "injectable(",
                "@injectable_factory",
                "injectable_factory(",
            ]
        )

    @classmethod
    def _register_injectables(cls, file: os.DirEntry):
        module_name = find_module_name(file)
        spec = spec_from_file_location(module_name, file.path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
