

class Logger:
    __LOG_LEVEL_NONE__ = 0
    __LOG_LEVEL_DEFAULT__ = 1
    __LOG_LEVEL_DEBUG__ = 2

    def __init__(self, downstream=print, log_level=__LOG_LEVEL_DEFAULT__):
        self.log_level = log_level
        self.__downstream = downstream

    def log(self, message, log_level=None):
        log_level = log_level or self.__LOG_LEVEL_DEFAULT__
        prefix = "🟢[DEFAULT]: "
        if log_level == self.__LOG_LEVEL_DEBUG__:
            prefix = "🟡[DEBUG]: "
        if log_level <= self.log_level:
            self.__downstream(prefix + message)


logger: Logger = Logger()


