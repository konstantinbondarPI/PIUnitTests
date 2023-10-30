import fnmatch
import os
from . import SearchConfig


class PythonFilesSearcher:

    def __init__(self, config: SearchConfig):
        self.__config = config

    def search(self):
        files = []
        for start_directory in self.__config.search_directories:
            for file in self.__traverse_python_files(start_directory,
                                                     self.__config.in_depth_search,
                                                     self.__config.filename_rules):
                files.append(file)
        return files

    def __traverse_python_files(self, directory, recursively, rules):
        if recursively:
            for root, _, files in os.walk(directory):
                yield from self.__extract_python_files(root, files)
        else:
            yield from self.__extract_python_files(directory, os.listdir(directory))

    def __extract_python_files(self, root, files):
        for file in files:
            if file.endswith(".py") and self.__matches_file_name(file):
                yield os.path.join(root, file)

    def __matches_file_name(self, file):
        if not self.__config.filename_rules:
            return True
        return any(fnmatch.filter([file], rule) for rule in self.__config.filename_rules)
