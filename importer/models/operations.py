from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from importer.models import TextBlock, TextMatch
from importer.services.parsers import SettingRegexParser, \
    CharacterRegexParser, ActionDialogueRegexParser, SlugRegexParser
from screenplayreader.mixins.models import *


class ParseOperation(GenericOperation):
    class Meta:
        verbose_name = _('Parse Op')
        verbose_name_plural = _('Parse Ops')
        ordering = ["-created"]
        default_related_name = 'parse_operations'

    imported_content = models.ForeignKey('ImportedContent', models.CASCADE)

    def __str__(self):
        return str(self.imported_content)

    def operation(self):
        if self.imported_content:
            # self.parse_slugs()
            self.parse_settings()
            self.parse_characters()
            # self.parse_action_dialogue()

    def get_text_blocks(self):
        if self.text_blocks.count() == 0:
            self.split_text()
        return self.text_blocks.all()

    def split_text(self):
        if self.imported_content.raw_text:
            split_text = self.imported_content.raw_text.splitlines()
            for index, line in enumerate(split_text):
                TextBlock.objects.create(
                    imported_content=self.imported_content,
                    parse_operation=self,
                    index=index,
                    text=line
                )

    def parse_text(self, text_block, parser):
        match_type = parser.get_type()
        text = text_block.text
        match = parser.parse(text)
        if match:
            text_match, created = TextMatch.objects.get_or_create(
                parse_operation=self,
                match_type=match_type,
                text=text
            )
            if created:
                pass
                text_match.save_group_matches(match)
            text_match.text_blocks.add(text_block)

    def parse_text_blocks(self, parser_class):
        text_blocks = self.get_text_blocks()
        if text_blocks.count() > 0:
            parser = parser_class()
            for text_block in text_blocks:
                self.parse_text(text_block, parser)

    def parse_slugs(self):
        self.parse_text_blocks(SlugRegexParser)

    def parse_settings(self):
        self.parse_text_blocks(SettingRegexParser)

    def parse_characters(self):
        self.parse_text_blocks(CharacterRegexParser)

    def parse_action_dialogue(self):
        self.parse_text_blocks(ActionDialogueRegexParser)
