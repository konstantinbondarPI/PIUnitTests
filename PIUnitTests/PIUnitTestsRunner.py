import os

from PIUnitTests.Searchers import SearchConfig
from PIUnitTests.Searchers.PythonFilesSearcher import PythonFilesSearcher
from PIUnitTests.Searchers.TestFunctionsSearcher import TestFunctionsSearcher
from PIUnitTests.Executors.TestExecutor import TestExecutor

def search_config():
    print("searching for config")
    pass


def init_with_config():
    print("initializing with config")
    pass


def search_tests():
    print("searching for tests with rules")
    parent_folder = os.path.dirname(os.getcwd())

    config = SearchConfig(search_directories=[os.path.join(parent_folder, "Example")],
                          filename_rules=["*"],
                          function_rules=[""], )
    files_searcher = PythonFilesSearcher(config)
    files = files_searcher.search()

    test_searcher = TestFunctionsSearcher(config.function_rules, files)
    return test_searcher.search()


def execute_tests(test_cases):
    executor = TestExecutor(test_cases)
    executor.execute()


def generate_output():
    print("generating output")
    pass


if __name__ == "__main__":
    search_config()
    init_with_config()
    test_cases = search_tests()
    execute_tests(test_cases)
    generate_output()
