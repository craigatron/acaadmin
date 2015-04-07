from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from songs.models import Song, Vote

import logging
import sendgrid

class Command(BaseCommand):
  help = 'Send emails to each user that hasn\'t voted on songs.'

  def handle(self, *args, **options):
    sg = sendgrid.SendGridClient(settings.EMAIL_HOST_USER,
                                 settings.EMAIL_HOST_PASSWORD,
                                 raise_errors=True)
    prospective_songs = list(Song.objects.filter(state=0))
    for user in User.objects.all():
      if not user.email:
        continue

      unvoted_songs = []
      for song in prospective_songs:
        if not Vote.objects.filter(user=user, song=song):
          unvoted_songs.append(song)

      if unvoted_songs:
        message = sendgrid.Mail()
        message.add_to(user.email)
        message.set_subject('Daily Pow Arrangers nag email')
        songs_message = []
        for song in unvoted_songs:
          songs_message.append('<li><a href="%s">%s - %s</a> (suggested by %s)</li>' % (
            song.song_url, song.artist, song.title, song.suggested_by.first_name))
        message.set_html("""
Hi %s!

<p>
Looks like there are some songs you haven't voted on yet!
Head over to <a href="http://powarrangers.herokuapp.com/songs?filter=novote">the 'Rangers app</a> to submit your votes!
</p>
<p>
Songs you still need to vote on:
<ul>
%s
</ul>
</p>
<p><3 Craig</p>""" % (
          user.first_name, '\n'.join(songs_message)))
        message.set_from('Craig Martek <president@powarrangers.com>')

        try:
          sg.send(message)
        except sendgrid.SendGridClientError:
          logging.exception('Client error.')
        except sendgrid.SendGridServerError:
          logging.exception('Server error.')
