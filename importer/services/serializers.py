from rest_framework import serializers
from importer.models import *


class TimeStampedOwnableMixinSerializer(serializers.HyperlinkedModelSerializer):
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


class ImportedContentSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = ImportedContent
        fields = ('id', 'created', 'updated', 'user', 'raw_text', 'text')


class ParseOperationSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = ParseOperation
        fields = ('id', 'created', 'updated', 'user', 'imported_content')


class InterpretOperationSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = InterpretOperation
        fields = ('id', 'created', 'updated', 'user', 'parse_operation')


class TextBlockSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = TextBlock
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'index', 'text', 'text_matches')


class TextMatchSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = TextMatch
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'text_blocks', 'match_type', 'text',
                  'group_matches')


class GroupMatchSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = GroupMatch
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'text_match', 'group_type', 'text')


class ScreenplaySerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = Screenplay
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation')


class LineSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = Line
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'locations', 'characters',
                  'screenplay', 'index', 'text')


class TitlePageSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = TitlePage
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'raw_text', 'text', 'lines')


class SceneSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'number', 'location',
                  'characters', 'location_name', 'position', 'time', 'character_names', 'scene_text')

    location_name = serializers.SerializerMethodField()
    character_names = serializers.SerializerMethodField()
    scene_text = serializers.SerializerMethodField()

    def get_location_name(self, scene):
        return scene.location.title

    def get_character_names(self, scene):
        return [character['title'] for character in scene.characters.values('title')]

    def get_scene_text(self, scene):
        return [line['text'] for line in scene.lines.values('text')]


class LocationSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = Location
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'title',
                  'lines')


class CharacterSerializer(TimeStampedOwnableMixinSerializer):
    class Meta:
        model = Character
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'title',
                  'lines')
