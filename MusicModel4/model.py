import tensorflow as tf
from keras.callbacks import ModelCheckpoint

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
        model.compile(
            loss='categorical_crossentropy',
            optimizer='rmsprop'
            )
        return model
    
        # KI Model trainieren
    def train(self, X, y):
        """Trainiert das Modell"""
        checkpoint = ModelCheckpoint(
            filepath = self.aiModel,
            monitor='loss',
            verbose=1,
            save_best_only=True,
            mode='min'
        )
        callbacks_list = [checkpoint]

        self.model.fit(
            self.aiModel,
            X,
            y,
            epochs = self.epochs,
            batch_size = self.batch_size,
            validation_split =0.1,
            callbacks=callbacks_list
            )
        self.model.save(self.aiModel)