import json

from PIUnitTests.Config.SearchConfig import SearchConfig
from PIUnitTests.Logger.Logger import *


class ConfigLoader:
    __DEFAULT_CONFIG_PATH = "default_config.json"

    def load(self, config_path):
        if not config_path:
            config_path = self.__DEFAULT_CONFIG_PATH
            logger.log("Using default config path", Logger.__LOG_LEVEL_DEBUG__)
        return self.__try_to_parse_config(config_path)

    def __try_to_parse_config(self, path):
        try:
            with open(path, "r") as config_file:
                config = json.load(config_file)
                return SearchConfig(**config)
        except FileNotFoundError:
            logger.log(f"Config file not found {path}")
            if path == self.__DEFAULT_CONFIG_PATH:
                logger.log("Default config file not found")
                return ConfigLoader.__create_default_config()
            else:
                return self.__try_to_parse_config(self.__DEFAULT_CONFIG_PATH)

    @staticmethod
    def __create_default_config():
        logger.log("Loading hardcoded config")
        return SearchConfig(search_directories=[],
                            filename_rules=["*"],
                            function_rules=["test_"],
                            in_depth_search=False)
