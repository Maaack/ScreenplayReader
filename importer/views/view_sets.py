from .serializers import *
from screenplayreader.mixins.views import BaseViewSet, OperationViewSet


# Create your views here.
class ImportedContentViewSet(BaseViewSet):
    queryset = ImportedContent.objects.all()
    serializer_class = ImportedContentSerializer


class ParseOperationViewSet(OperationViewSet):
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
