""" ---------- NEURAL NETWORK MODULES ---------- """
from keras.models import Model
from keras.layers import CuDNNLSTM as LSTM, Input, GaussianNoise

""" ---------- DATA MODULES ---------- """
from dataParse import mapReplayFiles

"""
Class that encapsulates all the functions and data of a user-trainable neural network
"""
class NeuralNetwork:

    def __init__(self):

        # defines the epochs used
        self.EPOCHS = 8
        # defines the amount of training iterations the network completes
        self.iterations = 300
        # defines the amount of data passed to the network
        self.MAX_BATCH_SIZE = 2400

        # initializes the model
        self.model = None

        # tracks the status of the model
        self.trained = False

    """ 
    Method that creates a model
    weightFile: file that holds the already trained weights
    """
    def createModel(self, weightFile=None):
        # make sure self.model is completely clear
        del(self.model)

        # create the input layer with the correct shape
        inputLayer = Input(shape=(None, self.MAX_BATCH_SIZE, 5), name='input-layer')
        # add an LSTM (CuDNNLSTM) cell to the network
        lstm = LSTM(64, return_sequences=True)(inputLayer)
        # add a dense layer
        pos = Dense(64, activation='linear')(lstm)
        # add a gaussian noise layer
        pos = GaussianNoise(0.2)(pos)
        # add a dense layer
        pos = Dense(16, activation='linear')(pos)
        # add a dense (output layer) with the shape of the output data
        pos = Dense(y.shape[2], activation='linear', name='position')(pos)

        # create the model with the ipt and output sequences
        self.model = Model(inputs=map_input, outputs=pos)
        # compile the model
        self.model.compile(optimizer=tf.train.AdamOptimizer(), loss='mae')

    """
    Method to train the model based off of user input
    replayFile: folder that contains replays, specified by user
    args: subsequent beatmap files (osu default song folder is searched by default)
    """
    def trainData(self, replayFile, *args):
        
        # get a pandas dataframe mapping replay files to beatmap files
        mappedReplays = mapReplayFiles(replayFile, args)

        for replaySet in mappedReplays.iloc:
            print(replaySet)

    """
    Method to predict data from a beatmap that has been inputted
    beatmapInput: beatmap file to play
    """
    def predictData(self, beatmapInput):

        # if the network is not trained, warn the user
        if not self.trained:
            print("WARNING: NETWORK HAS NOT BEEN TRAINED")

# only run if the file is being debugged
if __name__ == "__main__":
    # create a neural network object
    mrekk = NeuralNetwork()
    # train data based off of two folders
    mrekk.trainData("C:\\Users\\joant\\AppData\\Local\\osu!\\Replays", "D:\\Downloads\\pyOsuV3-main (4)\\pyOsuV3-main\\beatmaps")


    
