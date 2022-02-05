""" ---------- PYTHON MODULES ---------- """
import pygame                               # for audio
import config                               # for program-global variables
import os                                   # for creating filepaths


class audioStream:
    """
    Should ensure that everything is playing according to the rules of osu!
    """

    def __init__(self):

        # initialize pygame's sound playing module
        pygame.mixer.init()

        # create the two channels used for handling music and effects playing
        self.effectChannel = pygame.mixer.Channel(0)
        self.musicChannel = pygame.mixer.music

        # dictionary mapping effects to their respective mp3's
        self.effects = {"hitSound": "normal-hitnormal.ogg"}

        # set the music volume to the volume saved in the config
        self.musicChannel.set_volume(0.1)
        self.effectChannel.set_volume(0.3)


    def playEffect(self, effect):
        """
        Plays a defined sound effect
        """
        # load the sound to play
        effectSound = pygame.mixer.Sound(os.path.join(config.cSkinDirectory, self.effects[effect]))
        # play the sound
        self.effectChannel.play(effectSound)

    def previewSong(self, songFile, offset):
        """
        Method called when previewing a beatmap
        """
        # load the song file
        self.musicChannel.load(songFile)
        # play the song at the offset specified in the osu file, and make it loop infinitely
        self.musicChannel.play(start=offset/1000, loops=-1)


    def playSong(self, songFile):
        """
        Method for actually playing the song
        """
        # load the file
        self.musicChannel.load(songFile)
        # play the song
        self.musicChannel.play()

    def IsPlayingSong(self) -> bool:
        return self.musicChannel.get_busy()


    def pauseSong(self):
        """
        Method for pausing the song
        """
        self.musicChannel.pause()


    def resumeSong(self, pTime=0):
        """
        Method for resuming the song,
        pTime is the offset since pausing and resuming in pygame sometimes has a slight offset
        """
        # if the user has not defined an offset
        if pTime == 0:
            # unpause
            self.musicChannel.unpause()
        else:
            # else play the music from the offset
            self.musicChannel.play(start=pTime/1000)
