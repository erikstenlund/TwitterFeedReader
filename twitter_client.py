#!/usr/bin/python3
from twitter_auth import TwitterObj
from gi.repository import Gtk, GdkPixbuf

class TwitterApp(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Twitter feed")

        self.containerTweets = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        containerBox = Gtk.Box(spacing=4, orientation=Gtk.Orientation.VERTICAL)
        containerBox.pack_start(self.containerTweets, True, True, 0)
        
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.set_min_content_height(500)
        scrolledWindow.set_min_content_width(600)
        scrolledWindow.add(containerBox)

        self.add(scrolledWindow)
        self.connect("delete-event", Gtk.main_quit)
        ConnectionDialog(self).run()

class ConnectionDialog(Gtk.Dialog):
    def __init__(self, app):
        Gtk.Dialog.__init__(self, "Kleet", app, 0)
        self.app = app
        button = Gtk.Button("Connect")
        button.connect("clicked", self.get_tweets)
        
        self.ta = TwitterObj()
        self.entry = Gtk.Entry()

        urlLabel = Gtk.Label(self.ta.get_auth_url(), selectable=True)

        containerBox = self.get_content_area()
        containerBox.pack_start(urlLabel, True, True, 0)
        containerBox.pack_start(self.entry, True, True, 0)
        containerBox.pack_start(button, True, True, 0)
        self.show_all()
    def get_tweets(self, widget):
        tweets = self.ta.get_tweets(self.entry.get_text())
        for tweet in tweets:
            tweetGrid = TweetBox(tweet['imgFilePath'], tweet['name'], tweet['text'])
            self.app.containerTweets.pack_start(tweetGrid, True, True, 5)
            
        self.app.show_all()
        self.destroy()

class TweetBox(Gtk.Grid):
    def __init__(self, path, user, textf):
        Gtk.Grid.__init__(self)
        image = Gtk.Image()
        image.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file(path))
        imgfield = image
        textfield = Gtk.Label(textf)
        textfield.set_line_wrap(True)
        userfield = Gtk.Label(user)
        userfield.set_justify(Gtk.Justification.LEFT)
        self.attach(imgfield, 0,0, 2,2)
        self.attach_next_to(userfield, imgfield, Gtk.PositionType.RIGHT, 3, 1)

        self.attach_next_to(textfield, userfield, Gtk.PositionType.BOTTOM, 3, 1)



win = TwitterApp()
win.show_all()
Gtk.main()
