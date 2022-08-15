django-log-errors
=================

Django Log Viewer allows you to read & download log files in the admin page


Installation
------------

    pip install django-log-errors


Example
------------

Add app in your ``settings.py``

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
        },
        "handlers": {
            "db_log": {"level": "DEBUG", "class": "log_errors.handler.DatabaseLogHandler"},
        },
        "loggers": {
            "django": {
                "handlers": ["db_log"],
                "level": "ERROR",
                "propagate": False,
            },
        }
    }   