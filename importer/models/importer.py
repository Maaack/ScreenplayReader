from django.utils.translation import ugettext_lazy as _

from screenplayreader.mixins.models import *
from importer.services.parsers import SettingRegexParser


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
        result_object = super(ParseOperation, self).save(*args, **kwargs)
        self.run_operation()
        return result_object

    def run_operation(self):
        if self.imported_content:
            self.parse_settings()

    def get_split_text(self):
        if self.imported_content.raw_text:
            return self.imported_content.raw_text.splitlines()
        return None

    def parse_settings(self):
        split_text = self.get_split_text()
        if split_text:
            parser = SettingRegexParser()
            for index, line in enumerate(split_text):
                match = parser.search(line)
                if match:
                    text_match = TextMatch.objects.create(
                        parse_operation=self,
                        index=index,
                        type='setting',
                        text=line
                    )
                    text_match.add_group_matches(match)
                    text_match.save()


class TextMatch(BaseModel):
    class Meta:
        verbose_name = _('Text Match')
        verbose_name_plural = _('Text Matches')
        ordering = ["-created"]
        default_related_name = 'text_matches'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    index = models.IntegerField(_('Index'), db_index=True)
    type = models.CharField(_('Type'), max_length=25, db_index=True)
    text = models.TextField(_('Text'))

    def add_group_matches(self, group_matches):
        for group_match in group_matches:
            if group_match[1]:
                GroupMatch.objects.create(
                            parse_operation=self.parse_operation,
                            text_match=self,
                            type=group_match[0],
                            text=group_match[1]
                )


class GroupMatch(BaseModel):
    class Meta:
        verbose_name = _('Group Match')
        verbose_name_plural = _('Group Matches')
        ordering = ["-created"]
        default_related_name = 'group_matches'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    text_match = models.ForeignKey('TextMatch', models.CASCADE)
    type = models.CharField('Type', max_length=25)
    text = models.TextField(_('Text'))


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
        if self.name:
            return str(self.name[:25])
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
