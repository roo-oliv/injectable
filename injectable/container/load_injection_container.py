import os

from injectable.container.injection_container import InjectionContainer
from injectable.common_utils import get_caller_filepath
from injectable.constants import DEFAULT_NAMESPACE


def load_injection_container(
    search_path: str = None, *, default_namespace: str = None,
):
    """
    Loads injectables under the search path to a shared injection container under the
    designated namespaces.

    :param search_path: (optional) path under which to search for injectables. Can
            be either a relative or absolute path. Defaults to the caller's file
            directory.
    :param default_namespace: (optional) designated namespace for registering
            injectables which does not explicitly request to be addressed in a
            specific namespace. Defaults to
            :const:`injectable.constants.DEFAULT_NAMESPACE`.

    Usage::

      >>> from injectable import load_injection_container
      >>> load_injection_container()

    .. note::

        This method will not scan any file already scanned by previous calls to it.
        Multiple invocations to different search paths will add found injectables into
        the injection container without clearing previously loaded ones but never
        loading a same injectable more than once.

    .. versionadded:: 3.4.0
    """
    if search_path is None:
        search_path = os.path.dirname(get_caller_filepath())
    elif not os.path.isabs(search_path):
        caller_path = os.path.dirname(get_caller_filepath())
        search_path = os.path.abspath(os.path.join(caller_path, search_path))
    InjectionContainer.load_dependencies_from(
        search_path, default_namespace or DEFAULT_NAMESPACE
    )
