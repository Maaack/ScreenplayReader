from django.utils.translation import ugettext_lazy as _
from screenplayreader.mixins.models import *


class TextBlock(TimeStampedOwnable):
    class Meta:
        verbose_name = _('Text Block')
        verbose_name_plural = _('Text Blocks')
        ordering = ["-created"]
        default_related_name = 'text_blocks'

    imported_content = models.ForeignKey('ImportedContent', models.CASCADE)
    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    index = models.IntegerField(_('Index'), db_index=True)
    text = models.TextField(_('Text'))

    def __str__(self):
        return self.text[0:25]

    def get_text_match(self, text_match_type):
        return self.text_matches.filter(match_type=text_match_type).first()

    def has_text_match(self, text_match_type):
        return bool(self.get_text_match(text_match_type))

    def get_group_match_text(self, group_match_type):
        try:
            return self.text_matches.filter(group_matches__group_type=group_match_type)\
                .values('group_matches__text').first()['group_matches__text']
        except TypeError:
            pass
        return None


class TextMatch(TimeStampedOwnable):
    class Meta:
        verbose_name = _('Text Match')
        verbose_name_plural = _('Text Matches')
        ordering = ["-created"]
        default_related_name = 'text_matches'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    text_blocks = models.ManyToManyField('TextBlock')
    match_type = models.CharField(_('Type'), max_length=25, db_index=True)
    text = models.TextField(_('Text'))

    def save_group_matches(self, group_matches):
        if self.group_matches.count() > 0:
            return
        for group_match in group_matches:
            if group_match[1]:
                self.group_matches.create(
                    parse_operation=self.parse_operation,
                    group_type=group_match[0],
                    text=group_match[1]
                )

    def __str__(self):
        return self.text[0:25]

    def get_group_match(self, group_match_type):
        return self.group_matches.filter(group_type=group_match_type).first()

    def has_group_match(self, group_match_type):
        return bool(self.get_group_match(group_match_type))


class GroupMatch(TimeStampedOwnable):
    class Meta:
        verbose_name = _('Group Match')
        verbose_name_plural = _('Group Matches')
        ordering = ["-created"]
        default_related_name = 'group_matches'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)
    text_match = models.ForeignKey('TextMatch', models.CASCADE)
    group_type = models.CharField(_('Type'), max_length=25, db_index=True)
    text = models.TextField(_('Text'))

    def __str__(self):
        return self.text[0:25]

