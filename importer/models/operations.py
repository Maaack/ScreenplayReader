from django.utils.translation import ugettext_lazy as _

from importer.models import BaseModel, TextBlock, TextMatch, Screenplay, TitlePage
from importer.services.parsers import SettingRegexParser, CharacterRegexParser
from screenplayreader.mixins.models import *


class ParseOperation(BaseModel):
    PARSER_TYPE_SETTING = 'setting'
    PARSER_TYPE_CHARACTER = 'character'

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
        return TextBlock.objects.filter(parse_operation=self)

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

    def parse_text_blocks(self, match_type, parser_class):
        text_blocks = self.get_text_blocks()
        if text_blocks.count() > 0:
            parser = parser_class()
            for text_block in text_blocks:
                self.parse_text(match_type, text_block, parser)

    def parse_settings(self):
        self.parse_text_blocks(self.PARSER_TYPE_SETTING, SettingRegexParser)

    def parse_characters(self):
        self.parse_text_blocks(self.PARSER_TYPE_CHARACTER, CharacterRegexParser)


class InterpretOperation(BaseModel):
    TITLE_PAGE_MAX_BLOCKS = 40

    class Meta:
        verbose_name = _('Interpret Op')
        verbose_name_plural = _('Interpret Ops')
        ordering = ["-created"]
        default_related_name = 'interpret_operations'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)

    def save(self, *args, **kwargs):
        result_object = super(InterpretOperation, self).save(*args, **kwargs)
        self.run_operation()
        return result_object

    def run_operation(self):
        if self.parse_operation:
            self.interpret_title_page()
            self.interpret_locations()
            self.interpret_characters()

    def get_screenplay(self):
        if Screenplay.objects.filter(interpret_operation=self).count() == 0:
            content = self.parse_operation.imported_content.text
            Screenplay.objects.create(
                interpret_operation=self,
                raw_text=content,
            )
        return Screenplay.objects.filter(interpret_operation=self).first()

    def get_text_blocks_set(self):
        return TextBlock.objects.filter(parse_operation=self.parse_operation)

    def get_text_match_set(self):
        return TextMatch.objects.filter(parse_operation=self.parse_operation)

    def interpret_title_page(self):
        first_setting = self.get_text_match_set().filter(match_type=ParseOperation.PARSER_TYPE_SETTING).order_by('text_block__index').first()
        first_setting_index = min(first_setting.text_block.index, self.TITLE_PAGE_MAX_BLOCKS)
        first_text_blocks = self.get_text_blocks_set().order_by('index')[0:first_setting_index]
        title = None
        for text_block in first_text_blocks:
            text = text_block.text
            if text != '' and text is not None:
                title = text
                break

        text_query_set = first_text_blocks.values('text')
        text = "\n".join([dict_a['text'] for dict_a in text_query_set])
        TitlePage.objects.create(
            interpret_operation=self,
            raw_title=title,
            raw_text=text,
        )

    def interpret_locations(self):
        pass

    def interpret_characters(self):
        pass
