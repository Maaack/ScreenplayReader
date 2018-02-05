from django.shortcuts import render

# Create your views here.

from .models.serializers import *

from screenplayreader.mixins.views import BaseViewSet


# Create your views here.
class ImportedContentViewSet(BaseViewSet):
    queryset = ImportedContent.objects.all()
    serializer_class = ImportedContentSerializer


class ParseOperationViewSet(BaseViewSet):
    queryset = ParseOperation.objects.all()
    serializer_class = ParseOperationSerializer


class TextMatchViewSet(BaseViewSet):
    queryset = TextMatch.objects.all()
    serializer_class = TextMatchSerializer
