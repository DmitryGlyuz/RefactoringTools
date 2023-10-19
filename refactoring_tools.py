import ast
import re


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


def transform_keys_in_dict(code_with_dict: str, transform_func) -> str:
    """
        Transforms keys within dictionaries found in Python code using a provided function.

        This function parses a Python code string, identifies dictionaries, and applies a
        transformation function to their keys. It then returns the modified code as a string.

        Args:
            code_with_dict (str): A string containing Python code that may include dictionaries.
            transform_func (callable): A function that takes a string (the original key) and
                returns a modified string to replace the original key.

        Returns:
            str: A modified Python code string with transformed dictionary keys.

        Example:
            If you have a Python code string like this:
            >>> code = "my_dict = {'first_name': 'John', 'last_name': 'Doe'}"

            And a transformation function that converts keys to uppercase:
            >>> def uppercase_string(string):
            ...     return str(string).upper()

            You can use this function to transform the keys:
            >>> transformed_code = transform_keys_in_dict(code, uppercase_string)

            The result would be:
            # >>> print(transformed_code)
            "my_dict = {'FIRST_NAME': 'John', 'LAST_NAME': 'Doe'}"
        """
    tree = ast.parse(code_with_dict)
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key in node.keys:
                key.value = transform_func(key.value)
    return str(ast.unparse(tree))


def swap_values_around_hyphen(original_string: str) -> str:
    """
        Swaps the positions of two words around a hyphen, which may or may not have spaces around it, in the input
        string.

        Parameters:
        original_strring (str): The input string containing two words separated by a hyphen, which may or may not
        have spaces around it.

        Returns:
        str: A new string with the positions of the two words swapped around the hyphen, preserving any space
        formatting.

        Example:
        >>> swap_values_around_hyphen("apple - banana")
        'banana - apple'
        >>> swap_values_around_hyphen("chocolate-  vanilla")
        'vanilla-  chocolate'

        Note:
        The function assumes that the input string contains exactly one hyphen ('-') that may or may not have spaces
        around it, and two words separated by it. It preserves any spaces around the hyphen in the output.
        """
    match = re.search(r"(\w+)( *- *)(\w+)", original_string)
    return f"{match.group(3)}{match.group(2)}{match.group(1)}"


def transform_string_keys_in_dict_using_regexps(code_string: str, transform_func) -> str:
    """
        Transforms the keys in a dictionary-like string using regular expressions and a custom transformation function.

        This function takes a string representation of a dictionary and applies a regular expression to match and
        transform the keys (as str) using the provided `transform_func`.
        It returns the modified string with transformed keys.

        Args:
            code_string (str): The input string containing a dictionary-like structure.
            transform_func (callable): A function that takes a string and returns the transformed version of the string.
                This function is applied to the matched key strings in the dictionary.

        Returns:
            str: A new string with keys in the dictionary transformed as per the `transform_func`.
        """
    pattern = r"""('|").*('|"):"""

    def replace_func(match):
        new_value = transform_func(match.group(0))
        return f'"{new_value}"'

    return re.sub(pattern, replace_func, code_string)
