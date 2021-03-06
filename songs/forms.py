from django import forms
from songs import models

class SongForm(forms.ModelForm):
    class Meta(object):
        model = models.Song
        fields = ['artist', 'title', 'song_url']
