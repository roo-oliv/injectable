from typing import List

import typing_inspect
from injectable.autowiring.autowiring_utils import sanitize_if_forward_ref


class TestSanitizeIfForwardRef:
    def test__sanitize_if_forward_ref__with_no_forward_ref(self):
        # given
        tp = List[str]
        subscripted_type = typing_inspect.get_args(tp, evaluate=True)[0]

        # when
        sanitized_type = sanitize_if_forward_ref(subscripted_type)

        # then
        assert sanitized_type == subscripted_type

    def test__sanitize_if_forward_ref__with_forward_ref(self):
        # given
        forward_ref = "forward_ref"
        tp = List[forward_ref]
        subscripted_type = typing_inspect.get_args(tp, evaluate=True)[0]

        # when
        sanitized_type = sanitize_if_forward_ref(subscripted_type)

        # then
        assert sanitized_type == forward_ref
