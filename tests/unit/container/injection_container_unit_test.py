import os
from unittest.mock import MagicMock

import pytest
from pytest import fixture
from pytest_mock import MockFixture

from injectable.container.injection_container import InjectionContainer
from injectable.container.namespace import Namespace
from injectable.constants import DEFAULT_NAMESPACE
from injectable.testing import reset_injection_container


@fixture
def patch_injection_container(mocker: MockFixture):
    module_path = "injectable.container.injection_container"
    return lambda name, **kwargs: mocker.patch(f"{module_path}.{name}", **kwargs)


@fixture
def patch_open(mocker: MockFixture):
    return lambda *a, **kw: mocker.patch("builtins.open", mocker.mock_open(*a, **kw))


@fixture(autouse=True)
def reset_injection_container_before_test():
    reset_injection_container()


class TestInjectionContainer:
    def test__new__raises(self):
        with pytest.raises(NotImplementedError):
            InjectionContainer()

    def test__load__leaves_loading_vars_clean(self, patch_injection_container):
        # given
        patch_injection_container(
            "get_caller_filepath", return_value=os.path.join("fake", "path", "file.py")
        )
        patch_injection_container("PythonFileCollector")

        # when
        InjectionContainer.load()

        # then
        assert InjectionContainer.LOADING_FILEPATH is None
        assert InjectionContainer.LOADING_DEFAULT_NAMESPACE is None

    def test__load__with_defaults(self, patch_injection_container):
        # given
        get_caller_filepath = patch_injection_container(
            "get_caller_filepath", return_value=os.path.join("fake", "path", "file.py")
        )
        file_collector = MagicMock()
        patch_injection_container("PythonFileCollector", return_value=file_collector)

        # when
        InjectionContainer.load()

        # then
        assert get_caller_filepath.called is True
        assert file_collector.collect.called is True

    def test__load__with_absolute_search_path(self, patch_injection_container):
        # given
        get_caller_filepath = patch_injection_container("get_caller_filepath")
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        file_collector = MagicMock()
        patch_injection_container("PythonFileCollector", return_value=file_collector)

        # when
        InjectionContainer.load(search_path)

        # then
        assert get_caller_filepath.called is False
        assert file_collector.collect.called is True

    def test__load__with_relative_search_path(self, patch_injection_container):
        # given
        search_path = os.path.join("..", "relative", "path")
        get_caller_filepath = patch_injection_container(
            "get_caller_filepath",
            return_value=os.path.join("fake", "path", "file.py"),
        )
        expected_path = os.path.join("fake", "relative", "path")
        file_collector = MagicMock()
        patch_injection_container("PythonFileCollector", return_value=file_collector)

        # when
        InjectionContainer.load(search_path)

        # then
        assert get_caller_filepath.called is True
        assert file_collector.collect.call_args[0][0] == expected_path

    def test__load__with_files_with_injectables(
        self, patch_injection_container, patch_open
    ):
        # given
        patch_injection_container(
            "get_caller_filepath",
            return_value=os.path.join("fake", "path", "file.py"),
        )
        file_collector = MagicMock()
        file_collector.collect.return_value = {
            MagicMock(spec=os.DirEntry),
            MagicMock(spec=os.DirEntry),
        }
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(
            read_data="from injectable import injectable\n@injectable\nclass A: ..."
        )
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")

        # when
        InjectionContainer.load()

        # then
        assert file_collector.collect.called is True
        assert run_module.call_count == 2
        assert run_path.call_count == 0

    def test__load__when_runpy_run_module_fails_in_pytest_corner_case(
        self, patch_injection_container, patch_open
    ):
        # given
        patch_injection_container(
            "get_caller_filepath",
            return_value=os.path.join("fake", "path", "file.py"),
        )
        file_collector = MagicMock()
        file_collector.collect.return_value = {
            MagicMock(spec=os.DirEntry),
            MagicMock(spec=os.DirEntry),
        }
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(
            read_data="from injectable import injectable\n@injectable\nclass A: ..."
        )
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")

        def raise_attribute_error(*args, **kwargs):
            raise AttributeError()

        run_module.side_effect = raise_attribute_error
        run_path = patch_injection_container("run_path")

        # when
        InjectionContainer.load()

        # then
        assert file_collector.collect.called is True
        assert run_module.call_count == 2
        assert run_path.call_count == 2

    def test__load__with_files_without_injectables(
        self, patch_injection_container, patch_open
    ):
        # given
        patch_injection_container(
            "get_caller_filepath",
            return_value=os.path.join("fake", "path", "file.py"),
        )
        file_collector = MagicMock()
        file_collector.collect.return_value = {
            MagicMock(spec=os.DirEntry),
            MagicMock(spec=os.DirEntry),
        }
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(read_data='"""not injectable"""')
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")

        # when
        InjectionContainer.load()

        # then
        assert file_collector.collect.called is True
        assert run_module.called is False
        assert run_path.called is False

    def test__load__with_already_loaded_files(
        self, patch_injection_container, patch_open
    ):
        # given
        patch_injection_container(
            "get_caller_filepath",
            return_value=os.path.join("fake", "path", "file.py"),
        )
        mocked_file_1 = MagicMock(spec=os.DirEntry)
        mocked_file_1.path = os.path.join("fake", "path", "file_1.py")
        mocked_file_2 = MagicMock(spec=os.DirEntry)
        mocked_file_2.path = os.path.join("fake", "path", "file_2.py")
        file_collector = MagicMock()
        file_collector.collect.return_value = {mocked_file_1, mocked_file_2}
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(
            read_data="from injectable import injectable\n@injectable\nclass A: ..."
        )
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")
        InjectionContainer.load()

        # when
        InjectionContainer.load()

        # then
        assert file_collector.collect.call_count == 2
        assert run_module.call_count == 2
        assert run_path.call_count == 0
        assert len(InjectionContainer.LOADED_FILEPATHS) == 2

    def test__load_dependencies_from__leaves_loading_vars_clean(
        self, patch_injection_container
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        namespace = DEFAULT_NAMESPACE
        patch_injection_container("PythonFileCollector")

        # when
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # then
        assert InjectionContainer.LOADING_FILEPATH is None
        assert InjectionContainer.LOADING_DEFAULT_NAMESPACE is None

    def test__load_dependencies_from__regular_call(self, patch_injection_container):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        namespace = DEFAULT_NAMESPACE
        file_collector = MagicMock()
        patch_injection_container("PythonFileCollector", return_value=file_collector)

        # when
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # then
        assert file_collector.collect.called is True

    def test__load_dependencies_from__with_files_with_injectables(
        self, patch_injection_container, patch_open
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        namespace = DEFAULT_NAMESPACE
        file_collector = MagicMock()
        file_collector.collect.return_value = {
            MagicMock(spec=os.DirEntry),
            MagicMock(spec=os.DirEntry),
        }
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(
            read_data="from injectable import injectable\n@injectable\nclass A: ..."
        )
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")

        # when
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # then
        assert file_collector.collect.called is True
        assert run_module.call_count == 2
        assert run_path.call_count == 0

    def test__load_dependencies_from__with_files_without_injectables(
        self, patch_injection_container, patch_open
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        namespace = DEFAULT_NAMESPACE
        file_collector = MagicMock()
        file_collector.collect.return_value = {
            MagicMock(spec=os.DirEntry),
            MagicMock(spec=os.DirEntry),
        }
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(read_data='"""not injectable"""')
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")

        # when
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # then
        assert file_collector.collect.called is True
        assert run_module.called is False
        assert run_path.called is False

    def test__load_dependencies_from__with_already_loaded_files(
        self, patch_injection_container, patch_open
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        namespace = DEFAULT_NAMESPACE
        mocked_file_1 = MagicMock(spec=os.DirEntry)
        mocked_file_1.path = os.path.join("fake", "path", "file_1.py")
        mocked_file_2 = MagicMock(spec=os.DirEntry)
        mocked_file_2.path = os.path.join("fake", "path", "file_2.py")
        file_collector = MagicMock()
        file_collector.collect.return_value = {mocked_file_1, mocked_file_2}
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(
            read_data="from injectable import injectable\n@injectable\nclass A: ..."
        )
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # when
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # then
        assert file_collector.collect.call_count == 2
        assert run_module.call_count == 2
        assert run_path.call_count == 0
        assert len(InjectionContainer.LOADED_FILEPATHS) == 2

    def test__load_dependencies_from__with_specific_encoding(
        self, patch_injection_container, patch_open
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")
        namespace = DEFAULT_NAMESPACE
        file_collector = MagicMock()
        file_collector.collect.return_value = {
            MagicMock(spec=os.DirEntry),
            MagicMock(spec=os.DirEntry),
        }
        patch_injection_container(
            "PythonFileCollector",
            return_value=file_collector,
        )
        patch_open(
            read_data=r"from injectable import injectable\n@injectable\nclass A: ..."
        )
        patch_injection_container("module_finder")
        run_module = patch_injection_container("run_module")
        run_path = patch_injection_container("run_path")

        # when
        InjectionContainer.load_dependencies_from(search_path, namespace)

        # then
        assert file_collector.collect.called is True
        assert run_module.call_count == 2
        assert run_path.call_count == 0

    def test__register_injectable__with_defaults(self, patch_injection_container):
        # given
        klass = TestInjectionContainer
        filepath = os.path.join("fake", "path", "file.py")
        namespace = "TEST"
        InjectionContainer.LOADING_DEFAULT_NAMESPACE = namespace
        mocked_namespace: Namespace = MagicMock(spec=Namespace)
        patch_injection_container(
            "Namespace",
            return_value=mocked_namespace,
        )

        # when
        InjectionContainer._register_injectable(klass, filepath)

        # then
        assert namespace in InjectionContainer.NAMESPACES
        assert InjectionContainer.NAMESPACES[namespace] == mocked_namespace
        assert mocked_namespace.register_injectable.call_count == 1
        (
            injectable_arg,
            klass_arg,
            qualifier_arg,
        ) = mocked_namespace.register_injectable.call_args[0][:3]
        assert injectable_arg.constructor is klass
        assert injectable_arg.unique_id is not None
        assert injectable_arg.primary is False
        assert injectable_arg.group is None
        assert injectable_arg.singleton is False
        assert klass_arg is klass
        assert qualifier_arg is None

    def test__register_injectable__with_explicit_values(
        self, patch_injection_container
    ):
        # given
        klass = TestInjectionContainer
        filepath = os.path.join("fake", "path", "file.py")
        qualifier = "QUALIFIER"
        namespace = "TEST"
        group = "GROUP"
        InjectionContainer.LOADING_DEFAULT_NAMESPACE = DEFAULT_NAMESPACE
        mocked_namespace: Namespace = MagicMock(spec=Namespace)
        patch_injection_container(
            "Namespace",
            return_value=mocked_namespace,
        )

        # when
        InjectionContainer._register_injectable(
            klass, filepath, qualifier, True, namespace, group, True
        )

        # then
        assert namespace in InjectionContainer.NAMESPACES
        assert InjectionContainer.NAMESPACES[namespace] == mocked_namespace
        assert mocked_namespace.register_injectable.call_count == 1
        (
            injectable_arg,
            klass_arg,
            qualifier_arg,
        ) = mocked_namespace.register_injectable.call_args[0][:3]
        assert injectable_arg.constructor is klass
        assert injectable_arg.unique_id is not None
        assert injectable_arg.primary is True
        assert injectable_arg.group is group
        assert injectable_arg.singleton is True
        assert klass_arg is klass
        assert qualifier_arg is qualifier

    def test__register_factory__for_class_with_defaults(
        self, patch_injection_container
    ):
        # given
        factory = MagicMock
        klass = TestInjectionContainer
        filepath = os.path.join("fake", "path", "file.py")
        namespace = "TEST"
        InjectionContainer.LOADING_DEFAULT_NAMESPACE = namespace
        mocked_namespace: Namespace = MagicMock(spec=Namespace)
        patch_injection_container(
            "Namespace",
            return_value=mocked_namespace,
        )

        # when
        InjectionContainer._register_factory(factory, filepath, klass)

        # then
        assert namespace in InjectionContainer.NAMESPACES
        assert InjectionContainer.NAMESPACES[namespace] == mocked_namespace
        assert mocked_namespace.register_injectable.call_count == 1
        (
            injectable_arg,
            klass_arg,
            qualifier_arg,
        ) = mocked_namespace.register_injectable.call_args[0][:3]
        assert injectable_arg.constructor is factory
        assert injectable_arg.unique_id is not None
        assert injectable_arg.primary is False
        assert injectable_arg.group is None
        assert injectable_arg.singleton is False
        assert klass_arg is klass
        assert qualifier_arg is None

    def test__register_factory__for_qualifier_with_defaults(
        self, patch_injection_container
    ):
        # given
        factory = MagicMock
        qualifier = "QUALIFIER"
        filepath = os.path.join("fake", "path", "file.py")
        namespace = "TEST"
        InjectionContainer.LOADING_DEFAULT_NAMESPACE = namespace
        mocked_namespace: Namespace = MagicMock(spec=Namespace)
        patch_injection_container(
            "Namespace",
            return_value=mocked_namespace,
        )

        # when
        InjectionContainer._register_factory(factory, filepath, qualifier=qualifier)

        # then
        assert namespace in InjectionContainer.NAMESPACES
        assert InjectionContainer.NAMESPACES[namespace] == mocked_namespace
        assert mocked_namespace.register_injectable.call_count == 1
        (
            injectable_arg,
            klass_arg,
            qualifier_arg,
        ) = mocked_namespace.register_injectable.call_args[0][:3]
        assert injectable_arg.constructor is factory
        assert injectable_arg.unique_id is not None
        assert injectable_arg.primary is False
        assert injectable_arg.group is None
        assert injectable_arg.singleton is False
        assert klass_arg is None
        assert qualifier_arg is qualifier

    def test__register_factory__with_all_explicit_values(
        self, patch_injection_container
    ):
        # given
        factory = MagicMock
        klass = TestInjectionContainer
        filepath = os.path.join("fake", "path", "file.py")
        qualifier = "QUALIFIER"
        namespace = "TEST"
        group = "GROUP"
        InjectionContainer.LOADING_DEFAULT_NAMESPACE = DEFAULT_NAMESPACE
        mocked_namespace: Namespace = MagicMock(spec=Namespace)
        patch_injection_container(
            "Namespace",
            return_value=mocked_namespace,
        )

        # when
        InjectionContainer._register_factory(
            factory, filepath, klass, qualifier, True, namespace, group, True
        )

        # then
        assert namespace in InjectionContainer.NAMESPACES
        assert InjectionContainer.NAMESPACES[namespace] == mocked_namespace
        assert mocked_namespace.register_injectable.call_count == 1
        (
            injectable_arg,
            klass_arg,
            qualifier_arg,
        ) = mocked_namespace.register_injectable.call_args[0][:3]
        assert injectable_arg.constructor is factory
        assert injectable_arg.unique_id is not None
        assert injectable_arg.primary is True
        assert injectable_arg.group is group
        assert injectable_arg.singleton is True
        assert klass_arg is klass
        assert qualifier_arg is qualifier
