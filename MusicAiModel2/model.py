import tensorflow as tf
class MusicModelAI:
    #initialisieren
    def __init__(self, epochs, batch_size,sequence_length, aiModel, n_vocab):
        self.n_vocab = n_vocab
        self.epochs = epochs
        self.batch_size = batch_size
        self.aiModel = aiModel
        self.sequence_length = sequence_length
        self.model = self.create_model()

    #KI Modell erstellen
    def create_model(self):
        model =tf.keras.Sequential([
            tf.keras.layers.LSTM(256, input_shape=(self.sequence_length, 3), return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256, return_sequences=False),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(self.n_vocab, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model
    #mit den Trainingsdaten Trainieren
    def train(self, training_data, target_data):
        self.model.fit(training_data, target_data,epochs = self.epochs, batch_size = self.batch_size)
        self.model.save()
    
    def save_model(self):
        self.model.save(self.aiModel)
                        
    @staticmethod
    def load_model(filepath):
        return tf.keras.models.load_model(filepath)