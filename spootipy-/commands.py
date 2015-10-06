#TODO: implement libspotify features from module "spotify", implement complete pyspotify
#method from trackplayertest.py


import os


import time
import curses
import subprocess
import requester
import spotify

class CommandManager(object):

    def __init__(self, stdscreen):
        track_list_length = 120
        track_list_height = 33

        search_buffer_length = 100
        search_buffer_height = 1

        help_window_length = 120
        help_window_height = 5

        self.country_id = None
        self.stdscreen = stdscreen
        self.track_list = None
        self.back_track_history = []
        self.forward_track_history = []
        self.track_start = 2
        self.curr_position = self.track_start
        self.track_window = stdscreen.subwin(track_list_height, track_list_length, 0, 0)
        self.help_window = stdscreen.subwin(help_window_height, help_window_length, self.track_window.getmaxyx()[0], 1)
        self.prompt_area = self.help_window
        self.search_window = stdscreen.subwin(search_buffer_height, search_buffer_length, self.track_window.getmaxyx()[0], 10)
        self.input_prompt = stdscreen.subwin(1, 15, self.track_window.getmaxyx()[0], 1)
        self.now_playing_window = stdscreen.subwin(1, 120, stdscreen.getmaxyx()[0] - 1, 0)
        self.command_list_hint = stdscreen.subwin(1, 30, stdscreen.getmaxyx()[0] - 3, 0)

        self.command_list_hint.addstr(0, 0, "Press C for Command List")
        self.command_list_hint.refresh()

    def print_command_list(self):
        """Display all possible commands available to the user."""
        command_menu = """[<Up>/K: Go Up] [<Down>/J: Go Down] [<Left>/H: Prev Track] [<Right>/L: Next Track]
                          [<Enter>: Play Selected Track] [<Space>: Toggle Play/Pause] [Q: Quit] [Y: Change Country Code]
                          [S: Search] [I: Play Track at Index] [F: Bring Spotify Client to Front] [C: Show Command List]
                          [A: Go to Album of Selected Track] [T: Top Tracks of Artist of Selected Track] [V: Set Volume]
                          [B: Previous track listing ] [N: Next track listing] [O: Decrease Volume] [P: Increase Volume]"""

        command_menu = '\n'.join(' '.join(line.split()) for line in command_menu.split('\n'))

        self.help_window.clear()
        self.help_window.addstr(0, 0, command_menu)
        self.help_window.refresh()

    def set_curr_position(self, curr_position):
        """Set the current position of the track list cursor."""
        self.curr_position = curr_position

    def move_up(self):
        """Move the track list cursor position up one."""
        if self.track_list != None and self.curr_position > self.track_start:
            self.curr_position -= 1
            self.draw_track_list()

    def move_down(self):
        """Move the track list cursor position down one."""
        if self.track_list != None and self.curr_position < (len(self.track_list) + self.track_start - 1):
            self.curr_position += 1
            self.draw_track_list()

    def next_song(self):
        """Play the next song in the track list (based on current cursor position)."""
        self.move_down()
        self.current_song()

    def prev_song(self):
        """Play the previous song in the track list (based on current cursor position)."""
        self.move_up()
        self.current_song()

    def play_at_index(self):
        """Play song located at a specific index within the current track list. User will be prompted for desired index."""
        desired_index = self.get_input(" Index:")

        try:
            desired_index = int(desired_index)
            screen_index = desired_index + self.track_start - 1
            if self.track_list != None and screen_index <= (len(self.track_list) + self.track_start - 1) and screen_index >= self.track_start:
                self.curr_position = screen_index
                self.current_song()
                self.draw_track_list()

        except ValueError:
            #Case: Invalid Index
            pass

    def current_song(self):
        """Play song track list cursor is currently on."""
        if self.track_list != None:
            self.play_song(self.track_list[self.curr_position - self.track_start])

    def toggle_play_pause(self):
        """Send command to Spotify desktop client to pause/play."""
        apple_script_call = ['osascript', '-e', 'tell application "Spotify" to playpause']
        subprocess.call(apple_script_call)

    def play_song(self, track):
        """Given track info, send command to Spotify desktop client to play it."""
        ##TODO: Implement method for playing spotify track via libspotify
        

        ##track_spotify_uri = track[4]
        ##apple_script_call = ['osascript', '-e', 'tell application "Spotify" to play track "{0}"'.format(track_spotify_uri)]

        ##subprocess.call(apple_script_call)
        ##self.update_now_playing(track)

    def update_now_playing(self, track):
        """Update the 'Now Playing' string to reflect currently playing track."""
        now_playing = ">>> Now Playing: {0} --- {1} <<<".format(track[1][:50], track[2][:40])
        self.now_playing_window.clear()
        self.now_playing_window.addstr(0, 0, now_playing)
        self.now_playing_window.refresh()

    def show_client(self):
        """Bring Spotify desktop client to the front of the screen."""
        get_client_command = 'tell application "Spotify" \n activate \n end tell'
        apple_script_call = ['osascript', '-e', get_client_command]
        subprocess.call(apple_script_call)

    def prev_track_list(self):
        """Go back to the previously displayed track listing."""
        if len(self.back_track_history) > 1:
            self.forward_track_history.append(self.track_list)
            self.track_list = self.back_track_history.pop()
            self.curr_position = self.track_start
            self.draw_track_list()

    def next_track_list(self):
        """Go ahead one track listing in the user's track listing history."""
        if len(self.forward_track_history) > 0:
            self.back_track_history.append(self.track_list)
            self.track_list = self.forward_track_history.pop()
            self.curr_position = self.track_start
            self.draw_track_list()

    def search_content(self):
        """Fulfill user's search request for music by keywords."""
        user_search = self.get_input("Search:")

        if len(user_search) > 0:
            if not self.back_track_history or self.track_list != self.back_track_history[-1] and self.track_list:
                self.forward_track_history = []
                self.back_track_history.append(self.track_list)

            self.track_list = requester.execute_search(user_search, self.country_id, self.track_window.getmaxyx()[0]-3)
            self.curr_position = self.track_start
            self.draw_track_list()

    def get_artist_top(self):
        """Display the top tracks (according to Spotify) by the artist of the currently selected track."""
        if self.track_list != None:
            track = self.track_list[self.curr_position - self.track_start]
            artist_name = track[2]
            artist_id = track[7]
            artist_uri = track[6]

            if not self.back_track_history or self.track_list != self.back_track_history[-1] and self.track_list:
                self.forward_track_history = []
                self.back_track_history.append(self.track_list)

            self.track_list = requester.get_artist_top(artist_name, artist_id, artist_uri, self.country_id)
            self.curr_position = self.track_start
            self.draw_track_list()

    def get_album_tracks(self):
        """Display all tracks in the album of the currently selected track."""
        if self.track_list != None:
            track = self.track_list[self.curr_position - self.track_start]
            album_name = track[3]
            album_id = track[8]
            album_uri = track[5]

            if not self.back_track_history or self.track_list != self.back_track_history[-1] and self.track_list:
                self.forward_track_history = []
                self.back_track_history.append(self.track_list)

            self.track_list = requester.get_album_tracks(album_name, album_id, album_uri)
            self.curr_position = self.track_start
            self.draw_track_list()

    def draw_track_list(self):
        """Handles all of the track list displaying."""
        self.track_window.clear()

        result_line = '{0:<2} | {1:<40} | {2:<25} | {3:<40}'
        result_header = result_line.format('#', 'Song Name', 'Artist', 'Album')
        separator_bar = '=' * (self.track_window.getmaxyx()[1] - 5)

        self.track_window.addstr(0, 0, result_header)
        self.track_window.addstr(1, 0, separator_bar)

        for song_index, track in enumerate(self.track_list, start=1):
            if (self.curr_position - self.track_start) == track[0]:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            song_index = str(song_index)

            if len(song_index) == 1:
                song_index = '0' + song_index

            track_string = result_line.format(song_index, track[1][:40], track[2][:25], track[3][:40])
            self.track_window.addstr(track[0] + self.track_start, 0, track_string, mode)

        bottom_bar_position = self.track_start + len(self.track_list)
        self.track_window.addstr(bottom_bar_position, 0, separator_bar)
        self.track_window.refresh()

    def country_check(self):
        """Ensure a valid country ISO code is inputted by the user."""
        valid_countries = [line.strip() for line in open(os.path.dirname(os.path.realpath(__file__)) + "/country_iso_codes.txt", 'r')]
        self.country_check_prompt()

        while self.country_id not in valid_countries:
            self.flash_message(":: Invalid Country ISO Code ::", 0.7)
            self.country_check_prompt()

    def country_check_prompt(self):
        """Country check helper method. Gets user input and properly formats it for validation."""
        user_input = self.get_input("Country:")

        if len(user_input) > 0:
            self.country_id = user_input.split()[0].upper()

    def increment_volume(self):
        """Increase the volume of the Spotify desktop client."""
        set_volume_command = 'tell application "Spotify" \n set sound volume to (get sound volume + 5) \n end tell'
        apple_script_call = ['osascript', '-e', set_volume_command]
        subprocess.call(apple_script_call)
        self.flash_message(":: Volume ++ ::", 0.1)

    def decrement_volume(self):
        """Decrease the volume of the Spotify desktop client."""
        set_volume_command = 'tell application "Spotify" \n set sound volume to (get sound volume - 5) \n end tell'
        apple_script_call = ['osascript', '-e', set_volume_command]
        subprocess.call(apple_script_call)
        self.flash_message(":: Volume -- ::", 0.1)

    def user_volume_input(self):
        """Allows the user to set desired volume level."""
        while True:
            try:
                desired_volume = self.get_input(" Volume:")

                #If no user input, RETURN
                if not desired_volume:
                    return

                desired_volume = int(desired_volume)

                if desired_volume < 0 or desired_volume > 100:
                    self.flash_message(":: Volume Range 1-100 ::", 0.8)
                else:
                    break
            except ValueError:
                    #Case: Unable to convert user input to type Int
                    self.flash_message(":: Volume Range 1-100 ::", 0.8)

        self.set_curr_volume(desired_volume)

    def set_curr_volume(self, volume_level):
        """Sets Spotify desktop client to 'volume_level'"""
        set_volume_command = 'tell application "Spotify" \n set sound volume to {0} \n end tell'.format(volume_level)
        apple_script_call = ['osascript', '-e', set_volume_command]
        subprocess.call(apple_script_call)

    def flash_message(self, message, flash_speed):
        """Takes in a message string and flashes it on screen for 'flash_speed' seconds."""
        self.prompt_area.clear()
        self.prompt_area.addstr(message)
        self.prompt_area.refresh()

        time.sleep(flash_speed)

        self.prompt_area.clear()
        self.prompt_area.refresh()

    def get_input(self, prompt):
        """Get user input through the user interface and return it."""
        curses.curs_set(2)

        self.prompt_area.clear()
        self.input_prompt.addstr(0, 0, prompt)
        self.search_window.clear()
        self.prompt_area.refresh()

        curses.echo()
        user_input = self.search_window.getstr().decode(encoding="utf-8")
        curses.noecho()

        self.prompt_area.clear()
        self.prompt_area.refresh()

        curses.curs_set(0)
        return user_input
