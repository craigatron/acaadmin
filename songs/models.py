from django.contrib.auth.models import User
from django.db import models

class Song(models.Model):
  STATES = ['proposed', 'rejected', 'arranging', 'current', 'retired']

  suggested_by = models.ForeignKey(User, related_name='+')
  artist = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  song_url = models.URLField()

  state = models.IntegerField(choices=[(i, v) for i, v in enumerate(STATES)])
  has_willing_arranger = models.BooleanField(default=False)
  arranger = models.ForeignKey(User, blank=True, null=True, related_name='+')

  def __unicode__(self):
    return '%s (%s)' % (self.title, self.artist)

class Vote(models.Model):
  VOTE_CHOICES = (
      (0, 'yes'), (1, 'no'), (2, 'meh')
  )
  user = models.ForeignKey(User)
  song = models.ForeignKey(Song)
  vote = models.IntegerField(choices=VOTE_CHOICES)

  def __unicode__(self):
    return ', '.join([self.user.username, str(self.song), self.vote.get_vote_display()])
