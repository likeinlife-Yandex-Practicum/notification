import logging
from django.contrib import admin

from notifications.models import Notification, Template

logger = logging.getLogger(__name__)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'periodicity', 'start_at', 'finish_at', 'roles', 'template', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('subject',)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('slug', 'content', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('slug', )
