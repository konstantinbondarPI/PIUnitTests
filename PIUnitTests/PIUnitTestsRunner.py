from .Config.ConfigLoader import ConfigLoader
from .Executors.TestExecutor import TestExecutor
from .Report.ReportCreator import ReportCreator
from .Searchers.PythonFilesSearcher import PythonFilesSearcher
from .Searchers.TestFunctionsSearcher import TestFunctionsSearcher
from .Logger.Logger import *


class PIUnitTestRunner:
    def __init__(self):
        self.__config_loader = ConfigLoader()
        self.__report_creator = ReportCreator()
        pass

    def run(self, path_to_config="", config=None):
        if not config:
            logger.log(f"Searching for config at {path_to_config}", Logger.__LOG_LEVEL_DEBUG__)
            config = self.__search_config(path_to_config)

        self.__init_with_config(config)
        self.__execute_tests(self.__search_tests())

    def __search_tests(self):
        files = self.__files_searcher.search()
        logger.log(f"Test files found {files}", Logger.__LOG_LEVEL_DEBUG__)
        return self.__test_searcher.search(files)

    def __init_with_config(self, config):
        self.__files_searcher = PythonFilesSearcher(search_directories=config.search_directories,
                                                    rules=config.filename_rules,
                                                    in_depth_search=config.in_depth_search)
        self.__test_searcher = TestFunctionsSearcher(test_functions_rules=config.function_rules)
        self.__executor = TestExecutor()

    def __execute_tests(self, tests):
        logger.log(f"Executing tests {tests}", Logger.__LOG_LEVEL_DEBUG__)
        self.__executor.execute(tests, self.__report_creator)

    def __search_config(self, path):
        return self.__config_loader.load(path)

    def report(self):
        return self.__report_creator.json_report()
