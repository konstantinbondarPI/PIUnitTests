
from PIUnitTests.Config.ConfigLoader import ConfigLoader
from PIUnitTests.Searchers.PythonFilesSearcher import PythonFilesSearcher
from PIUnitTests.Searchers.TestFunctionsSearcher import TestFunctionsSearcher
from PIUnitTests.Executors.TestExecutor import TestExecutor


class PUUnitTestRunner:
    def __init__(self):
        self.__config_loader = ConfigLoader()
        pass

    def run(self, path_to_config):
        self.__init_with_config(self.__search_config(path_to_config))
        self.__execute_tests(self.__search_tests())

    def __search_tests(self):
        files = self.__files_searcher.search()
        return self.__test_searcher.search(files)

    def __init_with_config(self, config):
        self.__files_searcher = PythonFilesSearcher(search_directories=config.search_directories,
                                                    rules=config.filename_rules,
                                                    in_depth_search=config.in_depth_search)
        self.__test_searcher = TestFunctionsSearcher(test_functions_rules=config.function_rules)
        self.__executor = TestExecutor()

    def __execute_tests(self, tests):
        self.__executor.execute(tests)

    def __search_config(self, path):
        return self.__config_loader.load(path)


if __name__ == "__main__":
    runner = PUUnitTestRunner()
    runner.run("")
