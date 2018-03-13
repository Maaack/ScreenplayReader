from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import *
from screenplayreader.mixins.views import BaseViewSet


# Create your views here.
class ImportedContentViewSet(BaseViewSet):
    queryset = ImportedContent.objects.all()
    serializer_class = ImportedContentSerializer


class OperationViewSet(BaseViewSet):
    class Meta:
        abstract = True

    @detail_route(methods=['post'],  url_path='run-operation')
    def run_operation(self, request, pk = None):
        operation = self.get_object()
        operation.run_operation()
        return Response('Operation complete!')


class ParseOperationViewSet(OperationViewSet):
    queryset = ParseOperation.objects.all()
    serializer_class = ParseOperationSerializer


class InterpretOperationViewSet(OperationViewSet):
    queryset = InterpretOperation.objects.all()
    serializer_class = InterpretOperationSerializer


class TextBlockViewSet(BaseViewSet):
    queryset = TextBlock.objects.all()
    serializer_class = TextBlockSerializer


class TextMatchViewSet(BaseViewSet):
    queryset = TextMatch.objects.all()
    serializer_class = TextMatchSerializer


class GroupMatchViewSet(BaseViewSet):
    queryset = GroupMatch.objects.all()
    serializer_class = GroupMatchSerializer


class ScreenplayViewSet(BaseViewSet):
    queryset = Screenplay.objects.all()
    serializer_class = ScreenplaySerializer


class LineViewSet(BaseViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer


class TitlePageViewSet(BaseViewSet):
    queryset = TitlePage.objects.all()
    serializer_class = TitlePageSerializer


class SceneViewSet(BaseViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


class LocationViewSet(BaseViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CharacterViewSet(BaseViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
