# <codecell>

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from functools import partial
import matplotlib.pyplot as plt
import time

# <codecell>




def autoencoder_outlier_detection(threshold, x):
    x_df = x
    index_ls = list(x_df.index)
    columns_ls = list(x_df.columns)
    
    # standardize
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_df.values)
    
    ## build topology
    n_input = x_train.shape[1] 
    n_hidden = 50
    n_reduction = 5

    training = tf.placeholder_with_default(False, shape=())

    # define placeholders
    x_input = tf.placeholder(tf.float32, shape = [None, n_input] )

    # to prevent the network just copying the originial data
    # adding noise to the input data or use dropout force the network learning the key features
    dropout_rate = 0.3
    x_drop = tf.layers.dropout(x_input, dropout_rate, training = training)

    # He initialization
    he_init = tf.contrib.layers.variance_scaling_initializer()
    #Equivalent to:
    #he_init = lambda shape, dtype=tf.float32: tf.truncated_normal(shape, 0., stddev=np.sqrt(2/shape[0])) 


    my_dense_layer = partial(tf.layers.dense, activation=tf.nn.relu, kernel_initializer = he_init)

    hidden_1 = my_dense_layer(x_drop, n_hidden)
    hidden_2 = my_dense_layer(hidden_1, n_reduction)
    hidden_3 = my_dense_layer(hidden_2, n_hidden)
    x_output = my_dense_layer(hidden_3, n_input, activation=None)


    #  loss
    loss = tf.reduce_mean(tf.squared_difference(x_output, x_input))

    # learning rate
    lr = 0.01
    # optimizer
    op = tf.train.AdamOptimizer(lr).minimize(loss)
    init = tf.global_variables_initializer()
    
    # train the model
    start_time=time.time()

    # epoch number
    n_epoch = 500

    train_loss_ls = []
    

    with tf.Session() as sess:

        # initialize weight and bias
        init.run()

        for e in range(n_epoch): 

            sess.run(op, feed_dict = {x_input:x_train, training:True})

            train_loss = loss.eval(feed_dict = {x_input:x_train})
            train_loss_ls.append(train_loss)

        # save the values of weight and bias
        # weight, bias = sess.run([w,b]) 
        reconstructed_x = x_output.eval(feed_dict={x_input:x_train})

    elapsed_time = time.time()-start_time
    print('the training takes',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))   
    
    # outlier
    reconstructed_x_df = outlier(x_df, reconstructed_x, x_train, index_ls, columns_ls, threshold)
    
    return reconstructed_x_df



# <codecell>

# plot loss

def plot_loss(train_loss_ls):
    plt.plot(train_loss_ls, label = 'training loss')
    plt.title('training loss')
    plt.legend()
    plt.show()
    
# plot_loss(train_loss_ls)


# <codecell>

# outlier detection
def outlier(x_df, reconstructed_x, x_train, index_ls, columns_ls, threshold):
    se = np.power((x_train - reconstructed_x), 2)
    se_df = pd.DataFrame(se, index =  index_ls, columns=columns_ls)

    for i in range(len(columns_ls)):
        s = se_df.iloc[:,i]
        mse_threshold = np.mean(s)+np.std(s)*threshold
        s[s>mse_threshold]= np.nan

    reconstructed_x_df = x_df.where(pd.notnull(se_df), np.nan)
    return reconstructed_x_df


# <codecell>

