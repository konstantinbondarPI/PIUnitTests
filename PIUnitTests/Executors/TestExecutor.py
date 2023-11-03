import importlib.util
import inspect
import os
import sys
import time

from PIUnitTests.Report.ReportCreator import ReportCreator

from PIUnitTests.Logger.Logger import *


class TestExecutor:

    def execute(self, test_cases, report_creator: ReportCreator):
        for filename in test_cases.keys():
            test_names = test_cases[filename]

            TestExecutor.log_start_executing(filename)

            module, module_name = self.__load_module(filename)

            logger.log(f"Searching functions in {module}", Logger.__LOG_LEVEL_DEBUG__)
            for name in test_names:
                if not self.__try_to_extract_func_and_execute(module, name, module_name, report_creator):
                    for _, obj in inspect.getmembers(module):
                        if inspect.isclass(obj):
                            logger.log(f"Function inside class: {obj}", Logger.__LOG_LEVEL_DEBUG__)
                            instance = None
                            try:
                                instance = obj()
                            except TypeError as type_error:
                                logger.log(f"Failed to instantiate an class object with tests (required params) {repr(obj)} {type_error}")
                                continue

                            if hasattr(instance, name) and callable(getattr(instance, name)):
                                self.__try_to_extract_func_and_execute(instance, name, module_name, report_creator)

            TestExecutor.log_end_executing()

    @staticmethod
    def __load_module(filename):

        current_dir = os.path.dirname(os.path.abspath(filename))
        # Add the current directory to sys.path to allow dynamic imports
        sys.path.append(current_dir)
        logger.log(f"Appending module dir to sys.path: {current_dir}", Logger.__LOG_LEVEL_DEBUG__)

        module_name = inspect.getmodulename(filename)
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)
        logger.log(f"Running module {module}", Logger.__LOG_LEVEL_DEBUG__)

        return module, module_name

    def __try_to_extract_func_and_execute(self, obj, name, module_name, report_creator):
        func = getattr(obj, name, None)
        if func:
            self.__executing_test_decorator(func, module_name, report_creator)
            return True
        else:
            return False

    @staticmethod
    def __executing_test_decorator(fun, module_name, report_creator: ReportCreator):
        start_time = time.time()
        result_message = f"{fun.__name__} - "
        is_succeed = False
        try:
            fun()
            result_message += "Succeed"
            is_succeed = True
        except AssertionError as assert_error:
            error_message = f"with assert message: \'{assert_error}\'" if assert_error.args else ""
            result_message += f"Failed {error_message}"
        except TypeError as type_error:
            result_message += f"Failed (not a test) {type_error}"

        delta = time.time() - start_time
        if delta > 0.0009:
            result_message += f": {delta:.3f}s"

        report_creator.add(module_name + ".py", fun.__name__, is_succeed, delta)

        logger.log(result_message)

    @staticmethod
    def log_start_executing(filename):
        logger.log("˅------------------˅")
        logger.log(f"Executing tests from: {inspect.getmodulename(filename)}.py")

    @staticmethod
    def log_end_executing():
        logger.log("^------------------^\n")