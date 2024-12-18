
import tensorflow as tf

class MusicGeneratorModel:
    def __init__(self, sequence_length, n_vocab, epochs, batch_size):
        self.sequence_length = sequence_length
        self.n_vocab = n_vocab
        self.model = self.create_model()
        self.epochs = epochs
        self.batch_size = batch_size
    # KI Modell erstellen (LSTM-Model)
    def create_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(256, input_shape=(self.sequence_length, 1), return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(128),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(self.n_vocab, activation='softmax')
        ])
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        return model
    
 

    # KI Model trainieren
    def train(self, X, y):
        self.model.fit(X, y, epochs = self.epochs, batch_size = self.batch_size)
        self.model.save("music_model.h5")

    # trainiertes KI model laden
    @staticmethod
    def load_model(filepath):
        return tf.keras.models.load_model(filepath)
