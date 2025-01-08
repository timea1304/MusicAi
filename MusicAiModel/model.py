import tensorflow as tf

class MusicGeneratorModel:
    def __init__(self, sequence_length, n_vocab, batch_size, musicModel):
        self.sequence_length = sequence_length
        self.n_vocab = n_vocab
        self.batch_size = batch_size
        self.musicModel = musicModel
        self.model = self.create_model()

    # KI Modell erstellen (LSTM-Model)
    def create_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(512, input_shape=(self.sequence_length, 1), return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(512, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256, return_sequences=False),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(self.n_vocab, activation='softmax')
        ])
        model.compile(
            loss='categorical_crossentropy',
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            metrics=['accuracy']
        )
        return model

    # KI Model trainieren
    def train(self, X, y, epochs):
        self.model.fit(X, y, epochs=epochs, batch_size=self.batch_size)
        self.model.save(self.musicModel)

    def save_model(self, model_filepath):
        self.model.save(model_filepath)

    # trainiertes KI Model laden
    @staticmethod
    def load_model(filepath):
        return tf.keras.models.load_model(filepath)
