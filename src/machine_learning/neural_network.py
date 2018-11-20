import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers

#%% FIRST PART: read original data
raw_data = pd.read_csv('data/input_output_data.csv', index_col=0)  # Read the CSV file
raw_data_np = raw_data.values
print(raw_data.head())
y = raw_data_np[:, 0]
X = raw_data_np[:, 1:]
y_name = list(raw_data)[0]
feature_names = list(raw_data)[1:]
N, M = X.shape
scaler = StandardScaler()
X_std = scaler.fit_transform(X)  # standardize data

#%% SECOND PART: two-layer cross-validation
K = 5  # Outer cross-validation fold: 5-Fold
CV = KFold(n_splits=K, shuffle=True)
# Initialize variables for artificial neural network
ANN_hidden_units = np.empty(K)         # Number of hidden units (Artificial Neural Network)
ANN_Error_train = np.empty(K)          # Train error (Artificial Neural Network)
ANN_Error_test = np.empty(K)           # Test error (Artificial Neural Network)
adam = optimizers.Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.00000001)

n_hidden_units_test = [150, 200, 250, 300]       # number of hidden units to check (multiplied by the number of inputs)
n_train = 2                                 # number of networks trained in each k-fold
batching_size = 2000                        # bathching size for the training
max_epochs = 1000                           # stop criterion 2 (max epochs in training)

k = 0
for train_index, test_index in CV.split(X):  # Outer 2-layer cross-validation loop
    print("\n OUTER CROSS-VALIDATION {0}/{1}".format(k+1, K))
    # extract training and test set for current CV fold
    X_train = X_std[train_index, :]
    y_train = y[train_index]
    X_test = X_std[test_index, :]
    y_test = y[test_index]

    K_internal = 5
    n_hidden_units_select = np.empty(K_internal)  # Store the selected number of hidden units
    inner_fold_error_ANN = np.empty(K_internal)   # Store the error for each inner fold

    CV_ANN = KFold(K_internal, shuffle=True)
    inner_k = 0
    for ann_train_index, ann_test_index in CV_ANN.split(X_train):
        print("   INNER CROSS-VALIDATION {0}/{1}".format(inner_k + 1, K_internal))
        X_ANN_train = X_train[ann_train_index]
        y_ANN_train = y_train[ann_train_index]
        X_ANN_test = X_train[ann_test_index]
        y_ANN_test = y_train[ann_test_index]

        bestnet = None
        best_train_error = np.inf
        best_val_error = np.inf
        bestlayer = None
        for n_hidden_units in n_hidden_units_test:
            print("      training with {0} hidden units...".format(n_hidden_units))
            for i in range(n_train):
                print('         training network {0}/{1}...'.format(i + 1, n_train))

                model = Sequential()
                model.add(Dense(n_hidden_units, input_shape=(M,)))
                model.add(Activation('relu'))
                model.add(Dense(1))
                model.add(Activation('linear'))
                model.compile(loss='mean_squared_error', optimizer=adam)
                history = model.fit(X_ANN_train, y_ANN_train, epochs=max_epochs, batch_size=batching_size,
                                    verbose=0, validation_data=(X_ANN_test, y_ANN_test))
                train_error = history.history['loss'][-1]
                val_error = history.history['val_loss'][-1]
                print('         Training error: {0}'.format(train_error))
                print('         Validation error: {0}'.format(val_error))
                if train_error < best_train_error:
                    bestnet = model
                    best_train_error = train_error
                    best_val_error = val_error
                    bestlayer = n_hidden_units
        print('   Best train error: {0} (with {1} hidden layers)'.format(best_train_error, bestlayer))
        print('   Best validation error: {0} (with {1} hidden layers)'.format(best_val_error, bestlayer))
        inner_fold_error_ANN[inner_k] = best_val_error
        n_hidden_units_select[inner_k] = bestlayer
        inner_k += 1
    best_index = np.asscalar(np.argmin(inner_fold_error_ANN))
    ANN_hidden_units[k] = n_hidden_units_select[best_index]

    bestnet = None
    best_train_error = np.inf
    best_val_error = np.inf
    for i in range(n_train):
        model = Sequential()
        aux = np.asscalar(n_hidden_units_select[best_index])
        model.add(Dense(int(np.asscalar(n_hidden_units_select[best_index])), input_shape=(M,)))
        model.add(Activation('relu'))
        model.add(Dense(1))
        model.add(Activation('linear'))
        model.compile(loss='mean_squared_error', optimizer=adam)

        history = model.fit(X_train, y_train, epochs=max_epochs, batch_size=batching_size, verbose=0,
                            validation_data=(X_test, y_test))
        train_error = history.history['loss'][-1]
        val_error = history.history['val_loss'][-1]
        print('        Training error: {0}'.format(train_error))
        print('        Validation error: {0}'.format(val_error))
        if train_error < best_train_error:
            bestnet = model
            best_train_error = train_error
            best_val_error = val_error

    plt.figure(figsize=(12, 6))
    plt.title('test values vs prediction (CV {0}/{1})'.format(k+1, K))
    plt.xlabel('actual power')
    plt.ylabel('predicted power')
    plt.plot(y_test, bestnet.predict(X_test), '.')
    plt.show()

    ANN_Error_train[k] = best_train_error
    ANN_Error_test[k] = best_val_error
    k += 1

# Figure with ANN generalization error
plt.figure(figsize=(9, 6))
plt.plot(range(1, ANN_Error_test.shape[0]+1), ANN_Error_test)
plt.xlabel('Iteration')
plt.ylabel('Squared error (crossvalidation)')
plt.title('Artificial Neural Network Generalization Error')
plt.show()
print('- [ANN] Number of hidden units for each fold: {0}'.format(str(ANN_hidden_units)))
print('- [ANN] Generalization error for each fold: {0}'.format(str(ANN_Error_test)))
