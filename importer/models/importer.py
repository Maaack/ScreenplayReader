from django.utils.translation import ugettext_lazy as _
from screenplayreader.mixins.models import *


class Import(TimeStampedOwnable):
    class Meta:
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ["-created"]
        default_related_name = 'imports'

    file = models.FileField(_("Uploaded File"), upload_to="imports/%Y/%m/%d/")


class ImportedContent(TimeStampedOwnable, RawText):
    class Meta:
        verbose_name = _('Imported Content')
        verbose_name_plural = _('Imported Contents')
        ordering = ["-created"]
        default_related_name = 'imported_contents'

