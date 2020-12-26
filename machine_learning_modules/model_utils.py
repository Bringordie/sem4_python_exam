import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

def train_model(model, x_train, y_train, x_test, y_test):
    optimizer = keras.optimizers.Adam()
    #compile: Configures the model for training.
    model.compile(optimizer=optimizer, 
            loss='mean_absolute_error')
    #fit: Trains the model for a fixed number of epochs (iterations on a dataset).
    history = model.fit(x_train, y_train,
                    epochs=400, batch_size=1024,
                    validation_data=(x_test, y_test), 
                    verbose=1)
    return history

def train_model_with_callbackStop(model, x_train, y_train, x_test, y_test, callbacks_list):
    
    optimizer = keras.optimizers.Adam()
    model.compile(optimizer=optimizer,
            loss='mean_absolute_error')
    history = model.fit(x_train, y_train,
                    epochs=400, batch_size=1024,
                    validation_data=(x_test, y_test), 
                    callbacks=callbacks_list, 
                    verbose=1)
    return history


def make_model(x_train):
    model=keras.models.Sequential([
    
    keras.layers.Dense(512, input_dim = x_train.shape[1], activation='relu'),  
    keras.layers.Dense(512, input_dim = x_train.shape[1], activation='relu'),  
    keras.layers.Dense(units=256,activation='relu'),  
    keras.layers.Dense(units=256,activation='relu'),    
    keras.layers.Dense(units=128,activation='relu'),
    keras.layers.Dense(units=1, activation="linear"),



    ],name="Initial_model",)
    return model

def make_model_with_dropout(x_train):
    model=keras.models.Sequential([
    
    keras.layers.Dense(512, input_dim = x_train.shape[1], activation='relu'),  
    keras.layers.Dropout(0.3),
    
    keras.layers.Dense(512, activation='relu'),  
    keras.layers.Dropout(0.3),

    keras.layers.Dense(units=256,activation='relu'), 
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=256,activation='relu'), 
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=128,activation='relu'),
    keras.layers.Dense(units=1, activation="linear"),

    ],name="Dropout",)
    return model

def make_model_with_batch_normalization(x_train):
    model=keras.models.Sequential([
    
    keras.layers.Dense(512, input_dim = x_train.shape[1], activation='relu'), 
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    
    keras.layers.Dense(512, activation='relu'),  
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),

    keras.layers.Dense(units=256,activation='relu'), 
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=256,activation='relu'), 
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=128,activation='relu'),
    keras.layers.Dense(units=1, activation="linear"),
    ],name="Batchnorm",)
    return model

def make_model_with_leakyRelu(x_train):
    model=keras.models.Sequential([
    
    keras.layers.Dense(512, input_dim = x_train.shape[1]), 
    keras.layers.LeakyReLU(),
    keras.layers.Dropout(0.3),
    
    keras.layers.Dense(512),  
    keras.layers.LeakyReLU(),
    keras.layers.Dropout(0.3),

    keras.layers.Dense(units=256), 
    keras.layers.LeakyReLU(),
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=256), 
    keras.layers.LeakyReLU(),
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=128),
    keras.layers.LeakyReLU(), 
    keras.layers.Dense(units=1, activation="linear"),
    ],name="LeakyRELU",)
    return model

def make_model_with_extra_hidden_layer(x_train):
    model=keras.models.Sequential([
    
    keras.layers.Dense(1024, input_dim = x_train.shape[1]), 
    keras.layers.Dropout(0.4),
    
    keras.layers.Dense(512),  
    keras.layers.Dropout(0.3),

    keras.layers.Dense(512),  
    keras.layers.Dropout(0.3),
    
    keras.layers.Dense(units=256), 
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=256), 
    keras.layers.Dropout(0.01),
        
    keras.layers.Dense(units=128), 
    keras.layers.Dropout(0.05),
    keras.layers.Dense(units=1, activation="linear"),
    ],name="Larger_network",)
    return model

def make_model_with_callbackStop(x_train):
    model=keras.models.Sequential([
    
    keras.layers.Dense(1024, input_dim = x_train.shape[1]), 
    keras.layers.Dropout(0.4),
    
    keras.layers.Dense(512),  
    keras.layers.Dropout(0.3),

    keras.layers.Dense(512),  
    keras.layers.Dropout(0.3),
    
    keras.layers.Dense(units=256), 
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(units=256), 
    keras.layers.Dropout(0.01),
  
    keras.layers.Dense(units=128),
    keras.layers.Dropout(0.05),
    keras.layers.Dense(units=1, activation="linear"),
    ],name="Callbacks_stop",)
    return model