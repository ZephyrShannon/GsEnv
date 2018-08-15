# <codecell>

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from scipy import stats
import tensorflow as tf
import seaborn as sns
from pylab import rcParams
from sklearn.model_selection import train_test_split
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers


# <codecell>

def Outlier_Autoencoder(context,x,axis):

    # Assume x is a preprocessed selected factor exposure (Dictionary and DataFrame), \
    # with factor name as keys and dataframe where index-dates and columns-symbols as values \
    # ( !!! dates and symbols are equal to those of y's)
    x_dic = x
    factor_ls = list(x_dic.keys())
    symbol_ls = list(x_dic(factor_ls[0]).columns)
    date_ls = list(x_dic(factor_ls[0]).index)
    
    # check stock return outliers on all dates
    if axis == 0:
        for i in range(len(date_ls)):

            # obtain x and y array
            x_ls = []
            for value in x_dic.values():              
                x_df = value.asMatrix().iloc[i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)

        mae,mae_threshold = autoencoder_detection(x_array)

        # find outliers
        outlier_loc = np.where(mae >mae_threshold)[0]
        outlier=[]
        for i in range(len(outlier_loc)):
            outlier[i] = date_ls[outlier_loc[i]]
        return outlier

  
    if axis == 1:
        for i in range(len(symbol_ls)):
            # obtain x and y array
            x_ls = []
            y_series = y_df.iloc[:,i]
            for value in x_dic.values():
                x_df = value.asMatrix().iloc[:,i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)

        mae,mae_threshold = autoencoder_detection(x_array)

        # find outliers
        outlier_loc = np.where(mae >mae_threshold)[0]
        outlier=[]
        for i in range(len(outlier_loc)):
            outlier[i] = symbol_ls[outlier_loc[i]]
        return outlier
     

        

# <codecell>

def autoencoder_detection(x): 

    # standardize
    from sklearn.preprocessing import StandardScaler
    x_std = StandardScaler().fit_transform(x_array)

    ## data split (for evaluation purpose)
    RANDOM_SEED = 42
    x_train, x_test = train_test_split(x_std, test_size=0.2,random_state=RANDOM_SEED)

    ## build 4 layers (there are no specific rules for how may layers and nodes should be contained in hidden layer) 
    # eg. 28 - 14 - 14 - 56 
    input_dim = x_train.shape[1] 
    encoding_dim = int(input_dim/2)
    input_layer = Input(shape=(input_dim, ))
    # first dense layer: encoding_dim neurons
    # activation function "tanh" is ranged(-1,1) from (-0.5,0.5)
    # some examples use 'relu' for all the activations but only the last decoding layer as 'tanh'
    # apply penalty in loss function, can be customized
    encoder = Dense(encoding_dim, activation = "tanh", activity_regularizer = regularizers.l1(10e-5))(input_layer)
    # second dense layer: 7 neurons
    # activation function "ReLU(x) = max(0,x)" is ranged(0,1) 
    encoder = Dense(int(encoding_dim/2), activation = "relu")(encoder)
    decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
    decoder = Dense(input_dim, activation='relu')(decoder)

    autoencoder = Model(inputs=input_layer, outputs = decoder)

    ## trian the model: 

    # Set optimizer and loss function
    # optimizer: Adam - an algorihm for first-order gradient-based optimization of stochastic fn. https://arxiv.org/abs/1412.6980v8
    # metrics: to evaluate performance, similar to loss function, but not used during training
    autoencoder.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics =['accuracy'])

    # iteration times, the longer the more choices will have, also runs longer
    nb_epoch = 10
    # random samples size
    # default number is also 32
    batch_size = 32 
    # define "ModelCheckpoint" to save the best performing model to a file
    checkpointer = ModelCheckpoint(filepath="model.h5",verbose=0,  save_best_only=True)
    # additionally export the training process that TensorBoard can understand
    tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)
    # train the model
    # Verbosity 日志显示:  0 = silent, 1 = progress bar, 2 = one line per epoch
    # callbacks： 调回函数
    # return a history
    autoencoder_history = autoencoder.fit(x_train, x_train, epochs=nb_epoch,batch_size=batch_size,shuffle=True,\
                              validation_data=(x_test, x_test), verbose=1,\
                              callbacks=[checkpointer, tensorboard])

    ## run the model and compare with original dataset
    x_pred = autoencoder.predict(x_std)
    # find the maximum squared errors
    mae = np.max(np.power(x_std - x_pred, 2),axis =1)
    # define a threshold, can use a running mean instead
    mae_threshold = np.mean(mae)+np.std(mae)
    
    return mae, mae_threshold

# <codecell>

