import json
from dataclasses import dataclass

from PIUnitTests.Logger.Logger import *


@dataclass(frozen=True)
class ReportItem:
    test_name: str
    is_succeed: bool
    time: float


class ReportItemEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ReportItem):
            # Convert ReportItem object to a dictionary
            return {"test_name": o.test_name, "is_succeed": o.is_succeed, "time": f"{o.time:.3f}"}
        return super().default(o)


class ReportCreator:

    def __init__(self):
        self.__report = {}

    def add(self, test_suite, test_name, is_succeed, time):
        logger.log(f"Added to report {test_name, is_succeed}", Logger.__LOG_LEVEL_DEBUG__)
        if test_suite not in self.__report:
            self.__report[test_suite] = []
        self.__report[test_suite].append(ReportItem(test_name, is_succeed, time))

    def json_report(self):
        return json.dumps(self.__report, cls=ReportItemEncoder, indent=4)
