from .serializers import *
from screenplayreader.mixins.view_sets import BaseViewSet, OperationViewSet


# Create your views here.
class InterpretOperationViewSet(OperationViewSet):
    queryset = InterpretOperation.objects.all()
    serializer_class = InterpretOperationSerializer


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
