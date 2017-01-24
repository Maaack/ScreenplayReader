from django.utils.translation import ugettext_lazy as _

from .importer import BaseModel, RawText, RawTitle, models


class Screenplay(BaseModel):
    class Meta:
        verbose_name = _('Screenplay')
        verbose_name_plural = _('Screenplays')
        ordering = ["-created"]
        default_related_name = 'screenplays'

    title_page = models.OneToOneField('TitlePage', null=True)
    content = models.OneToOneField('Content')

    def __str__(self):
        try:
            return str(self.title_page)
        except TitlePage.DoesNotExist:
            return str(self.content)


class TitlePage(BaseModel, RawTitle, RawText):
    class Meta:
        verbose_name = _("TitlePage")
        verbose_name_plural = _("TitlePages")
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Content(BaseModel, RawText):
    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")
        ordering = ["-created"]
        default_related_name = 'contents'

    def __str__(self):
        return self.text[:25]


class ContentElement(BaseModel, RawText):
    class Meta:
        verbose_name = _("Content Element")
        verbose_name_plural = _("Content Elements")
        ordering = ["-created"]
        default_related_name = 'content_elements'

    content = models.ForeignKey('Content')
    order = models.IntegerField(_("Order"), default=0, db_index=True)

    def save(self, *args, **kwargs):
        from django.db.models import F
        if self.order is None or not self.order:
            last_time = self.content.content_elements.order_by('-order').first()
            self.order = last_time.order + 1
        else:
            conflicting_time = self.content.content_elements.filter(order=self.order).exists()
            if conflicting_time:
                self.timeline.time_links.filter(order__gte=self.order).update(order=F('order') + 1)
        return super(ContentElement, self).save(*args, **kwargs)


class SceneHeading(ContentElement):
    class Meta:
        verbose_name = _("Scene Heading")
        verbose_name_plural = _("Scene Headings")
        ordering = ["-created"]
        default_related_name = 'scene_headings'


class Transition(ContentElement):
    class Meta:
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")
        ordering = ["-created"]
        default_related_name = 'transitions'


class Dialogue(ContentElement):
    class Meta:
        verbose_name = _("Dialogue")
        verbose_name_plural = _("Dialogues")
        ordering = ["-created"]
        default_related_name = 'dialogues'


class Action(ContentElement):
    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")
        ordering = ["-created"]
        default_related_name = 'actions'


class Parenthetical(ContentElement):
    class Meta:
        verbose_name = _("Parenthetical")
        verbose_name_plural = _("Parentheticals")
        ordering = ["-created"]
        default_related_name = 'parentheticals'


class Character(ContentElement):
    class Meta:
        verbose_name = _("Character")
        verbose_name_plural = _("Characters")
        ordering = ["-created"]
        default_related_name = 'characters'


class Intercut(ContentElement):
    class Meta:
        verbose_name = _("Intercut")
        verbose_name_plural = _("Intercuts")
        ordering = ["-created"]
        default_related_name = 'intercuts'


class MoreText(ContentElement):
    class Meta:
        verbose_name = _("More Text")
        verbose_name_plural = _("More Texts")
        ordering = ["-created"]
        default_related_name = 'more_texts'


class ContinuedText(ContentElement):
    class Meta:
        verbose_name = _("Continued Text")
        verbose_name_plural = _("Continued Texts")
        ordering = ["-created"]
        default_related_name = 'continued_texts'


class Unclassified(ContentElement):
    class Meta:
        verbose_name = _("Unclassified")
        verbose_name_plural = _("Unclassifieds")
        ordering = ["-created"]
        default_related_name = 'unclassifieds'
