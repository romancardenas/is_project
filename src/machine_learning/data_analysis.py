import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#%% FIRST PART: read original data
raw_data = pd.read_csv('data/original_data.csv', index_col=0, parse_dates=True)  # Read the CSV file
raw_data_np = raw_data.values
print(raw_data.head())
y = raw_data_np[:, 0]
X = raw_data_np[:, 1:]
y_name = list(raw_data)[0]
feature_names = list(raw_data)[1:]
N, M = X.shape
del raw_data_np

#%% SECOND PART: data representation
print(type(raw_data.index))
time = raw_data.index.values.astype(np.int64) // 10 ** 9
for column in list(raw_data):
    plt.figure(figsize=(12, 6))
    plt.title(column)
    plt.xlabel('time')
    plt.ylabel(column)
    plt.plot(time, raw_data[column], '*')
    plt.xticks(rotation='vertical')
    #raw_data.plot.scatter(raw_data.ix, column)
    plt.show()

for column1 in list(raw_data):
    if column1 != 'output_power':
        plt.figure(figsize=(12, 6))
        plt.title('{0} vs output power'.format(column1))
        plt.xlabel(column1)
        plt.ylabel('output power')
        plt.plot(raw_data[column1], raw_data['output_power'], '*')
        plt.xticks(rotation='vertical')
        # raw_data.plot.scatter(raw_data.ix, column)
        plt.show()

#%% THIRD PART: PCA Analysis
scaler = StandardScaler()
std_X = scaler.fit_transform(X)  # standardize data
# Then apply PCA.
pca = PCA()  # We will use only 20 components
pca.fit(std_X)  # Apply PCA to the standardized data
pca_info = np.empty(M)
for i in range(0, M):
    pca_info[i] = sum(pca.explained_variance_ratio_[0:i+1])
for i in range(0, M):
    if pca_info[i] > 0.9:
        print('We need at least ' + str(i+1) + ' PCA components in order to preserve 90% of information.')
        break
plt.figure(figsize=(12, 6))
plt.title('PCA Analysis')
plt.xlabel('number of PC')
plt.ylabel('explained variance')
plt.plot(range(1, M+1), pca_info)
plt.show()
