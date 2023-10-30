import os

import TestSearcher
def search_config():
    print("searching for config")
    pass


def init_with_config():
    print("initializing with config")
    pass


def search_tests():
    print("searching for tests with rules")
    parent_folder = os.path.dirname(os.getcwd())

    config = TestSearcher.SearchConfig(search_directories=[os.path.join(parent_folder, "PIUnitTests"),
                                                           os.path.join(parent_folder, "Example")],
                                       filename_rules=[], function_rules=[])
    TestSearcher.search_test_files(config)


def execute_tests():
    print("executing tests")
    pass


def generate_output():
    print("generating output")
    pass


if __name__ == "__main__":
    search_config()
    init_with_config()
    search_tests()
    execute_tests()
    generate_output()