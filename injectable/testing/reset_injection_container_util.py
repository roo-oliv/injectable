from injectable import InjectionContainer


def reset_injection_container():
    """
    Utility function to reset the injection container, clearing all injectables
    registered from all namespaces and reseting the record for already scanned files.

    Usage::

      >>> from injectable.testing import reset_injection_container
      >>> reset_injection_container()

    .. versionadded:: 3.4.0
    """
    InjectionContainer.NAMESPACES = {}
    InjectionContainer.LOADED_FILEPATHS = set()
    InjectionContainer.LOADING_DEFAULT_NAMESPACE = None
    InjectionContainer.LOADING_FILEPATH = None
