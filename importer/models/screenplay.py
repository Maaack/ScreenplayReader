from django.utils.translation import ugettext_lazy as _

from .importer import BaseModel, RawText, RawTitle, models


class Screenplay(BaseModel, RawText):
    class Meta:
        verbose_name = _('Screenplay')
        verbose_name_plural = _('Screenplays')
        ordering = ["-created"]
        default_related_name = 'screenplays'

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)

    def __str__(self):
        return self.text[:25]


class TitlePage(BaseModel, RawTitle, RawText):
    class Meta:
        verbose_name = _("TitlePage")
        verbose_name_plural = _("TitlePages")
        ordering = ["-created"]

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)

    def __str__(self):
        return self.title
