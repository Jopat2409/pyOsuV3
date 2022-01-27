


class NeuralNetwork:


    def __init__(self, profile=None):

        if profile:
            self.LoadProfile(profile)

        self.m_configuration = {"FRAMES_PER_SECOND": 24,
                                "EPOCHS": 8,
                                "TIMEFRAME_LENGTH": 2048}

    def Configuration(self):
        return self.m_configuration


    def PassData(self, beatmapMap):
        self.m_beatmapMap = beatmapMap

    def LoadProfile(self, profile):
        pass
