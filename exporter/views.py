import csv
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import detail_route

from interpreter.models import Screenplay
from interpreter.views import ScreenplaySerializer, BaseViewSet


class ScreenplayViewSet(BaseViewSet):
    queryset = Screenplay.objects.all()
    serializer_class = ScreenplaySerializer

    @detail_route(methods=['get'],  url_path='character-csv')
    def export_character_csv(self, request, pk = None):
        return ScreenplayViewSet.csv_export_character_breakout(self.get_object())

    @detail_route(methods=['get'],  url_path='basics-csv')
    def export_basics_csv(self, request, pk = None):
        return ScreenplayViewSet.csv_export_basics(self.get_object())

    @staticmethod
    def get_csv_response(filename):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
        return response

    @staticmethod
    def csv_export_character_breakout(screenplay):
        title = screenplay.title_pages.first().title
        response = ScreenplayViewSet.get_csv_response(title + ' - Character Breakout')
        writer = csv.writer(response)

        character_list = [character['title'] for character in
                          screenplay.characters.annotate(line_count=Count('lines')).order_by('-line_count').values('title')]
        headers = ['Number', 'Location']
        headers += character_list
        writer.writerow(headers)
        scene_number = 0
        for scene in screenplay.scenes.all():
            scene_number += 1
            scene_characters = [character['title'] for character in scene.characters.values('title')]
            location = scene.location.title
            row = [scene_number, location]
            for character in character_list:
                if scene_characters.count(character):
                    row.append('X')
                else:
                    row.append('')
            writer.writerow(row)
        return response

    @staticmethod
    def csv_export_basics(screenplay):
        title = screenplay.title_pages.first().title
        response = ScreenplayViewSet.get_csv_response(title)
        writer = csv.writer(response)

        writer.writerow(['Number', 'Characters', 'Location'])
        scene_number = 0
        for scene in screenplay.scenes.all():
            scene_number += 1
            characters = ", ".join([character['title'] for character in scene.characters.values('title')])
            location = scene.location.title
            writer.writerow([scene_number, characters, location])
        return response
