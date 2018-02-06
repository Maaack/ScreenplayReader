# Create your views here.

from screenplayreader.mixins.views import BaseViewSet
from .models.serializers import *


# Create your views here.
class ImportedContentViewSet(BaseViewSet):
    queryset = ImportedContent.objects.all()
    serializer_class = ImportedContentSerializer


class ParseOperationViewSet(BaseViewSet):
    queryset = ParseOperation.objects.all()
    serializer_class = ParseOperationSerializer


class TextBlockViewSet(BaseViewSet):
    queryset = TextBlock.objects.all()
    serializer_class = TextBlockSerializer


class TextMatchViewSet(BaseViewSet):
    queryset = TextMatch.objects.all()
    serializer_class = TextMatchSerializer


class GroupMatchViewSet(BaseViewSet):
    queryset = GroupMatch.objects.all()
    serializer_class = GroupMatchSerializer
