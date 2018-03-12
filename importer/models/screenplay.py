from django.utils.translation import ugettext_lazy as _
from screenplayreader.mixins.models import *


class Screenplay(TimeStampedOwnable, RawText):
    class Meta:
        verbose_name = _('Screenplay')
        verbose_name_plural = _('Screenplays')
        ordering = ["-created"]
        default_related_name = 'screenplays'

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)

    def __str__(self):
        return self.text[:25]


class Line(TimeStampedOwnable):
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


class TitlePage(TimeStampedOwnable, RawTitle, RawText):
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


class Scene(TimeStampedOwnable):
    class Meta:
        verbose_name = _("Scene")
        verbose_name_plural = _("Scenes")
        ordering = ["created"]
        default_related_name = 'scenes'

    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)
    screenplay = models.ForeignKey('Screenplay', models.CASCADE)
    number = models.PositiveIntegerField(_('Number'), db_index=True)
    characters = models.ManyToManyField('Character')
    location = models.ForeignKey('Location', models.CASCADE)
    position = models.CharField(_('Position'), max_length=25, blank=True, null=True)
    time = models.CharField(_("Time"), max_length=25, blank=True, null=True)
    lines = models.ManyToManyField('Line')


class ObjectTitle(TimeStampedOwnable):
    class Meta:
        abstract = True
    title = models.CharField(_("Title"), max_length=100)
    interpret_operation = models.ForeignKey('InterpretOperation', models.CASCADE)
    screenplay = models.ForeignKey('Screenplay', models.CASCADE)
    lines = models.ManyToManyField('Line')

    def __str__(self):
        return self.title[0:25]


class Location(ObjectTitle):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["created"]
        default_related_name = 'locations'


class Character(ObjectTitle):
    class Meta:
        verbose_name = _("Character")
        verbose_name_plural = _("Characters")
        ordering = ["created"]
        default_related_name = 'characters'
