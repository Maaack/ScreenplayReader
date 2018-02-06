from rest_framework import serializers
from . import ImportedContent, TextMatch, GroupMatch, TextBlock, ParseOperation, InterpretOperation, Screenplay, TitlePage


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
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'index', 'text')


class TextMatchSerializer(BaseModelSerializer):
    class Meta:
        model = TextMatch
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'text_block', 'match_type', 'text')


class GroupMatchSerializer(BaseModelSerializer):
    class Meta:
        model = GroupMatch
        fields = ('id', 'created', 'updated', 'user', 'parse_operation', 'text_match', 'group_type', 'text')


class ScreenplaySerializer(BaseModelSerializer):
    class Meta:
        model = Screenplay
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation')


class TitlePageSerializer(BaseModelSerializer):
    class Meta:
        model = TitlePage
        fields = ('id', 'created', 'updated', 'user', 'interpret_operation', 'screenplay', 'raw_text', 'text')

