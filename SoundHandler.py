
import pygame
import config



class audioStream:



    def __init__(self):

        # initialize pygame's sound playing module
        pygame.mixer.init()

        # create the two channels used for handling music and effects playing
        self.effects = pygame.mixer.Channel(0)
        self.musicChannel = pygame.mixer.music

        # dictionary mapping effects to their respective mp3's
        self.effects = {}

        # set the music volume to the volume saved in the config
        self.musicChannel.set_volume(int(config.currentSettings["VolumeMusic"]) / 100)





    # method called when previewing a beatmap
    def previewSong(self, songFile, offset):

        #print("Started {} at {}".format(songFile, offset))
        # load the song file
        self.musicChannel.load(songFile)
        # play the song at the offset specified in the osu file, and make it loop infinitely
        self.musicChannel.play(start=offset/1000,loops=-1)

    def playSong(self, songFile):

        self.musicChannel.load(songFile)
        self.musicChannel.play()
        

        

        
