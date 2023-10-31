import importlib.util
import inspect
import time


class TestExecutor:
    def __init__(self, test_cases):
        self.__test_cases = test_cases

    def execute(self):
        for filename in self.__test_cases.keys():
            test_names = self.__test_cases[filename]
            module, module_name = self.__load_module(filename)

            for name in test_names:
                if not self.__try_to_extract_func_and_execute(module, name, module_name):
                    for _, obj in inspect.getmembers(module):
                        if inspect.isclass(obj):
                            instance = None
                            try:
                                instance = obj()
                            except TypeError as type_error:
                                print(f"Failed to instantiate an class object with tests (required params) {repr(obj)} {type_error}")
                                continue

                            if hasattr(instance, name) and callable(getattr(instance, name)):
                                self.__try_to_extract_func_and_execute(instance, name, module_name)

    @staticmethod
    def __load_module(filename):
        module_name = inspect.getmodulename(filename)
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module, module_name

    def __try_to_extract_func_and_execute(self, obj, name, module_name):
        func = getattr(obj, name, None)
        if func:
            self.__executing_test_decorator(func, module_name)
            return True
        else:
            return False

    @staticmethod
    def __executing_test_decorator(fun, filename):
        print("\n------------------")
        print(f"Executing test: {fun.__name__} from: {filename}.py")
        start_time = time.time()
        try:
            fun()
            print("Succeed")
        except AssertionError as assert_error:
            error_message = f"with assert message: \'{assert_error}\'" if assert_error.args else ""
            print(f"Failed {error_message}")
        except TypeError as type_error:
            print(f"Failed (not a test) {type_error}")

        print(f"Time elapsed: {(time.time() - start_time):.2f}")
        print("------------------\n")
