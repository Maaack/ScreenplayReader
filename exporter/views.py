import csv
from django.http import HttpResponse
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