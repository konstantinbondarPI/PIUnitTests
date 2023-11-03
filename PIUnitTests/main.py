import argparse
import json

from PIUnitTests.Config.SearchConfig import SearchConfig
from PIUnitTests.Logger.Logger import *
from PIUnitTests.PIUnitTestsRunner import PIUnitTestRunner


def setup_argument_parser():
    argument_parser = argparse.ArgumentParser(description="Unit test searcher and runner")

    required_group = argument_parser.add_mutually_exclusive_group(required=True)
    required_group.add_argument("--config", type=str, help="Mode with json config file")
    required_group.add_argument("--no-config", action="store_true", help="Mode with direct setting config values")

    no_config_group = argument_parser.add_argument_group("No config group")
    no_config_group.add_argument("--search-directories", nargs="+", help="Directories to search for tests")
    no_config_group.add_argument("--filename-rules", nargs="+", help="Rules to search for test files")
    no_config_group.add_argument("--function-rules", nargs="+", help="Rules to search for test functions inside file")
    no_config_group.add_argument("--in-depth-search", action="store_true", help="Enable in-depth search")

    argument_parser.add_argument("-d", action="store_true", help="Debug log level")
    argument_parser.add_argument("-s", action="store_true", help="Debug log level")

    return argument_parser


def main():
    parser = setup_argument_parser()

    args = parser.parse_args()

    if args.d:
        logger.log_level = Logger.__LOG_LEVEL_DEBUG__
    elif args.s:
        logger.log_level = Logger.__LOG_LEVEL_NONE__

    runner = PIUnitTestRunner()

    if args.config:
        runner.run(args.config)
    else:
        search_config = SearchConfig(
            search_directories=args.search_directories or [],
            filename_rules=args.filename_rules or ["*"],
            function_rules=args.function_rules or ["test_"],
            in_depth_search=args.in_depth_search
        )
        runner.run(config=search_config)

    json_report = runner.report()

    print(f"Report:\n{json_report}")


if __name__ == "__main__":
    main()
