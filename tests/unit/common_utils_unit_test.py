from injectable.common_utils import get_dependency_name, get_caller_filepath


class TestGetCallerFilepath:
    def test__get_caller_filepath__with_1_step_back(self):
        # given
        expected = __file__

        # when
        filepath = get_caller_filepath(steps_back=1)

        # then
        assert filepath == expected


class TestGetDependencyName:
    def test__get_dependency_name__using_class(self):
        # given
        class_name = "TestClass"
        klass = type(class_name, (), {})

        # when
        name = get_dependency_name(klass)

        # then
        assert name == class_name

    def test__get_dependency_name__using_function(self):
        # given
        expected = "TestGetDependencyName.test__get_dependency_name__using_function"

        # when
        name = get_dependency_name(self.test__get_dependency_name__using_function)

        # then
        assert name == expected

    def test__get_dependency_name__using_qualifier(self):
        # given
        qualifier = "qualifier"

        # when
        name = get_dependency_name(qualifier)

        # then
        assert name == qualifier
