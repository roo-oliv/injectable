from typing import Optional

from pytest_mock import MockFixture

from injectable import Autowired


class TestAutowiredTypePy39:
    def test__inject__with_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(list[TestAutowiredTypePy39])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredTypePy39

    def test__inject__with_list_qualifier_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(list[expected])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == expected

    def test__inject__with_optional_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(Optional[list[TestAutowiredTypePy39]])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredTypePy39
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
        autowired = Autowired(Optional[list[expected]])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == expected
        assert kwargs["optional"] is True
