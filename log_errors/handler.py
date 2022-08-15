import re
import logging
import traceback


db_default_formatter = logging.Formatter()


class DatabaseLogHandler(logging.Handler):
    def log_level(self, levelno):
        logs = {}
        logs[logging.NOTSET] = "NotSet"
        logs[logging.INFO] = "Info"
        logs[logging.WARNING] = "Warning"
        logs[logging.DEBUG] = "Debug"
        logs[logging.ERROR] = "Error"
        logs[logging.FATAL] = "Fatal"
        return logs[levelno]

    def emit(self, record):
        from .models import LogError

        line = 0
        pathname = record.pathname
        function = ""

        if len(record.exc_info) >= 2:
            trace = db_default_formatter.formatException(record.exc_info)
            trace_parse = traceback.format_tb(record.exc_info[2]).pop()
            result = re.findall(r".*, line (\d+), in .*", trace_parse)
            if len(result) > 0:
                line = int(result[0])
            result = re.findall(r'.* File "(.*)", line .*', trace_parse)
            if len(result) > 0:
                pathname = result[0]
            result = re.findall(r".*, in (.*)", trace_parse)
            if len(result) > 0:
                function = result[0]
            if hasattr(record, "request"):
                kwargs = {
                    "logger_name": record.name,
                    "level": self.log_level(record.levelno),
                    "pathname": pathname,
                    "line": line,
                    "function": function,
                    "http_method": record.request.method,
                    "request_url": record.request.path,
                    "exception_type": record.exc_info[0].__name__,
                    "exception_value": str(record.exc_info[1]),
                    "stack_trace": trace,
                }
                if record.request.user.is_authenticated:
                    kwargs["user"] = record.request.user
            else:
                kwargs = {
                    "logger_name": record.name,
                    "level": self.log_level(record.levelno),
                    "pathname": pathname,
                    "line": line,
                    "function": function,
                    "exception_type": record.exc_info[0].__name__,
                    "exception_value": str(record.exc_info[1]),
                    "stack_trace": trace,
                }
            LogError.objects.create(**kwargs)
