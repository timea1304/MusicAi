import tensorflow as tf

class AIModel:
    def __init__(self, sequence_length, n_vocab, batch_size, musicModel):
        self.sequence_length = sequence_length
        self.n_vocab = n_vocab
        self.batch_size = batch_size
        self.musicModel = musicModel
        self.model = self.create_model()

    def create_model(self):
        input_layer = tf.keras.layers.Input(shape=(self.sequence_length,3))

        lstm_layer = tf.keras.layers.LSTM(512, return_sequences=True)(input_layer)
        lstm_layer = tf.keras.layers.Dropout(0.3)(lstm_layer)

        lstm_layer = tf.keras.layers.LSTM(512, return_sequences=True)(lstm_layer)
        lstm_layer = tf.keras.layers.Dropout(0.3)(lstm_layer)
        
        lstm_layer = tf.keras.layers.LSTM(256, return_sequences=False)(lstm_layer)
        lstm_layer = tf.keras.layers.Dropout(0.3)(lstm_layer)
        
        # Separate Dense-Schichten für jede Ausgabe
        pitch_output = tf.keras.layers.Dense(self.n_vocab, activation='softmax', name="pitch_output")(lstm_layer)
        duration_output = tf.keras.layers.Dense(1, activation='relu', name="duration_output")(lstm_layer)
        pause_output = tf.keras.layers.Dense(1, activation='relu', name="pause_output")(lstm_layer)
        
        model = tf.keras.Model(inputs=input_layer, outputs=[pitch_output, duration_output, pause_output])
        # Modell kompilieren
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(
            optimizer=optimizer,
            loss={
                "pitch_output": "sparse_categorical_crossentropy",
                "duration_output": "mse",
                "pause_output": "mse"
            },
            metrics={
                "pitch_output": ["accuracy"],
                "duration_output": ["mae"],
                "pause_output": ["mae"]
            }
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

