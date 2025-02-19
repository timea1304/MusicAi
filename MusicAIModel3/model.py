import tensorflow as tf

class AIModel:
    def __init__(self, sequence_length, n_vocab, batch_size, epochs, model_path):
        self.sequence_length = sequence_length
        self.n_vocab = n_vocab
        self.batch_size = batch_size
        self.model_path = model_path
        self.epochs = epochs
        self.model = self.create_model()


    def create_model(self):
        """Erstellt das LSTM-Musikmodell"""
        input_layer = tf.keras.layers.Input(shape=(self.sequence_length, 3))

        x = tf.keras.layers.LSTM(512, return_sequences=True)(input_layer)
        x = tf.keras.layers.Dropout(0.3)(x)

        x = tf.keras.layers.LSTM(512, return_sequences=True)(x)
        x = tf.keras.layers.Dropout(0.3)(x)

        x = tf.keras.layers.LSTM(256, return_sequences=False)(x)
        x = tf.keras.layers.Dropout(0.3)(x)

        pitch_output = tf.keras.layers.Dense(self.n_vocab, activation="softmax", name="pitch_output")(x)
        duration_output = tf.keras.layers.Dense(1, activation="relu", name="duration_output")(x)
        pause_output = tf.keras.layers.Dense(1, activation="relu", name="pause_output")(x)

        model = tf.keras.Model(inputs=input_layer, outputs=[pitch_output, duration_output, pause_output])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss={
                "pitch_output": "sparse_categorical_crossentropy",
                "duration_output": "mse",
                "pause_output": "mse"
            },
            metrics={"pitch_output": "accuracy", "duration_output": "mae", "pause_output": "mae"}
        )
        
        return model
    
    # KI Model trainieren
    def train(self, X, y):
        """Trainiert das Modell"""
        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size)
        self.model.save(self.model_path)

    # trainiertes KI Model laden
    @staticmethod
    def load_model(filepath):
        return tf.keras.models.load_model(filepath)
