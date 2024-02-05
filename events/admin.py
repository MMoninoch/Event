# events/admin.py

from django.contrib import admin
from .models import Event, Material

class MaterialInline(admin.StackedInline):
    model = Material
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Material)

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['title', 'date', 'location']
#     list_filter = ['date']
