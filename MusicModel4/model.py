import tensorflow as tf

class AIModel:
    def __init__(self, sequence_length, epochs, batch_size, n_vocab, aiModel):
        self.sequence_length = sequence_length
        self.epochs = epochs,
        self.batch_size = batch_size,
        self.n_vocab = n_vocab,
        self.aiModel = aiModel
        self.model = self.create_model()

    def create_model(self):
        """Erstellt das LSTM-Musikmodell"""
 
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(512, input_shape=(self.sequence_length, 1), return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(512, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(self.n_vocab, activation='softmax')
        ])
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
        return model
    
        # KI Model trainieren
    def train(self, X, y):
        """Trainiert das Modell"""
        self.model.fit(X, y,self.epochs, self.batch_size)
        self.model.save(self.aiModel)