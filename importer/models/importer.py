from django.utils.translation import ugettext_lazy as _

from screenplayreader.mixins.models import *


class BaseModel(TimeStamped, Ownable):
    class Meta:
        abstract = True


class Import(BaseModel):
    class Meta:
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ["-created"]
        default_related_name = 'imports'

    file = models.FileField(_("Uploaded File"), upload_to="imports/%Y/%m/%d/")


class FileFormat(BaseModel):
    class Meta:
        verbose_name = _('Format')
        verbose_name_plural = _('Formats')
        ordering = ["-created"]
        default_related_name = 'formats'

    readable_name = models.CharField(_("Readable Name"), max_length=50)
    machine_name = models.CharField(_("Machine Name"), max_length=25)
    file_extension = models.CharField(_("File Extension"), default=".txt", max_length=10)
    description = models.TextField(_("Description"), blank=True)

    element_formats = models.ManyToManyField(
        'ElementFormat',
        through='FormatLink',
        through_fields=('file_format', 'element_format'),
    )

    def __str__(self):
        if self.readable_name:
            return str(self.readable_name[:25])
        elif self.machine_name:
            return str(self.machine_name[:25])
        else:
            return self.description[:25]


class ElementFormat(BaseModel):
    class Meta:
        verbose_name = _("Element Format")
        verbose_name_plural = _("Element Formats")
        ordering = ["-created"]

    name = models.CharField(_("Name"), max_length=25)
    regex_pattern = models.CharField(_("RegEx Pattern"), max_length=255)
    example = models.CharField(_("Example"), max_length=255)

    def __str__(self):
        return self.name


class FormatLink(BaseModel):
    class Meta:
        verbose_name = _("Format Link")
        verbose_name_plural = _("Format Links")
        ordering = ["-created"]
        default_related_name = 'format_links'

    file_format = models.ForeignKey('FileFormat')
    element_format = models.ForeignKey('ElementFormat')

    def __str__(self):
        return str(self.file_format)[:10] + " : " + str(self.element_format)[:10]
