from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import News, Tag


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'archived')
    search_fields = ('title', 'text')
    list_filter = ('tags',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
