from django.utils.translation import ugettext_lazy as _

from .importer import BaseModel, RawText, RawTitle, models


class Screenplay(BaseModel):
    class Meta:
        verbose_name = _('Screenplay')
        verbose_name_plural = _('Screenplays')
        ordering = ["-created"]
        default_related_name = 'screenplays'

    title_page = models.OneToOneField('TitlePage', models.SET_NULL, null=True)
    content = models.OneToOneField('Content', models.CASCADE)

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

    content = models.ForeignKey('Content', models.CASCADE)
    order = models.IntegerField(_("Order"), default=0, db_index=True)
    type = models.CharField(_("Type"), max_length=32)

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
