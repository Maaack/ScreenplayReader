from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from importer.models import BaseModel, TextBlock, TextMatch, Screenplay, Scene, TitlePage, Location, Character, Line
from importer.services.parsers import SettingRegexParser, \
    CharacterRegexParser, ActionDialogueRegexParser, SlugRegexParser
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
            self.parse_slugs()
            self.parse_settings()
            self.parse_characters()
            self.parse_action_dialogue()

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
            text_match = TextMatch.objects.create(
                parse_operation=self,
                text_block=text_block,
                match_type=match_type,
                text=text
            )
            text_match.save_group_matches(match)

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
            self.interpret_lines()
            self.interpret_title_page()
            self.interpret_locations()
            self.interpret_characters()
            self.interpret_scenes()

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

    def get_text_match_setting_set(self):
        return self.get_text_match_set().filter(match_type=SettingRegexParser.get_type())

    def get_text_match_character_set(self):
        return self.get_text_match_set().filter(match_type=CharacterRegexParser.get_type())

    def get_title_page(self):
        if self.title_pages.count() == 0:
            self.interpret_title_page()
        return self.title_pages.all()

    def get_locations(self):
        if self.locations.count() == 0:
            self.interpret_locations()
        return self.locations.all()

    def get_characters(self):
        if self.characters.count() == 0:
            self.interpret_characters()
        return self.characters.all()

    def interpret_lines(self):
        screenplay = self.get_screenplay()
        text_blocks = self.get_text_blocks_set().all()
        for text_block in text_blocks:
            Line.objects.create(
                interpret_operation=self,
                screenplay=screenplay,
                index=text_block.index,
                text=text_block.text
            )

    def interpret_title_page(self):
        screenplay = self.get_screenplay()
        first_setting = self.get_text_match_setting_set().order_by('text_block__index').first()
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
            screenplay=screenplay,
            raw_title=title,
            raw_text=text,
        )

    def interpret_locations(self):
        screenplay = self.get_screenplay()
        settings_match = self.get_text_match_setting_set().filter(group_matches__group_type='location'). \
            values('group_matches__text').order_by('group_matches__text'). \
            annotate(occurrences=Count('group_matches__text')).order_by('-occurrences')
        for setting_match in settings_match:
            location = Location.objects.create(
                interpret_operation=self,
                screenplay=screenplay,
                raw_title=setting_match['group_matches__text'],
                occurrences=setting_match['occurrences']
            )
            location.lines.set(Line.objects.filter(text__icontains=location.title))
            location.save()

    def interpret_characters(self):
        screenplay = self.get_screenplay()
        characters_match = self.get_text_match_character_set().filter(group_matches__group_type='full_title'). \
            values('group_matches__text').order_by('group_matches__text'). \
            annotate(occurrences=Count('group_matches__text')).order_by('-occurrences')
        for character_match in characters_match:
            character = Character.objects.create(
                interpret_operation=self,
                screenplay=screenplay,
                raw_title=character_match['group_matches__text'],
                occurrences=character_match['occurrences']
            )
            character.lines.set(Line.objects.filter(text__icontains=character.title))
            character.save()

    def interpret_scenes(self):
        if self.characters and self.locations:
            screenplay = self.get_screenplay()
            for location in self.locations.all():
                Scene.objects.create(
                    interpret_operation=self,
                    screenplay=screenplay,
                    location=location
                )
