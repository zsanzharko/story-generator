import os
import tensorflow as tf
from keras.models import Model, load_model
import keras.backend as k_backed
from keras.layers import Dense, LSTM, Input, Embedding, Dropout
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import RMSprop
from keras.callbacks import LambdaCallback
import gc
import keras.backend as k


class MultiLSTMModel:

    def __init__(self, model_file, total_words, n_units=1024, embedding_size=256):
        self.model = None
        self.n_units = n_units
        self.embedding_size = embedding_size
        models_location = os.path.dirname(os.path.abspath(os.getcwd())) + '/models'
        try:
            for file in os.listdir(models_location):
                if file == model_file:
                    self.model = load_model(models_location + fr'/{file}')
                    self.model_location = models_location + fr'/{file}'
                    break
        except BaseException as e:
            print(e)
            print("Don't loaded model file. Creation new model...")

        if self.model is None:
            text_in = Input(shape=(None,))
            embedding = Embedding(total_words, embedding_size)
            x = embedding(text_in)

            x = LSTM(n_units, return_sequences=True)(x)
            x = Dropout(0.2)(x)
            x = LSTM(n_units)(x)
            x = Dropout(0.2)(x)
            text_out = Dense(total_words, activation='softmax')(x)

            self.model = Model(text_in, text_out)
            # self.opti = RMSprop(lr=0.001)
            self.model.compile(loss='categorical_crossentropy', metrics=["mae"], run_eagerly=True)
            self.model_location = models_location + fr'/{model_file}'
            self.model.save(self.model_location)
            print(fr'Model {model_file} saved. Current file location {self.model_location}')
            pass

        print(self.model.summary())
        pass

    def fit(self, X, y, epochs=5, batch_size=16, shuffle=False, callbacks=None, save=False):
        epochs_on_epoch = LambdaCallback(on_epoch_end=epoch_on_epoch)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, callbacks=[epochs_on_epoch], shuffle=shuffle)
        if save:
            try:
                self.model.save(self.model_location)
                print(fr'-----------------Model {self.model_location} saved.-----------------')
            except BaseException as e:
                print(e)
                print("We don't save model, cause have problem with location")
            pass
        pass

    def save(self, model_location=None):
        if model_location is None:
            self.model.save(self.model_location)
        self.model.save(model_location)


def epoch_on_epoch(epoch, logs):
    k.clear_session()
    gc.collect()
    # start_text = ""
    # count_words = 50
    #
    # print('Temp 0.2')
    # print (generate_text(start_text, count_words, model, seq_length, temp = 0.2))
    # print('Temp 0.33')
    # print (generate_text(start_text, count_words, model, seq_length, temp = 0.33))
    # print('Temp 0.5')
    # print (generate_text(start_text, count_words, model, seq_length, temp = 0.5))
    # print('Temp 1.0')
    # print (generate_text(start_text, count_words, model, seq_length, temp = 1))
    pass
