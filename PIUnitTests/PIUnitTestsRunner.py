import argparse

from PIUnitTests.Config.ConfigLoader import ConfigLoader
from PIUnitTests.Config.SearchConfig import SearchConfig
from PIUnitTests.Searchers.PythonFilesSearcher import PythonFilesSearcher
from PIUnitTests.Searchers.TestFunctionsSearcher import TestFunctionsSearcher
from PIUnitTests.Executors.TestExecutor import TestExecutor


class PIUnitTestRunner:
    def __init__(self):
        self.__config_loader = ConfigLoader()
        pass

    def run(self, path_to_config="", config=None):
        if not config:
            config = self.__search_config(path_to_config)

        self.__init_with_config(config)

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


def setup_argument_parser():
    argument_parser = argparse.ArgumentParser(description="Unit test searcher and runner")

    required_group = argument_parser.add_mutually_exclusive_group(required=True)
    required_group.add_argument("--config", type=str, help="Mode with json config file")
    required_group.add_argument("--no-config", help="Mode with direct setting config values")

    no_config_group = argument_parser.add_argument_group("No config group")
    no_config_group.add_argument("--search-directories", nargs="+", help="Directories to search for tests")
    no_config_group.add_argument("--filename-rules", nargs="+", help="Rules to search for test files")
    no_config_group.add_argument("--function-rules", nargs="+", help="Rules to search for test functions inside file")
    no_config_group.add_argument("--in-depth-search", action="store_false", help="Enable in-depth search")

    return argument_parser


if __name__ == "__main__":
    parser = setup_argument_parser()

    args = parser.parse_args()

    runner = PIUnitTestRunner()
    if args.config:
        runner.run(args.config)
    else:
        search_config = SearchConfig(
            search_directories=args.search_directories,
            filename_rules=args.filename_rules,
            function_rules=args.function_rules,
            in_depth_search=args.in_depth_search
        )
        runner.run(config=search_config)