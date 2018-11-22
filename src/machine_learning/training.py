import pandas as pd
import numpy as np

raw_data = pd.read_csv('data/input_output_data.csv', index_col=0)  # Read the CSV file
raw_data_np = raw_data.values
y = raw_data_np[:, 0]
X = raw_data_np[:, 1:]
y_name = list(raw_data)[0]
feature_names = list(raw_data)[1:]

X_mean = X.mean(axis=0)
X_std = X.std(axis=0)

print(X_mean)
print(X_std)

X = (X - X_mean) / X_std
print(X.mean(axis=0))
print(X.std(axis=0))
a = np.concatenate((X_mean, X_std)).reshape(2, X_mean.shape[0]).T
print(a)
a = pd.DataFrame({'mean': a[:, 0], 'std_deviation': a[:, 1]})
print(a)
a.to_csv('data/ann_normalization.csv', index=False)
