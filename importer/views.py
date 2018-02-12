# Create your views here.

from screenplayreader.mixins.views import BaseViewSet
from .models.serializers import *
from .services.pagination import StandardResultsSetPagination


# Create your views here.
class ImportedContentViewSet(BaseViewSet):
    queryset = ImportedContent.objects.all()
    serializer_class = ImportedContentSerializer


class ParseOperationViewSet(BaseViewSet):
    queryset = ParseOperation.objects.all()
    serializer_class = ParseOperationSerializer


class InterpretOperationViewSet(BaseViewSet):
    queryset = InterpretOperation.objects.all()
    serializer_class = InterpretOperationSerializer


class TextBlockViewSet(BaseViewSet):
    queryset = TextBlock.objects.all()
    serializer_class = TextBlockSerializer
    pagination_class = StandardResultsSetPagination


class TextMatchViewSet(BaseViewSet):
    queryset = TextMatch.objects.all()
    serializer_class = TextMatchSerializer
    pagination_class = StandardResultsSetPagination


class GroupMatchViewSet(BaseViewSet):
    queryset = GroupMatch.objects.all()
    serializer_class = GroupMatchSerializer
    pagination_class = StandardResultsSetPagination


class ScreenplayViewSet(BaseViewSet):
    queryset = Screenplay.objects.all()
    serializer_class = ScreenplaySerializer


class TitlePageViewSet(BaseViewSet):
    queryset = TitlePage.objects.all()
    serializer_class = TitlePageSerializer


class LocationViewSet(BaseViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CharacterViewSet(BaseViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
