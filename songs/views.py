from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from songs import forms, models

@login_required
def add(request):
  if request.method == 'POST':
    form = forms.SongForm(request.POST)
    if form.is_valid():
      song = form.save(commit=False)
      song.state = 0
      song.suggested_by = request.user
      song.save()
      return HttpResponseRedirect('/songs')
  else:
    form = forms.SongForm()
  return render(request, 'add.html', {'form': form},
      context_instance=RequestContext(request))

@login_required
def delete(request, song_id):
  song = models.Song.objects.get(pk=song_id)
  if song and song.suggested_by == request.user:
    song.delete()
    return HttpResponseRedirect('/songs')

  return HttpResponseForbidden()


@login_required
def index(request):
  songs = models.Song.objects.all()
  states = models.Song.STATES
  dictionary = {k: songs.filter(state=states.index(k)) for k in states}

  return render(request, 'list.html', dictionary,
      context_instance=RequestContext(request))
