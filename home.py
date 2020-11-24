if __name__ == '__main__':
#Aleks4920

    import kivy
    from kivy.uix.slider import Slider
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.animation import Animation
    from kivy.uix.widget import Widget
    from kivy.uix.image import Image
    from kivy.uix.image import AsyncImage
    from kivy.config import Config
    Config.set('graphics', 'resizable', True)
    from PIL import Image
    import requests
    from PIL import Image
    from io import BytesIO
    import os
    import sys
    #import json
    import spotipy
    import webbrowser
    import spotipy.util as util
    from time import sleep
    from kivy.lang import Builder
    from kivy.base import runTouchApp
    from kivy.uix.floatlayout import FloatLayout
    from kivy.factory import Factory
    from kivy.uix.actionbar import ActionItem
    from kivy.uix.textinput import TextInput
    import subprocess
    ################################################################################

    #get following info from your spotipy account
    username = ""
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    client_id = ''
    client_secret = ''
    redirect_uri = 'https://google.com/'


    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri) # add scope

    # Create our spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)
    devices = spotifyObject.devices()
    deviceID = devices['devices'][0]['id']


    # Current track information
    track = spotifyObject.current_user_playing_track()
    if track != None:
        artist = track['item']['artists'][0]['name']
        playing = track['item']['name']


    #define image
    ################################################################################
    link = (track['item']['album']['images'][0]['url'])
    response = requests.get(link)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((300,300))
    img.save("img1.jpg")

    #Create kivy GUI
    ################################################################################
    class MainWindow(Screen, Widget):
        def __init__(self, **kwargs):
            super(Screen, self).__init__(**kwargs)
            img.load()
            self.image = 'img1.jpg'
            self.track = playing
            self.artist = artist

        def on_touch_move(Widget,touch):
            volume = int(Widget.value)
            spotifyObject.volume(volume, device_id=(deviceID))
            
        #refreshes app on song switch
        def next(self):
            spotifyObject.next_track(device_id=(deviceID))
            print(f'exec: {sys.executable} {["python"] + sys.argv}')
            os.execvp(sys.executable, ['python'] + sys.argv)
        def last(self):
            spotifyObject.previous_track(device_id=(deviceID))
            print(f'exec: {sys.executable} {["python"] + sys.argv}')
            os.execvp(sys.executable, ['python'] + sys.argv)

    class ActionTextInput(TextInput, ActionItem):
        pass
    class Slider(Widget):
        pass

    class WindowManager(ScreenManager):
        pass
    kv = Builder.load_file("home.kv")
    sm = WindowManager()

    screens = [MainWindow(name="main")]
    for screen in screens:
        sm.add_widget(screen)

    sm.current = "main"

    #load kivy app
    ################################################################################

    class HomeApp(App):
        def build(self):
            Builder.load_file("home.kv" )

            return sm

    #run GUI
    ##if __name__ == '__main__':

    HomeApp().run()
