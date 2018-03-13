from rest_framework import serializers
from interpreter.models import *

FIELDS_LIST_ID = ('id', )
FIELDS_LIST_TIMESTAMPED_OWNABLE = ('created', 'updated', 'user')
FIELDS_LIST_COMMON_OBJECT = FIELDS_LIST_ID + FIELDS_LIST_TIMESTAMPED_OWNABLE
FIELDS_LIST_GENERIC_OPERATION = FIELDS_LIST_COMMON_OBJECT + ('started', 'ended', 'running', 'milliseconds')
FIELDS_LIST_INTERPRET_OP_REL = FIELDS_LIST_COMMON_OBJECT + ('interpret_operation', )


class InterpretOperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterpretOperation
        fields = FIELDS_LIST_GENERIC_OPERATION + ('parse_operation', )


class ScreenplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Screenplay
        fields = FIELDS_LIST_INTERPRET_OP_REL


class LineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Line
        fields = FIELDS_LIST_INTERPRET_OP_REL + ('locations', 'characters', 'screenplay', 'index', 'text')


class TitlePageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TitlePage
        fields = FIELDS_LIST_INTERPRET_OP_REL + ('screenplay', 'raw_text', 'text', 'lines')


class SceneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scene
        fields = FIELDS_LIST_INTERPRET_OP_REL + ('screenplay', 'number', 'location', 'characters', 'location_name',
                                                 'position', 'time', 'character_names', 'scene_text')

    location_name = serializers.SerializerMethodField()
    character_names = serializers.SerializerMethodField()
    scene_text = serializers.SerializerMethodField()

    def get_location_name(self, scene):
        return scene.location.title

    def get_character_names(self, scene):
        return [character['title'] for character in scene.characters.values('title')]

    def get_scene_text(self, scene):
        return [line['text'] for line in scene.lines.values('text')]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = FIELDS_LIST_INTERPRET_OP_REL + ('screenplay', 'title', 'lines')


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Character
        fields = FIELDS_LIST_INTERPRET_OP_REL + ('screenplay', 'title', 'lines')
