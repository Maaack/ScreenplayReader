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


class ImportedContent(BaseModel, RawText):
    class Meta:
        verbose_name = _('Imported Content')
        verbose_name_plural = _('Imported Contents')
        ordering = ["-created"]
        default_related_name = 'imported_contents'


class ParseOperation(BaseModel):
    class Meta:
        verbose_name = _('Parse Op')
        verbose_name_plural = _('Parse Ops')
        ordering = ["-created"]
        default_related_name = 'parse_operations'

    imported_content = models.ForeignKey('ImportedContent', models.CASCADE)

    def save(self, *args, **kwargs):
        self.run_operation()
        return super(ParseOperation, self).save(*args, **kwargs)

    def run_operation(self):
        if self.imported_content:
            self.blank_operation()

    def blank_operation(self):
        return None


class TextFormat(BaseModel):
    class Meta:
        verbose_name = _('Format')
        verbose_name_plural = _('Formats')
        ordering = ["-created"]
        default_related_name = 'formats'

    name = models.CharField(_("Name"), max_length=50, default='Format')
    description = models.TextField(_("Description"), blank=True, null=True)

    element_formats = models.ManyToManyField('ElementFormat')

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
