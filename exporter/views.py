import csv
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from importer.models import Screenplay

# Create your views here.


def csv_preview(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['Number', 'Characters', 'Location'])
    writer.writerow([1, 'Guy, Gal', 'Home'])
    writer.writerow([2, 'Guy', 'Guestroom'])
    writer.writerow([3, 'Gal', 'Garage'])
    return response


def csv_export(request, screenplay_id):
    screenplay = get_object_or_404(Screenplay, pk=screenplay_id)
    title = screenplay.title_pages.first().raw_title
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + title + '.csv"'
    writer = csv.writer(response)
    writer.writerow(['Number', 'Characters', 'Location'])
    scene_number = 0
    for scene in screenplay.scenes.all():
        scene_number += 1
        characters = ", ".join([character['title'] for character in scene.characters.values('title')])
        location = scene.location.title
        writer.writerow([scene_number, characters, location])
    return response


def csv_export_character_breakout(request, screenplay_id):
    screenplay = get_object_or_404(Screenplay, pk=screenplay_id)
    title = screenplay.title_pages.first().raw_title
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + title + '- Scene Breakdown.csv"'
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
