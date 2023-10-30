import importlib.util
import inspect
import os
import time

from PIUnitTests.Searchers import SearchConfig
from PIUnitTests.Searchers.PythonFilesSearcher import PythonFilesSearcher
from PIUnitTests.Searchers.TestFunctionsSearcher import TestFunctionsSearcher


def search_config():
    print("searching for config")
    pass


def init_with_config():
    print("initializing with config")
    pass


def search_tests():
    print("searching for tests with rules")
    parent_folder = os.path.dirname(os.getcwd())

    config = SearchConfig(search_directories=[os.path.join(parent_folder, "PIUnitTests"),
                                              os.path.join(parent_folder, "Example")],
                          filename_rules=["*"],
                          function_rules=[], )
    files_searcher = PythonFilesSearcher(config)
    files = files_searcher.search()

    # print("\n".join(files))

    test_searcher = TestFunctionsSearcher(config.function_rules, files)
    return test_searcher.search()


def execute_tests(tests):
    for filename in tests.keys():
        test_names = tests[filename]
        module_name = inspect.getmodulename(filename)
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name in test_names:
            func = getattr(module, name, None)
            if func:
                executing_test_decorator(func, module_name)
            else:
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        instance = obj()
                        if hasattr(instance, name) and callable(getattr(instance, name)):
                            func = getattr(instance, name, None)
                            if func:
                                executing_test_decorator(func, module_name)


def executing_test_decorator(fun, filename):
    print("\n------------------")
    print(f"Executing test: {fun.__name__} from: {filename}.py")
    start_time = time.time()
    try:
        fun()
        print("Succeed")
    except AssertionError as assert_error:
        error_message = f"with assert message: \'{assert_error}\'" if assert_error.args else ""
        print(f"Failed {error_message}")

    print(f"Time elapsed: {(time.time() - start_time):.2f}")
    print("------------------\n")

def generate_output():
    print("generating output")
    pass


if __name__ == "__main__":
    search_config()
    init_with_config()
    tests = search_tests()
    execute_tests(tests)
    generate_output()
