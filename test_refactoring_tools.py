from unittest import TestCase
from refactoring_tools import swap_two_args_in_function_call


class TestSwapTwoArgsInFunctionCall(TestCase):
    def test_simple_function(self):
        self.assertEqual("func(arg2, arg1)", swap_two_args_in_function_call("func(arg1, arg2)"))

    def test_complicated_function(self):
        self.assertEqual(
            """object1.object2.method(arg_as_func('qwe', 'asd'), arg2(3, 4, 5))""",
            swap_two_args_in_function_call("""object1.object2.method(arg2(3, 4, 5), arg_as_func('qwe', 'asd'))"""))
