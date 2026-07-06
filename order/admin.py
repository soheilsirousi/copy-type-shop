from django.contrib import admin
from file.admin import FileInline
from order.models import Language, Order, InputFormat


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(InputFormat)
class InputFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (FileInline,)
    list_display = ('user', 'order_type', 'order_status', 'language', 'page_count')