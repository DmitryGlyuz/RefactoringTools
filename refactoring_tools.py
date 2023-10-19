import ast


def swap_two_args_in_function_call(original_string: str) -> str:
    tree = ast.parse(original_string)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            node.args[0], node.args[1] = node.args[1], node.args[0]
            break
    return ast.unparse(tree)


def swap_two_args_in_file(filename: str) -> str:
    with open(filename, 'r') as file:
        original_strings = file.readlines()
    new_strings = [swap_two_args_in_function_call(code_string) for code_string in original_strings]
    return '\n'.join(new_strings)


if __name__ == "__main__":
    print(swap_two_args_in_file("code_for_refactoring.py"))


