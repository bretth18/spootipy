from __future__ import unicode_literals
from blessings import Terminal


import sys
import threading
import logging
import spotify
import getpass

#debuging logger enabled
#logging.basicConfig(level=logging.DEBUG)
t = Terminal()


if sys.argv[1:]:
    track_uri = sys.argv[1]
else:
    print("""                 ____  ____  ____  ____  _____  _  ____ ___  _
                / ___\/  __\/  _ \/  _ \/__ __\/ \/  __\\  \//
                |    \|  \/|| / \|| / \|  / \  | ||  \/| \  /
                \___ ||  __/| \_/|| \_/|  | |  | ||  __/ / /
                \____/\_/   \____/\____/  \_/  \_/\_/   /_/      """)
    track_uri = raw_input('Enter spotify uri:')
    #If user input is equal to null, play "Marijuana"
    if track_uri == 'null':
        track_uri = 'spotify:track:5K4ExI2qvE1Ule3u7LxUDT'

#def on_login(self):
# Assuming a spotify_appkey.key in the current dir
    session = spotify.Session()
    username = raw_input('Enter username: ')
    password = getpass.getpass('Enter password: ')

#welcome message for user after username input
    if username == 'bretth18':
        print('Welcome Creator')
    else:
        print('Welcome: ' + username)

    session.login(username, password)
    remember_me = True

#if session.login(self.fail('ErrorType.BAD_USERNAME_OR_PASSWORD')):
    #session = spotify.Session()
    #username = raw_input('Enter username: ')
    #password = getpass.getpass('Enter password: ')


#TODO: Implement protocal for dealing with bad login "ErrorType.BAD_USERNAME_OR_PASSWORD"

#def on_bad_login(spotify.ErrorType.state.BAD_USERNAME_OR_PASSWORD):
#    session.login(spotify.CREDENTIALS)

# Process events in the background
loop = spotify.EventLoop(session)
loop.start()
print t.blue('Logging in...')


# port audio sink
audio = spotify.PortAudioSink(session)

# Events for coordination
logged_in = threading.Event()
end_of_track = threading.Event()


def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in.set()
    #elif spotify.Error:
    #else if LOGGED_IN(spotify.ErrorType.BAD_USERNAME_OR_PASSWORD):
    #TODO: spotify.ErrorType.state.BAD_USERNAME_OR_PASSWORD is not correlated w/ session.connection.state
    #elif session.connection.state is spotify.ErrorType.BAD_USERNAME_OR_PASSWORD:
        #print('Error: BAD USERNAME OR PASSWORD, CHECK CREDENTIALS')

def on_end_of_track(self):
    end_of_track.set()

# Register event listeners
session.on(
    spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)
session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)
#TODO:Fix session listener for ErrorType.state.BAD_USERNAME_OR_PASSWORD
#Event Listener is defined in libspotify
#session.on(
    #spotify.ErrorType.state.BAD_USERNAME_OR_PASSWORD, on_bad_login)


# Assuming a previous login with remember_me=True and a proper logout
#session.relogin()

logged_in.wait()

# Play a track
track = session.get_track(track_uri).load()
session.player.load(track)
session.player.play()
print t.red( 'Now Playing: '+ track.name)


# Wait for playback to complete or Ctrl+C
try:
    while not end_of_track.wait(0.1):
        pass
except KeyboardInterrupt:
    pass
