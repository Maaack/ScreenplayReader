from django.db import models
from django.utils.translation import ugettext_lazy as _

from importer.models import BaseModel


class TextBlock(BaseModel):
    class Meta:
        verbose_name = _('Text Block')
        verbose_name_plural = _('Text Blocks')
        ordering = ["-created"]
        default_related_name = 'text_blocks'

    imported_content = models.ForeignKey('ImportedContent', models.CASCADE)
    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    index = models.IntegerField(_('Index'), db_index=True)
    text = models.TextField(_('Text'))


class TextMatch(BaseModel):
    class Meta:
        verbose_name = _('Text Match')
        verbose_name_plural = _('Text Matches')
        ordering = ["-created"]
        default_related_name = 'text_matches'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    text_block = models.ForeignKey('TextBlock', models.CASCADE)
    match_type = models.CharField(_('Type'), max_length=25, db_index=True)
    text = models.TextField(_('Text'))

    def save_group_matches(self, group_matches):
        for group_match in group_matches:
            if group_match[1]:
                GroupMatch.objects.create(
                    parse_operation=self.parse_operation,
                    text_match=self,
                    group_type=group_match[0],
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
    group_type = models.CharField(_('Type'), max_length=25, db_index=True)
    text = models.TextField(_('Text'))
