from abc import ABC, abstractmethod
from django.db.models import Count
from importer.models import Screenplay, TitlePage, Location
from importer.services.parsers import SettingRegexParser


class BaseInterpreter(ABC):
    @staticmethod
    @abstractmethod
    def get_type() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_class():
        pass

    @abstractmethod
    def interpret(self, parse_operation, interpret_operation):
        pass


class ScreenplayInterpreter(BaseInterpreter):
    @staticmethod
    def get_type():
        return 'screenplay'

    @staticmethod
    def get_class():
        return Screenplay

    def interpret(self, parse_operation, interpret_operation):
        if Screenplay.objects.filter(interpret_operation=interpret_operation).count() == 0:
            content = parse_operation.imported_content.text
            Screenplay.objects.create(
                interpret_operation=self,
                raw_text=content,
            )
        return Screenplay.objects.filter(interpret_operation=interpret_operation).first()


class TitlePageInterpreter(BaseInterpreter):
    TITLE_PAGE_MAX_BLOCKS = 40

    @staticmethod
    def get_type():
        return 'title-page'

    @staticmethod
    def get_class():
        return TitlePage

    def interpret(self, parse_operation, interpret_operation):
        try:
            screenplay = interpret_operation.screenplays.all()[0]
            text_blocks = parse_operation.text_blocks
            text_matches = parse_operation.text_matches
        except AttributeError:
            return None

        match_type = SettingRegexParser.get_type()
        first_setting = text_matches.filter(match_type=match_type).order_by('text_block__index').first()
        first_setting_index = min(first_setting.text_block.index, self.TITLE_PAGE_MAX_BLOCKS)
        first_text_blocks = text_blocks.order_by('index')[0:first_setting_index]
        title = None
        for text_block in first_text_blocks:
            text = text_block.text
            if text != '' and text is not None:
                title = text
                break

        text_query_set = first_text_blocks.values('text')
        text = "\n".join([dict_a['text'] for dict_a in text_query_set])
        TitlePage.objects.create(
            interpret_operation=interpret_operation,
            screenplay=screenplay,
            raw_title=title,
            raw_text=text,
        )


class LocationInterpreter(BaseInterpreter):
    TITLE_PAGE_MAX_BLOCKS = 40

    @staticmethod
    def get_type():
        return 'location'

    @staticmethod
    def get_class():
        return Location

    def interpret(self, parse_operation, interpret_operation):
        try:
            screenplay = interpret_operation.screenplays.all()[0]
            text_blocks = parse_operation.text_blocks
            text_matches = parse_operation.text_matches
        except AttributeError:
            return None

        match_type = SettingRegexParser.get_type()
        settings_match = text_matches.filter(match_type=match_type).filter(group_matches__group_type='location'). \
            values('group_matches__text').order_by('group_matches__text'). \
            annotate(occurrences=Count('group_matches__text')).order_by('-occurrences')
        for setting_match in settings_match:
            Location.objects.create(
                interpret_operation=self,
                screenplay=screenplay,
                raw_title=setting_match['group_matches__text'],
                occurrences=setting_match['occurrences']
            )