import uuid
from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True, db_default=Now())
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True, db_default=Now())

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Template(TimeStampedMixin):
    slug = models.SlugField(_("slug"), max_length=64, primary_key=True)
    content = models.TextField(_("content"))
    params = ArrayField(
        models.CharField(max_length=64, null=True),
        verbose_name=_("params"),
        default=list,
        blank=True,
    )

    class Meta:
        db_table = 'public"."template'
        verbose_name = _("Template")
        verbose_name_plural = _("Template")

    def __str__(self):
        return self.slug


class Notification(UUIDMixin, TimeStampedMixin):
    template = models.ForeignKey(
        "Template",
        on_delete=models.CASCADE,
        verbose_name=_("template"),
    )
    subject = models.CharField(_("subject"), max_length=64)
    periodicity = models.DurationField(_("periodicity"), default=timedelta(days=7))
    start_at = models.DateTimeField(_("start_at"))
    finish_at = models.DateTimeField(_("finish_at"))
    roles = ArrayField(
        models.CharField(max_length=64),
        help_text=_("User roles. For example: admin, user, subscriber"),
        verbose_name=_("roles"),
    )

    class Meta:
        db_table = 'public"."notification'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notification")

    def __str__(self):
        return self.subject


class NotificationStatusEnum(models.TextChoices):
    PENDING = "PG", _("Pending")
    OK = "OK", _("Ok")
    ERROR = "ER", _("Error")


class NotificationStatus(UUIDMixin, TimeStampedMixin):
    task_id = models.UUIDField(_("task_id"), editable=False)
    subject = models.CharField(_("subject"), max_length=64)
    status = models.CharField(
        _("status"),
        max_length=2,
        choices=NotificationStatusEnum.choices,
        default=NotificationStatusEnum.PENDING,
    )
    description = models.TextField(_("description"), null=True)

    class Meta:
        db_table = 'public"."notification_status'
        verbose_name = _("Notification Status")
        verbose_name_plural = _("Notification Status")

    def __str__(self):
        return self.subject
