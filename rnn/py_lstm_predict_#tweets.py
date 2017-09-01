
# coding: utf-8

# In[2]:

#
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential


# In[7]:

#load data
df_all = pd.read_csv('./processed_features/Hashtag_Count_Hourly_NeuScore.csv', index_col=0)
df = df_all.ix[:,0:]
print('Raw Data shape:', df.shape)


# In[8]:

#filter rows that contains a lot of zero
rows = (df != 0).sum(1)
#print(rows[0:5])
rows_filtered = rows > 0.1*df.shape[1]
#print(rows_filtered[0:5])


# In[9]:

df_filtered = df[rows_filtered]
print(df_filtered.shape)
#print(df_filtered[0:5])


# In[13]:

from sklearn.preprocessing import normalize
# define a function to convert a vector of time series into a 2D matrix
def convertDataToSequence(df, seq_len, normalise_window):
    sequence_length = seq_len + 1
    result = []
    for index in range(len(df.columns) - sequence_length):
        #print(index, index+sequence_length)
        result.append(np.array(df.ix[:,index:index + sequence_length]))
    print(len(result))
    if normalise_window:
        result = normalise_windows(result)
        #result = result.div(result.sum(axis=1), axis=0)   

    result = np.array(result)    
    print('result:', result.shape)
    result = np.reshape(result, (result.shape[0]*result.shape[1], result.shape[2]))
    print('result:', result.shape)

    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    print('train:', train.shape)
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1]
    print('x_train:', x_train.shape, 'y_train:', y_train.shape)
    print('x_test:', x_test.shape, 'y_test:', y_test.shape)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1)) 

    return [x_train, y_train, x_test, y_test]

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        #normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        #print(window.shape)
        #row_sums = window.sum(axis=1)
        #normalised_data.append(window / row_sums[:, np.newaxis])
        normalised_window = normalize(window, axis=1, norm='l1')
        normalised_data.append(normalised_window)
    return normalised_data
def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_shape=(layers[1], layers[0]),
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print("> Compilation Time : ", time.time() - start)
    return model

def predict_point_by_point(model, data):
    #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted

def predict_sequence_full(model, data, window_size):
    #Shift the window by 1 new prediction each time, re-run predictions on new window
    curr_frame = data[0]
    predicted = []
    for i in range(len(data)):
        predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
        curr_frame = curr_frame[1:]
        curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
    return predicted

def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of 50 steps before shifting prediction run forward by 50 steps
    prediction_seqs = []
    for i in range(int(len(data)/prediction_len)):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs


# In[14]:

import time
import matplotlib.pyplot as plt
from numpy import newaxis

def plot_results(predicted_data, true_data, fileName):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()
    fig.savefig(fileName, bbox_inches='tight')

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()


# In[ ]:

global_start_time = time.time()
epochs  = 100
seq_len = 24

print('> Loading data... ')

X_train, y_train, X_test, y_test = convertDataToSequence(df_filtered, seq_len, True) #False

print('> Data Loaded. Compiling...')

model = build_model([1, 24, 128, 1])

model.fit(
    X_train,
    y_train,
    batch_size=512,
    nb_epoch=epochs,
    validation_split=0.05)

#predictions = predict_sequences_multiple(model, X_test, seq_len, 50)
#predicted = predict_sequence_full(model, X_test, seq_len)
predicted = predict_point_by_point(model, X_test)        

print('Training duration (s) : ', time.time() - global_start_time)
#plot_results_multiple(predictions, y_test, 50)
plot_results(predicted, y_test, 'output_prediction_NeuScore_100epoch_wd24_1x24x128x1.jpg')
np.savetxt('output_prediction_NeuScore_100epoch_wd24_1x24x128x1.txt', predicted)


# In[78]:

# evaluate the result
test_mse = model.evaluate(X_test, y_test, verbose=1)
print('\nThe mean squared error (MSE) on the test data set is %.6f over %d test samples.' 
      % (test_mse, len(y_test)))

