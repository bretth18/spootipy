from __future__ import unicode_literals

import sys
import threading
import logging
import spotify

if sys.argv[1:]:
    track_uri = sys.argv[1]
else:
    track_uri = 'spotify:track:6xZtSE6xaBxmRozKA0F6TA'

#TODO: Implement username/password input and storage of string type variables


# Assuming a spotify_appkey.key in the current dir
session = spotify.Session()
    #username = input('Enter username: ')
    #password = input('Enter password: ')
session.login('bretth18', 'henderson')
remember_me = True

# Process events in the background
loop = spotify.EventLoop(session)
loop.start()

# port audio sink
audio = spotify.PortAudioSink(session)

# Events for coordination
logged_in = threading.Event()
end_of_track = threading.Event()


def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in.set()


def on_end_of_track(self):
    end_of_track.set()


# Register event listeners
session.on(
    spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)
session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

# Assuming a previous login with remember_me=True and a proper logout
#session.relogin()

logged_in.wait()

# Play a track
track = session.get_track(track_uri).load()
session.player.load(track)
session.player.play()

# Wait for playback to complete or Ctrl+C
try:
    while not end_of_track.wait(0.1):
        pass
except KeyboardInterrupt:
    pass
