from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .utils import get_user_model_name

user_model_name = get_user_model_name()


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class Owned(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, models.CASCADE, verbose_name=_("Author"), related_name="%(class)ss")


class Ownable(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, models.SET_NULL, verbose_name=_("Author"), related_name="%(class)ss", blank=True, null=True)


class OneWayOwnable(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, models.SET_NULL, verbose_name=_("Author"), related_name="+", blank=True, null=True)


class RawTitle(models.Model):
    class Meta:
        abstract = True

    raw_title = models.CharField(_("Raw Title"), max_length=100)
    title = models.CharField(_("Title"), max_length=100, blank=True, null=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.raw_title.strip().capitalize()
        return super(RawTitle, self).save(*args, **kwargs)


class RawText(models.Model):
    class Meta:
        abstract = True

    raw_text = models.TextField(_("Raw Text"), blank=True, null=True, default='')
    text = models.TextField(_("Text"), blank=True, null=True, default='')
    snippet = models.CharField(_("Snippet"), max_length=25, blank=True, null=True, default='')

    def __str__(self):
        return self.snippet

    def save(self, *args, **kwargs):
        self.text = self.raw_text.strip()
        self.snippet = self.text[:25]
        return super(RawText, self).save(*args, **kwargs)


class TimeStampedOwnable(TimeStamped, Ownable):
    class Meta:
        abstract = True


class GenericOperation(TimeStampedOwnable):
    class Meta:
        abstract = True

    started = models.DateTimeField(_("Start Time"), null=True, editable=False)
    ended = models.DateTimeField(_("End Time"), null=True, editable=False)
    running = models.BooleanField(_("Running"), default=False, editable=False)
    milliseconds = models.FloatField(_("Runtime in milliseconds"), null=True, editable=False)

    def start_op(self):
        self.started = now()
        self.running = True
        self.ended = None
        self.milliseconds = 0
        self.save()

    def end_op(self):
        self.running = False
        self.ended = now()
        time_diff = self.ended - self.started
        self.milliseconds = time_diff.total_seconds() * 1000
        self.save()

    def run_operation(self):
        self.start_op()
        self.operation()
        self.end_op()

    def operation(self):
        pass
