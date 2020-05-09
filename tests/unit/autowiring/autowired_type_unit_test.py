from typing import Union, Optional, List, Sequence

import pytest
from pytest_mock import MockFixture

from injectable import Autowired


class TestAutowiredType:
    def test__init__with_union_without_dependency_raises(self):
        with pytest.raises(TypeError):
            Autowired(Union)

    def test__init__with_sequence_without_dependency_raises(self):
        with pytest.raises(TypeError):
            Autowired(Sequence)

    def test__init__with_union_of_more_than_two_types_raises(self):
        with pytest.raises(TypeError):
            Autowired(Union["T", "U", "V"])

    def test__init__with_union_of_not_representing_optional_raises(self):
        with pytest.raises(TypeError):
            Autowired(Union["T", "U"])

    def test__init__with_sequence_of_more_than_one_type_raises(self):
        with pytest.raises(TypeError):
            Autowired(Sequence[Union["T", "U"]])

    def test__init__with_optional_inside_collection_raises(self):
        with pytest.raises(TypeError):
            Autowired(List[Optional["T"]])

    def test__init__with_raw_sequence_with_more_than_one_type_raises(self):
        with pytest.raises(TypeError):
            Autowired(list(["T", "U"]))

    def test__inject__with_class_dependency_and_default_parameters(
        self, mocker: MockFixture
    ):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = {
            "namespace": None,
            "group": None,
            "exclude_groups": None,
            "lazy": False,
            "optional": False,
        }
        autowired = Autowired(TestAutowiredType)

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 1
        assert mocked_inject_multiple.call_count == 0
        args, kwargs = mocked_inject.call_args
        assert args[0] is TestAutowiredType
        assert kwargs == expected

    def test__inject__with_class_dependency_and_explicit_parameters(
        self, mocker: MockFixture
    ):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = {
            "namespace": "dummy",
            "group": "dummy",
            "exclude_groups": ["dummy"],
            "lazy": True,
            "optional": False,
        }
        autowired = Autowired(
            TestAutowiredType,
            namespace=expected["namespace"],
            group=expected["group"],
            exclude_groups=expected["exclude_groups"],
            lazy=expected["lazy"],
        )

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 1
        assert mocked_inject_multiple.call_count == 0
        args, kwargs = mocked_inject.call_args
        assert args[0] is TestAutowiredType
        assert kwargs == expected

    def test__inject__with_qualifier_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(expected)

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 1
        assert mocked_inject_multiple.call_count == 0
        args, kwargs = mocked_inject.call_args
        assert args[0] == expected

    def test__inject__with_raw_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired([TestAutowiredType])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredType

    def test__inject__with_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(List[TestAutowiredType])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredType

    def test__inject__with_list_qualifier_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(List[expected])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == expected

    def test__inject__with_optional_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(Optional[TestAutowiredType])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 1
        assert mocked_inject_multiple.call_count == 0
        args, kwargs = mocked_inject.call_args
        assert args[0] == TestAutowiredType
        assert kwargs["optional"] is True

    def test__inject__with_optional_qualifier_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(Optional[expected])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 1
        assert mocked_inject_multiple.call_count == 0
        args, kwargs = mocked_inject.call_args
        assert args[0] == expected
        assert kwargs["optional"] is True

    def test__inject__with_optional_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(Optional[List[TestAutowiredType]])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredType
        assert kwargs["optional"] is True

    def test__inject__with_optional_list_qualifier_dependency(
        self, mocker: MockFixture
    ):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(Optional[List[expected]])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == expected
        assert kwargs["optional"] is True
