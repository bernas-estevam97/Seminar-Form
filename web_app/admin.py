from .models import *
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import WordDocument
from django.utils.html import format_html

class ExcelAdmin(ImportExportModelAdmin):
    pass

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'file_preview')

    def file_preview(self, obj):
        if obj.file.url.endswith(('.jpg', '.png', '.gif')):  # Check for image types
            return format_html('<img src="{}" style="height: 100px;" />', obj.file.url)
        return format_html('<a href="{}">Download File</a>', obj.file.url)

    file_preview.short_description = 'File Preview'

admin.site.register(WordDocument, DocumentAdmin)

admin.site.register(SeminarFormModel, ExcelAdmin)