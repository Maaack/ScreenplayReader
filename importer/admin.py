from django.contrib import admin

# Register your models here.
from .models import ImportedContent, TextBlock, TextMatch, GroupMatch, ParseOperation, InterpretOperation

admin.site.register(ImportedContent)
admin.site.register(ParseOperation)
admin.site.register(InterpretOperation)
admin.site.register(TextBlock)
admin.site.register(GroupMatch)
admin.site.register(TextMatch)
