from rest_framework import serializers
from importer.models import *

FIELDS_LIST_ID = ('id', )
FIELDS_LIST_TIMESTAMPED_OWNABLE = ('created', 'updated', 'user')
FIELDS_LIST_COMMON_OBJECT = FIELDS_LIST_ID + FIELDS_LIST_TIMESTAMPED_OWNABLE
FIELDS_LIST_GENERIC_OPERATION = FIELDS_LIST_COMMON_OBJECT + ('started', 'ended', 'running', 'milliseconds')
FIELDS_LIST_RAW_TITLE = ('raw_title', 'title')
FIELDS_LIST_RAW_TEXT = ('raw_text', 'text')
FIELDS_LIST_PARSE_OP_REL = FIELDS_LIST_COMMON_OBJECT + ('parse_operation', )
FIELDS_LIST_INTERPRET_OP_REL = FIELDS_LIST_COMMON_OBJECT + ('interpret_operation', )


class ReadOnlyUserMixinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        abstract = True
        fields = FIELDS_LIST_COMMON_OBJECT

    user = serializers.ReadOnlyField(source='user.username')


class ImportedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedContent
        fields = FIELDS_LIST_COMMON_OBJECT + FIELDS_LIST_RAW_TEXT


class ParseOperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParseOperation
        fields = FIELDS_LIST_GENERIC_OPERATION + ('imported_content', )


class TextBlockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextBlock
        fields = FIELDS_LIST_PARSE_OP_REL + ('index', 'text', 'text_matches')


class TextMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextMatch
        fields = FIELDS_LIST_PARSE_OP_REL + ('text_blocks', 'match_type', 'text', 'group_matches')


class GroupMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupMatch
        fields = FIELDS_LIST_PARSE_OP_REL + ('text_match', 'group_type', 'text')

