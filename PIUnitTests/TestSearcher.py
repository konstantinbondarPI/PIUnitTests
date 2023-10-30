import fnmatch
import os
from dataclasses import dataclass


@dataclass
class SearchConfig:
    search_directories: list[str]
    filename_rules: list[str]
    function_rules: list[str]
    in_depth_search: bool = True
    only_matched_files_check: bool = False


def search_test_files(config: SearchConfig):
    files = []
    for start_directory in config.search_directories:
        for file in traverse_python_files(start_directory, config.in_depth_search):
            files.append(file)
    print("\n".join(files))
    return files


def traverse_python_files(directory, recursively):
    if recursively:
        for root, _, files in os.walk(directory):
            yield from extract_python_files(root, files)
    else:
        yield from extract_python_files(directory, os.listdir(directory))


def extract_python_files(root, files):
    for file in files:
        if file.endswith(".py"):
            yield os.path.join(root, file)