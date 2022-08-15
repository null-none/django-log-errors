import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

LOG_LEVELS = (
    (logging.NOTSET, _("NotSet")),
    (logging.INFO, _("Info")),
    (logging.WARNING, _("Warning")),
    (logging.DEBUG, _("Debug")),
    (logging.ERROR, _("Error")),
    (logging.FATAL, _("Fatal")),
)


class LogError(models.Model):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    logger_name = models.CharField(max_length=100)
    level = models.CharField(max_length=255, blank=True)
    line = models.PositiveIntegerField(default=0)
    function = models.CharField(max_length=255, blank=True)
    pathname = models.CharField(max_length=1024, blank=True)
    http_method = models.CharField(max_length=128, blank=True)
    request_url = models.CharField(max_length=1024, blank=True)
    exception_type = models.CharField(max_length=256, blank=True)
    exception_value = models.CharField(max_length=512, blank=True)
    stack_trace = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return str(self.logger_name)

    class Meta:
        ordering = ("-date",)
        verbose_name_plural = verbose_name = "Log Errors"
        db_table = "log_errors_django"
