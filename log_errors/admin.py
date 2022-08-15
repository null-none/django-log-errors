import logging

from django.contrib import admin
from django.utils.html import format_html

from .models import LogError


class LogErrorAdmin(admin.ModelAdmin):
    list_display = ("colored_msg", "traceback", "date_format", "pathname")
    list_display_links = ("colored_msg",)
    list_filter = ("level",)

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = "green"
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = "orange"
        else:
            color = "red"
        return format_html(
            '<span style="color: {color};">{msg}</span>',
            color=color,
            msg=instance.source_file,
        )

    colored_msg.short_description = "Message"

    def traceback(self, instance):
        return format_html(
            "<pre><code>{content}</code></pre>",
            content=instance.stack_trace if instance.stack_trace else "",
        )

    def date_format(self, instance):
        return instance.date.strftime("%Y-%m-%d %X")

    date_format.short_description = "Created at"


admin.site.register(LogError, LogErrorAdmin)
