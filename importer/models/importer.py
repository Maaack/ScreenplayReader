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


# TODO: Delete or use this
class TextFormat(TimeStampedOwnable):
    class Meta:
        verbose_name = _('Format')
        verbose_name_plural = _('Formats')
        ordering = ["-created"]
        default_related_name = 'formats'

    name = models.CharField(_("Name"), max_length=50, default='Format')
    description = models.TextField(_("Description"), blank=True, null=True)

    element_formats = models.ManyToManyField('ElementFormat')

    def __str__(self):
        if self.name:
            return str(self.name[:25])
        else:
            return self.description[:25]


# TODO: Delete or use this
class ElementFormat(TimeStampedOwnable):
    class Meta:
        verbose_name = _("Element Format")
        verbose_name_plural = _("Element Formats")
        ordering = ["-created"]

    name = models.CharField(_("Name"), max_length=25)
    regex_pattern = models.CharField(_("RegEx Pattern"), max_length=255)
    example = models.CharField(_("Example"), max_length=255)

    def __str__(self):
        return self.name
