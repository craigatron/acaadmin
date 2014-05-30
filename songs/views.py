from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
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
      vote = models.Vote(user=request.user, song=song, vote=0)
      vote.save()
      return HttpResponseRedirect('/songs')
  else:
    form = forms.SongForm()
  return render(request, 'add.html', {'form': form},
      context_instance=RequestContext(request))

@login_required
def delete(request, song_id):
  song = models.Song.objects.get(pk=song_id)
  if song and song.suggested_by == request.user:
    votes = models.Vote.objects.filter(song=song)
    for v in votes:
      v.delete()
    song.delete()
    return HttpResponseRedirect('/songs')

  return HttpResponseForbidden()

@login_required
def vote(request, song_id, vote):
  song = models.Song.objects.get(pk=song_id)
  if not song:
    return HttpResponseBadRequest()

  vote_obj = models.Vote.objects.all().filter(song=song, user=request.user)
  if vote_obj:
    vote_obj = vote_obj[0]
    if vote == 'x':
      vote_obj.delete()
      return HttpResponse()
  else:
    vote_obj = models.Vote()
    vote_obj.user = request.user
    vote_obj.song = song

  vote_obj.vote = int(vote)
  vote_obj.save()
  return HttpResponse()

@login_required
def arrange(request, song_id):
  song = models.Song.objects.get(pk=song_id)
  if not song:
    return HttpResponseBadRequest()

  if not request.user.has_perm('songs.arrange'):
    return HttpResponseBadRequest()

  song.has_willing_arranger = True
  song.save()
  return HttpResponse()

@login_required
def index(request):
  songs = models.Song.objects.all()
  all_votes = models.Vote.objects.all()
  states = models.Song.STATES
  dictionary = {k: songs.filter(state=states.index(k))
                for k in states if 'proposed' != k}
  proposed = [{'song': s} for s in songs.filter(state=states.index('proposed'))]

  if request.GET.get('filter') == 'novote':
    # only show songs that the user hasn't voted on yet
    proposed = [p for p in proposed
                if not all_votes.filter(song=p['song'], user=request.user)]

  for v in proposed:
    votes = all_votes.filter(song=v['song'])
    vote_counts = [0, 0, 0]
    for vote in votes:
      vote_counts[vote.vote] += 1
    v['votes'] = vote_counts
    user_vote = all_votes.filter(song=v['song'], user=request.user)[:1]
    v['user_vote'] = user_vote.get().vote if user_vote else -1
  dictionary['proposed'] = sorted(proposed, key=lambda x: x['votes'][1] - x['votes'][0])

  dictionary['is_arranger'] = request.user.has_perm('songs.arrange')

  return render(request, 'list.html', dictionary,
      context_instance=RequestContext(request))
