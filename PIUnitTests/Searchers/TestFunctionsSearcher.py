import ast


class TestFunctionsSearcher:

    def __init__(self, test_functions_rules, files):
        self.__rules = test_functions_rules
        self.__files = files

    def search(self):
        test_cases = {}

        for filename in self.__files:
            with open(filename, 'r') as file:
                tree = ast.parse(file.read(), filename=filename)
                tests = [node.name for node in ast.walk(tree) if (isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))]
                if tests:
                    test_cases[filename] = tests
        return test_cases

