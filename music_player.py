import os
import pickle
import tkinter as tk
from tkinter import *
from tkinter import filedialog  # to open songs file
from pygame import mixer  # to control music play,pause


class Player( tk.Frame ):
    def __init__(self, master):
        super().__init__( master )
        self.master = master
        self.pack()
        mixer.init()
        if os.path.exists( 'songs.pickle' ):
            with open( 'songs.pickle', 'rb' ) as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.playlist = []
        self.create_frame()
        self.track_widget()
        self.control_widget()
        self.tracklist_widget()

    def create_frame(self):  # frames
        self.track = tk.LabelFrame( self, text="SONGS TRACK", font=("Cornerstone", 15, "bold"), bg='#52595D',
                                    fg='white', bd=7, relief=tk.GROOVE )  # first_frame
        self.track.configure( width=410, height=300 )
        self.track.grid( row=0, column=0, padx=10 )

        self.tracklist = tk.LabelFrame( self, text=f"PlayList-{len( self.playlist )}",
                                        font=("Cornerstone", 15, "bold"), bg='#4863A0', fg='white',
                                        bd=7, relief=tk.GROOVE )  # first_frame
        self.tracklist.configure( width=190, height=400 )
        self.tracklist.grid( row=0, column=1, rowspan=3, pady=5 )

        self.controls = tk.LabelFrame( self, font=("times new roman", 15, "bold"), bg='#E6BF83', fg='white',
                                       bd=7, relief=tk.GROOVE )  # first_frame
        self.controls.configure( width=410, height=80 )
        self.controls.grid( row=2, column=0, pady=5, padx=10 )

    def track_widget(self):  # diffrent widgets of diffrent methods
        self.canvas = tk.Label( self.track, image=img_size)
        self.canvas.configure( width=400, height=240 )
        self.canvas.grid( row=0, column=0 )

        self.songtrack = tk.Label( self.track, font=("bookman old style", 15, "bold"), bg='#D8BFD8', fg='#2C3539')
        self.songtrack['text'] = 'MUSIC MP3 PLAYER'
        self.songtrack.configure( width=30, height=1 )
        self.songtrack.grid( row=1, column=0 )

    def control_widget(self):
        self.loadSongs = tk.Button( self.controls,image=add_size, font=10,bg='black')
        self.loadSongs['text'] = "Load Songs"
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid( row=0, column=0, padx=10 )

        self.prev = tk.Button( self.controls, bg='#E42217', fg='#DCD0FF', font=10, image=prev )
        self.prev['command'] = self.pre_song
        self.prev.grid( row=0, column=1 )

        self.pause = tk.Button( self.controls, bg='#E42217', fg='#DCD0FF', font=10, image=pause )
        self.pause['command'] = self.pause_song
        self.pause.grid( row=0, column=2 )

        self.next = tk.Button( self.controls, bg='#E42217', fg='#DCD0FF', font=10, image=next )
        self.next['command'] = self.next_song
        self.next.grid( row=0, column=3 )

        self.volume = tk.DoubleVar()  # volume part
        self.slider = tk.Scale( self.controls, from_=0, to=10, orient=tk.HORIZONTAL,bg='#E42217',fg='white',bd=3,font=('Incised901 BT',14,'bold'),highlightbackground = "#151B54")
        self.slider['variable'] = self.volume
        self.slider.set(5)
        mixer.music.set_volume(0.5)
        self.slider['command'] = self.change_volume
        self.slider.grid( row=0, column=4, padx=5 )

    def tracklist_widget(self):
        self.scrollbar = tk.Scrollbar( self.tracklist, orient=tk.VERTICAL )
        self.scrollbar.grid( row=0, column=1, rowspan=5, sticky='ns' )

        self.list = tk.Listbox( self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set,
                                selectbackground='sky blue' )
        self.enumerate_songs()
        self.list.config( height=22 )
        self.list.bind( '<Double-1>', self.play_song )

        self.scrollbar.config( command=self.list.yview )
        self.list.grid( row=0, column=0, rowspan=5 )

    def enumerate_songs(self):
        for index, song in enumerate( self.playlist ):
            self.list.insert( index, os.path.basename( song ) )

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root__, dirs, files in os.walk( directory ):
            for file in files:
                if os.path.splitext( file )[1] == '.mp3':
                    path = (root__ + '/' + file).replace( '\\', '/' )
                    self.songlist.append( path )

        with open( 'songs.pickle', 'wb' ) as f:
         pickle.dump( self.songlist, f )

        self.playlist = self.songlist
        self.tracklist['text'] = f"PlayList-{str( len( self.playlist ) )}"
        self.list.delete( 0, tk.END )
        self.enumerate_songs()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range( len( self.playlist ) ):
                self.list.itemconfigure( i, bg='white' )
        mixer.music.load( self.playlist[self.current] )

        self.pause['image']=play
        self.paused=False
        self.played=True
        self.songtrack['anchor']='w'
        self.songtrack['text']=os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current,bg='#C04000')
        mixer.music.play()

    def pause_song(self):
       if not self.paused:
           self.paused=True
           mixer.music.pause()
           self.pause['image']=pause
       else:
           if self.played==False:
              self.play_song()
           self.paused=False
           mixer.music.unpause()
           self.pause['image'] = play


    def pre_song(self):
        if self.current > 0:
            self.current-=1
        else:
            self.current=0
        self.list.itemconfigure(self.current+1,bg='white')
        self.play_song()
    def next_song(self):
        if self.current < len(self.playlist)-1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure( self.current-1, bg='white' )
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v/10)


root = tk.Tk()
root.config(bg='#C35817')
root.geometry( '600x400' )
root.title( "MP3 MUSIC PLAYER 🔊 🎧" )
img = PhotoImage( file=r'images/music.png' )
img_size=img.subsample(5,5)
next = PhotoImage( file=r'images/next.png' )
prev = PhotoImage( file=r'images/previous.png' )
play = PhotoImage( file=r'images/play.png' )
pause = PhotoImage( file=r'images/pause.png' )
add=PhotoImage(file=r'images/songs.png')
add_size=add.subsample(1,1)


app = Player( master=root )
app.mainloop()
