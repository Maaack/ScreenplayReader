from django.contrib import admin

# Register your models here.
from .models import InterpretOperation, Screenplay, Line, TitlePage, Scene, Character, Location

admin.site.register(InterpretOperation)
admin.site.register(Screenplay)
admin.site.register(Line)
admin.site.register(TitlePage)
admin.site.register(Scene)
admin.site.register(Location)
admin.site.register(Character)
