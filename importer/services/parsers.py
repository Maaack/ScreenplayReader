from abc import ABC, abstractmethod
import re


class RegexParser(ABC):
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

    def match_to_group(self, match):
        result = []
        groups = self.get_groups()
        for group in groups:
            group_text = match.group(group[1])
            if group_text:
                clean_text = self.clean_text(group_text)
                result.append((group[0], clean_text))
        return result

    def search(self, text: str):
        pattern = self.get_pattern()
        match = re.search(pattern, text)
        if match:
            result = self.match_to_group(match)
            return self.validate_result(result)
        return None


class SettingRegexParser(RegexParser):
    GROUP_POSITION = 'position'
    GROUP_LOCATION = 'location'
    GROUP_TIME = 'time'

    GROUPS = (
            (GROUP_POSITION, 1),
            (GROUP_LOCATION, 3),
            (GROUP_TIME, 5)
        )

    @staticmethod
    def get_pattern():
        return r"^((INT|EXT|EXT[\/\\]INT|INT[\/\\]EXT)\.+)([\w\s']*)(-\s?([\w\s']*))?$"

    @staticmethod
    def get_groups():
        return SettingRegexParser.GROUPS


class CharacterRegexParser(RegexParser):
    GROUP_FULL_TITLE = 'full_title'
    GROUP_HONORIFIC = 'honorific'
    GROUP_ROLE = 'role'
    GROUP_NUMBER = 'number'
    GROUP_POSITION = 'position'
    GROUP_CONTINUED = 'continued'

    GROUPS = (
            (GROUP_FULL_TITLE, 1),
            (GROUP_HONORIFIC, 2),
            (GROUP_ROLE, 3),
            (GROUP_NUMBER, 5),
            (GROUP_POSITION, 6),
            (GROUP_CONTINUED, 7)
        )

    @staticmethod
    def get_pattern():
        return r"^(([A-Z]{2,4}\.)? ?([A-Z\d\-\. ]{3,40})(#(\d+))? ?)(\(V\.O\.\)|\(O\.S\.\))? ?(\(CONT'D\))?$"

    @staticmethod
    def get_groups():
        return CharacterRegexParser.GROUPS

    @staticmethod
    def validate_result(result):
        honorific = result[1][1]
        if re.search(honorific, r"((INT|EXT|EXT[\/\\]INT|INT[\/\\]EXT)\.+)"):
            return None
        return RegexParser.validate_result(result)
