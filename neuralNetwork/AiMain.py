from keras.models import Model
from keras.layers import CuDNNLSTM as LSTM, Input, GaussianNoise

from dataParse import mapReplayFiles

class NeuralNetwork:



    def __init__(self):

        self.EPOCHS = 8
        self.iterations = 300

        self.MAX_BATCH_SIZE = 2400

        self.model = None

        self.trained = False


    def createModel(self, weightFile=None):
        del(self.model)

        inputLayer = Input(shape=(None, self.MAX_BATCH_SIZE, 5), name='input-layer')
        
        lstm = LSTM(64, return_sequences=True)(inputLayer)
        pos = Dense(64, activation='linear')(lstm)
        pos = GaussianNoise(0.2)(pos)
        pos = Dense(16, activation='linear')(pos)
        pos = Dense(y.shape[2], activation='linear', name='position')(pos)

        self.model = Model(inputs=map_input, outputs=pos)
        self.model.compile(optimizer=tf.train.AdamOptimizer(), loss='mae')
        print("Created Model")

    def trainData(self, replayFile, *args):
        
        mappedReplays = mapReplayFiles(replayFile, args)

        for replaySet in mappedReplays.iloc:
            print(replaySet)

    def predictData(self, beatmapInput):
        
        if not self.trained:
            print("WARNING: NETWORK HAS NOT BEEN TRAINED")


mrekk = NeuralNetwork()
mrekk.trainData("C:\\Users\\joant\\AppData\\Local\\osu!\\Replays", "D:\\Downloads\\pyOsuV3-main (4)\\pyOsuV3-main\\beatmaps")


    
