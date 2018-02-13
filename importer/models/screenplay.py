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


class Line(BaseModel):
    class Meta:
        verbose_name = _('Line')
        verbose_name_plural = _('Lines')
        ordering = ["index"]
        default_related_name = 'lines'

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)
    screenplay = models.ForeignKey('Screenplay', models.CASCADE)
    index = models.IntegerField(_('Index'), db_index=True)
    text = models.TextField(_('Text'))

    def __str__(self):
        return self.text[0:25]


class TitlePage(BaseModel, RawTitle, RawText):
    class Meta:
        verbose_name = _("Title Page")
        verbose_name_plural = _("Title Pages")
        ordering = ["-created"]
        default_related_name = 'title_pages'

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)
    screenplay = models.ForeignKey('Screenplay', models.CASCADE)
    lines = models.ManyToManyField('Line')

    def __str__(self):
        return self.title


class Scene(BaseModel):
    class Meta:
        verbose_name = _("Scene")
        verbose_name_plural = _("Scenes")
        ordering = ["-created"]
        default_related_name = 'scenes'

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)
    screenplay = models.ForeignKey('Screenplay', models.CASCADE)
    location = models.ForeignKey('Location', models.CASCADE)
    characters = models.ManyToManyField('Character')
    lines = models.ManyToManyField('Line')


class CountedTitle(BaseModel, RawTitle):
    class Meta:
        abstract = True
    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)
    screenplay = models.ForeignKey('Screenplay', models.CASCADE)
    occurrences = models.PositiveIntegerField('Occurrences', db_index=True)
    lines = models.ManyToManyField('Line')

    def __str__(self):
        return self.title


class Location(CountedTitle):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["-created"]
        default_related_name = 'locations'


class Character(CountedTitle):
    class Meta:
        verbose_name = _("Character")
        verbose_name_plural = _("Characters")
        ordering = ["-created"]
        default_related_name = 'characters'
