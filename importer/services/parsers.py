from abc import ABC, abstractmethod
import re


class LineParser:
    @staticmethod
    def get_type() -> str:
        return 'line'

    @staticmethod
    def parse(text):
        return text.splitlines()


class RegexParser(ABC):
    @staticmethod
    @abstractmethod
    def get_type() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_pattern() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_groups() -> tuple:
        pass

    @staticmethod
    def validate_result(result):
        return result

    @staticmethod
    def clean_text(text):
        return text.strip()

    # TODO: Make staticmethod
    # def static_match_to_group(match, groups):
    def match_to_group(self, match):
        result = []
        groups = self.get_groups()
        for group in groups:
            group_text = match.group(group[1])
            if group_text:
                clean_text = self.clean_text(group_text)
                result.append((group[0], clean_text))
        return result

    # TODO: Make staticmethod
    # def static_parse(text, pattern, groups, validate_method):
    def parse(self, text: str):
        pattern = self.get_pattern()
        match = re.search(pattern, text)
        if match:
            result = self.match_to_group(match)
            return self.validate_result(result)
        return None


class SlugRegexParser(RegexParser):
    GROUP_SLUG = 1

    GROUPS = (
            ('slug', GROUP_SLUG),
        )

    @staticmethod
    def get_type():
        return 'slug'

    @staticmethod
    def get_pattern():
        return r"^([A-Z]{1}[A-Z0-9\-\. \(\)\']*)$"

    @staticmethod
    def get_groups():
        return SlugRegexParser.GROUPS

    @staticmethod
    def validate_result(result):
        full_text = result[0][1]
        if re.search(r"((INT|EXT|EXT[/\\]INT|INT[/\\]EXT)\.+)", full_text):
            return None
        if re.search(r"(\(V\.O\.\)|\(O\.S\.\)|\(CONT'D\))", full_text):
            return None
        if not re.search(r"([a-z])", full_text):
            return None
        return RegexParser.validate_result(result)


class SettingRegexParser(RegexParser):
    GROUP_POSITION = 1
    GROUP_LOCATION = 3
    GROUP_TIME = 5

    GROUPS = (
            ('position', GROUP_POSITION),
            ('location', GROUP_LOCATION),
            ('time', GROUP_TIME)
        )

    @staticmethod
    def get_type():
        return 'setting'

    @staticmethod
    def get_pattern():
        return r"^((INT|EXT|EXT[\/\\]INT|INT[\/\\]EXT)\.+)([\w\s']*)(-\s?([\w\s']*))?$"

    @staticmethod
    def get_groups():
        return SettingRegexParser.GROUPS


class CharacterRegexParser(RegexParser):
    GROUP_FULL_TITLE = 1
    GROUP_HONORIFIC = 2
    GROUP_ROLE = 3
    GROUP_NUMBER = 5
    GROUP_POSITION = 6
    GROUP_CONTINUED = 7

    GROUPS = (
            ('full_title', GROUP_FULL_TITLE),
            ('honorific', GROUP_HONORIFIC),
            ('role', GROUP_ROLE),
            ('number', GROUP_NUMBER),
            ('position', GROUP_POSITION),
            ('continued', GROUP_CONTINUED)
        )

    @staticmethod
    def get_type():
        return 'character'

    @staticmethod
    def get_pattern():
        return r"^(([A-Z]{2,4}\.)? ?([A-Z\d\-\. ]{3,40})(#(\d+))? ?)(\(V\.O\.\)|\(O\.S\.\))? ?(\(CONT'D\))?$"

    @staticmethod
    def get_groups():
        return CharacterRegexParser.GROUPS

    @staticmethod
    def validate_result(result):
        honorific = result[1][1]
        full_title = result[0][1]
        if re.search(r"((INT|EXT|EXT[/\\]INT|INT[/\\]EXT)\.+)", honorific):
            return None
        if re.search(r"(FADE (IN|OUT)\.+)", full_title):
            return None
        if not re.search(r"(([^A-Za-z]*[A-Za-z][^A-Za-z]*){2,})", full_title):
            return None
        return RegexParser.validate_result(result)


class ActionDialogueRegexParser(RegexParser):
    GROUP_FULL_TEXT = 0

    GROUPS = (
            ('full_text', GROUP_FULL_TEXT),
        )

    @staticmethod
    def get_type():
        return 'action-dialogue'

    @staticmethod
    def get_pattern():
        return r"^(.+)$"

    @staticmethod
    def get_groups():
        return ActionDialogueRegexParser.GROUPS

    @staticmethod
    def validate_result(result):
        full_text = result[0][1]
        if re.search(SettingRegexParser.get_pattern(), full_text):
            return None
        elif re.search(CharacterRegexParser.get_pattern(), full_text):
            return None
        return RegexParser.validate_result(result)
