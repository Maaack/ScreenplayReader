from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from importer.models import TextBlock, TextMatch, GroupMatch, Screenplay, Scene, TitlePage, Location,\
    Character, Line
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


class InterpretOperation(GenericOperation):
    TITLE_PAGE_MAX_BLOCKS = 40
    current_scene_number = 0
    current_scene = None

    class Meta:
        verbose_name = _('Interpret Op')
        verbose_name_plural = _('Interpret Ops')
        ordering = ["-created"]
        default_related_name = 'interpret_operations'

    parse_operation = models.ForeignKey('ParseOperation', models.CASCADE)

    def __str__(self):
        return str(self.parse_operation)

    def operation(self):
        if self.parse_operation:
            self.interpret_lines()
            self.interpret_title_page()

    def get_screenplay(self):
        if Screenplay.objects.filter(interpret_operation=self).count() == 0:
            content = self.parse_operation.imported_content.text
            Screenplay.objects.create(
                interpret_operation=self,
                raw_text=content,
            )
        return Screenplay.objects.filter(interpret_operation=self).first()

    def get_text_blocks_set(self):
        return TextBlock.objects.filter(parse_operation=self.parse_operation).order_by('index')

    def get_title_page(self):
        if self.title_pages.count() == 0:
            self.interpret_title_page()
        return self.title_pages.all()

    def interpret_lines(self):
        screenplay = self.get_screenplay()
        text_blocks = self.get_text_blocks_set().all()
        for text_block in text_blocks:
            line = Line.objects.create(
                interpret_operation=self,
                screenplay=screenplay,
                index=text_block.index,
                text=text_block.text
            )
            line_object = self.interpret_text_block(text_block, screenplay)
            if line_object:
                line_object.lines.add(line)
            if self.current_scene:
                self.current_scene.lines.add(line)

    def interpret_title_page(self):
        screenplay = self.get_screenplay()
        first_lines = self.lines.order_by('index').all()[0:self.TITLE_PAGE_MAX_BLOCKS]
        title = None
        title_page_lines = []
        title_page_text = ''
        for line in first_lines:
            text = line.text
            if title is None and text is not None and text != '':
                title = text
            if len(title_page_lines) and (line.characters.count() or line.locations.count()):
                break
            title_page_lines.append(line)
            title_page_text += "\n" + text

        title_page = TitlePage.objects.create(
            interpret_operation=self,
            screenplay=screenplay,
            raw_title=title,
            raw_text=title_page_text,
        )
        title_page.lines.set(title_page_lines)

    def interpret_text_block(self, text_block, screenplay):
        if text_block.has_text_match(SettingRegexParser.get_type()):
            location = self.get_location_from_text_block(text_block, screenplay)
            self.get_scene_from_text_block(text_block, screenplay, location)
            return location
        elif text_block.has_text_match(CharacterRegexParser.get_type()):
            character = self.get_character_from_text_block(text_block, screenplay)
            if self.current_scene:
                self.current_scene.characters.add(character)
            return character
        return None

    def get_scene_from_text_block(self, text_block, screenplay, location):
        self.current_scene_number += 1
        position_text = text_block.get_group_match_text('position')
        time_text = text_block.get_group_match_text('time')
        self.current_scene = Scene.objects.create(
            interpret_operation=self,
            screenplay=screenplay,
            number=self.current_scene_number,
            location=location,
            position=position_text,
            time=time_text
        )

    def get_location_from_text_block(self, text_block, screenplay):
        return self.get_object_from_text_block(text_block, screenplay, 'location', Location)

    def get_character_from_text_block(self, text_block, screenplay):
        return self.get_object_from_text_block(text_block, screenplay, 'full_title', Character)

    def get_object_from_text_block(self, text_block, screenplay, get_type, object_class):
        type_text = text_block.get_group_match_text(get_type)
        new_object, created = object_class.objects.get_or_create(
            title=type_text,
            interpret_operation=self,
            screenplay=screenplay,
        )
        return new_object

