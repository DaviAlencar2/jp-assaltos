from django.contrib import admin
from .models import Robbery, Neighborhood

class ListarAssaltos(admin.ModelAdmin):
    list_display = ("id","date","time","neighborhood")
    list_display_links = ("id","neighborhood")
    search_fields = ("date","neighborhood")
    list_filter = ("type",)
    list_per_page = 10

admin.site.register(Robbery, ListarAssaltos)
admin.site.register(Neighborhood)