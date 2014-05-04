from django.contrib import admin
from songs.models import Song, Vote

admin.site.register(Song)
admin.site.register(Vote)
