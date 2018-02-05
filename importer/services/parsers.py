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

    def match_to_group(self, match):
        result = []
        groups = self.get_groups()
        for group in groups:
            result.append((group[0], match.group(group[1])))
        return result

    def search(self, text: str):
        pattern = self.get_pattern()
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return self.match_to_group(match)
        return None


class SettingRegexParser(RegexParser):
    GROUP_POSITION = 'position'
    GROUP_LOCATION = 'location'
    GROUP_TIME = 'time'

    @staticmethod
    def get_pattern():
        return r"^(int|ext|ext[\/\\]int|ext[\/\\]int)[\s\.]+([\w\s']*)(-\s?([\w\s']*))?$"

    @staticmethod
    def get_groups():
        return (
            (SettingRegexParser.GROUP_POSITION, 1),
            (SettingRegexParser.GROUP_LOCATION, 2),
            (SettingRegexParser.GROUP_TIME, 4)
        )
