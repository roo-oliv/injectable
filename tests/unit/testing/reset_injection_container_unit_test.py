import os

from injectable import InjectionContainer
from injectable.container.namespace import Namespace
from injectable.testing import reset_injection_container


class TestResetInjectionContainer:
    def test__reset_injection_container(self):
        # given
        InjectionContainer.NAMESPACES = {
            "DEFAULT_NAMESPACE": Namespace(),
            "TEST_NAMESPACE": Namespace(),
        }
        root = "/" if os.name != "nt" else "C:\\"
        InjectionContainer.LOADED_FILEPATHS = {
            os.path.join(root, "fake", "path", "file1.py"),
            os.path.join(root, "fake", "path", "file2.py"),
        }
        InjectionContainer.LOADING_DEFAULT_NAMESPACE = "TEST_NAMESPACE"
        InjectionContainer.LOADING_FILEPATH = os.path.join(
            root, "fake", "path", "file2.py"
        )

        # when
        reset_injection_container()

        # then
        assert InjectionContainer.NAMESPACES == {}
        assert InjectionContainer.LOADED_FILEPATHS == set()
        assert InjectionContainer.LOADING_DEFAULT_NAMESPACE is None
        assert InjectionContainer.LOADING_FILEPATH is None
