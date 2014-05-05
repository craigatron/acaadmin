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
  all_votes = models.Vote.objects.all()
  states = models.Song.STATES
  dictionary = {k: songs.filter(state=states.index(k))
                for k in states if 'proposed' != k}
  proposed = {s.pk : {'song': s} for s in songs.filter(state=states.index('proposed'))}
  for _, v in proposed.items():
    votes = all_votes.filter(song=v['song'])
    vote_counts = [0, 0, 0]
    for vote in votes:
      vote_counts[vote.vote] += 1
    v['votes'] = vote_counts
    user_vote = all_votes.filter(song=v['song'], user=request.user)[:1]
    v['user_vote'] = user_vote.get().vote if user_vote else -1
  dictionary['proposed'] = proposed.values()

  return render(request, 'list.html', dictionary,
      context_instance=RequestContext(request))
