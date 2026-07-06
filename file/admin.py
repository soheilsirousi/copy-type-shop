from django.contrib import admin
from .models import File


class FileInline(admin.TabularInline):
    model = File
    extra = 1