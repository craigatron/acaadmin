from django.contrib.auth.models import User
from django.db import models

class Song(models.Model):
    class Meta(object):
      permissions = (
          ('arrange', 'Can arrange'),
      )

    STATES = ['proposed', 'rejected', 'arranging', 'current', 'retired']

    suggested_by = models.ForeignKey(User, related_name='+')
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    song_url = models.URLField()

    state = models.IntegerField(choices=[(i, v) for i, v in enumerate(STATES)])
    has_willing_arranger = models.BooleanField(default=False)
    arranger = models.ForeignKey(User, blank=True, null=True, related_name='+')

    drive_link = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.artist)

    def score(self):
        votes = Vote.objects.all().filter(song=self)
        score = 0
        for v in votes:
            if v.vote == 0:
                score += 1
            elif v.vote == 1:
                score -= 1
            if self.has_willing_arranger:
                score += 0.5
        return score

class Vote(models.Model):
    VOTE_CHOICES = (
        (0, 'yes'), (1, 'no'), (2, 'meh')
    )
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    def __unicode__(self):
        return ', '.join([self.user.username, str(self.song), self.get_vote_display()])
