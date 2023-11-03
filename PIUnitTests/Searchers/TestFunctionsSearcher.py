import ast
from PIUnitTests.Logger.Logger import *


class TestFunctionsSearcher:

    def __init__(self, test_functions_rules):
        self.__rules = test_functions_rules

    def search(self, files):
        test_cases = {}

        for filename in files:
            with open(filename, 'r') as file:
                logger.log(f"Searching test functions in {filename}", Logger.__LOG_LEVEL_DEBUG__)
                tree = ast.parse(file.read(), filename=filename)
                tests = [node.name for node in ast.walk(tree) if (isinstance(node, ast.FunctionDef)
                                                                  and self.__check_function_name(node.name))]
                if tests:
                    logger.log(f"Test found {tests}", Logger.__LOG_LEVEL_DEBUG__)
                    test_cases[filename] = tests
        return test_cases

    def __check_function_name(self, name):
        return any(name.startswith(prefix) for prefix in self.__rules)
