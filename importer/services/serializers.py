from rest_framework import serializers
from importer.models import ImportedContent, TextMatch, GroupMatch, TextBlock, ParseOperation, InterpretOperation, Screenplay, \
    TitlePage, Location, Character, Scene, Line


class BaseModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        abstract = True
        fields = ('id', 'created', 'updated', 'user')

    user = serializers.ReadOnlyField(source='user.username')


class RawTitleSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ('id', 'raw_title', 'title')


class RawTextSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ('id', 'raw_text', 'text')


class ImportedContentSerializer(BaseModelSerializer):
    class Meta:
        model = ImportedContent
        fields = ('id', 'created', 'updated', 'user', 'raw_text', 'text')


class ParseOperationSerializer(BaseModelSerializer):
    class Meta:
        model = ParseOperation
        fields = ('id', 'created', 'updated', 'user', 'imported_content')


class InterpretOperationSerializer(BaseModelSerializer):
    class Meta:
        model = InterpretOperation
        fields = ('id', 'created', 'updated', 'user', 'parse_operation')


class TextBlockSerializer(BaseModelSerializer):
    class Meta:
        model = TextBlock
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'index', 'text', 'text_matches')


class TextMatchSerializer(BaseModelSerializer):
    class Meta:
        model = TextMatch
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'text_blocks', 'match_type', 'text',
                  'group_matches')


class GroupMatchSerializer(BaseModelSerializer):
    class Meta:
        model = GroupMatch
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'text_match', 'group_type', 'text')


class ScreenplaySerializer(BaseModelSerializer):
    class Meta:
        model = Screenplay
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation')


class LineSerializer(BaseModelSerializer):
    class Meta:
        model = Line
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'locations', 'characters',
                  'screenplay', 'index', 'text')


class TitlePageSerializer(BaseModelSerializer):
    class Meta:
        model = TitlePage
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'raw_text', 'text', 'lines')


class SceneSerializer(BaseModelSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'number', 'location',
                  'characters', 'location_name', 'location_text', 'position', 'time', 'character_names', 'scene_text')

    location_name = serializers.SerializerMethodField()
    character_names = serializers.SerializerMethodField()
    scene_text = serializers.SerializerMethodField()

    def get_location_name(self, scene):
        return scene.location.title

    def get_character_names(self, scene):
        return [character['title'] for character in scene.characters.values('title')]

    def get_scene_text(self, scene):
        return [line['text'] for line in scene.lines.values('text')]


class LocationSerializer(BaseModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'title',
                  'occurrences', 'lines')


class CharacterSerializer(BaseModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'title',
                  'occurrences', 'lines')
