from django.utils.translation import ugettext_lazy as _

from importer.models import BaseModel, TextBlock, TextMatch
from importer.services.parsers import SettingRegexParser, CharacterRegexParser
from screenplayreader.mixins.models import *


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
            self.parse_characters()

    def get_text_blocks(self):
        if TextBlock.objects.filter(parse_operation=self).count() == 0:
            self.split_text()
        return TextBlock.objects.filter(parse_operation=self).all()

    def split_text(self):
        if self.imported_content.raw_text:
            split_text = self.imported_content.raw_text.splitlines()
            for index, line in enumerate(split_text):
                TextBlock.objects.create(
                    imported_content=self.imported_content,
                    parse_operation=self,
                    index=index,
                    text=line
                ).save()

    def parse_text(self, match_type, text_block, parser):
        text = text_block.text
        match = parser.search(text)
        if match:
            text_match = TextMatch.objects.create(
                parse_operation=self,
                text_block=text_block,
                match_type=match_type,
                text=text
            )
            text_match.save_group_matches(match)
            text_match.save()

    def parse_text_blocks(self, match_type, parser_class):
        text_blocks = self.get_text_blocks()
        if text_blocks.count() > 0:
            parser = parser_class()
            for text_block in text_blocks:
                self.parse_text(match_type, text_block, parser)

    def parse_settings(self):
        self.parse_text_blocks('setting', SettingRegexParser)

    def parse_characters(self):
        self.parse_text_blocks('character', CharacterRegexParser)
