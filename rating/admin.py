from django.contrib import admin
from .models import Rating

class RatingAdmin(admin.ModelAdmin):
    list_display = ('song', 'rating',)
    search_fields = ('song__title',)
    list_filter = ('rating',)
    ordering = ('song',)

admin.site.register(Rating, RatingAdmin)
