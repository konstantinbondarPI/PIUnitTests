import fnmatch
import os

from PIUnitTests.Logger.Logger import *


class PythonFilesSearcher:

    def __init__(self, search_directories, rules, in_depth_search):
        if not search_directories:
            self.__search_directories = [os.getcwd()]
            logger.log("Added current dir if search_directories is empty", Logger.__LOG_LEVEL_DEBUG__)
        else:
            self.__search_directories = search_directories
        self.__rules = rules
        self.__in_depth_search = in_depth_search

    def search(self):
        files = []
        for start_directory in self.__search_directories:
            logger.log(f"Searching test files in {start_directory}", Logger.__LOG_LEVEL_DEBUG__)
            for file in self.__traverse_python_files(start_directory,
                                                     self.__in_depth_search):
                files.append(file)
        return files

    def __traverse_python_files(self, directory, recursively):
        if recursively:
            for root, _, files in os.walk(directory):
                yield from self.__extract_python_files(root, files)
        else:
            yield from self.__extract_python_files(directory, PythonFilesSearcher.__safe_listdir(directory))

    def __extract_python_files(self, root, files):
        for file in files:
            if file.endswith(".py") and self.__matches_file_name(file):
                yield os.path.join(root, file)

    def __matches_file_name(self, file):
        if not self.__rules:
            return True
        return any(fnmatch.filter([file], rule) for rule in self.__rules)

    @staticmethod
    def __safe_listdir(directory):
        try:
            return os.listdir(directory)
        except OSError as error:
            logger.log(f"Working directory error: {error}")
            return []
