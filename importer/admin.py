from django.contrib import admin

# Register your models here.
from .models import ImportedContent, ParseOperation, GroupMatch, TextMatch

admin.site.register(ImportedContent)
admin.site.register(ParseOperation)
admin.site.register(GroupMatch)
admin.site.register(TextMatch)
