import pandas as pd
import matplotlib.pyplot as plt

from keras.models import model_from_json
from keras import optimizers

json_file = open('data/ann_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("data/ann_weights.h5")
adam = optimizers.Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.00000001)
loaded_model.compile(loss='mean_squared_error', optimizer=adam)
model = loaded_model
model._make_predict_function()
# load normalization data
norm_data = pd.read_csv('data/ann_normalization.csv')
mean = norm_data.values[:, [0]].T
std = norm_data.values[:, [1]].T

print("(ANN predictor) Loaded model from disk")

data = pd.read_csv('data/data_training.csv', index_col=0)  # Read the CSV file
y = data.values[:, [0]]
X = data.values[:, 1:]
X = (X - mean) / std
prediction = model.predict(X)
y_l = y - 1e5
y_m = y + 1e5
y_l = y_l.sort(axis=0)
y_m = y_m.sort(axis=0)
y_more = y_m.copy()
y_less = y_l.copy()
y_less[y_l[:, 0] < 2e6] = y_l[:, 0] * 0.8
# Plot final model performance
plt.figure(figsize=(12, 9))
plt.title('train values vs prediction')
plt.xlabel('actual power')
plt.ylabel('predicted power')
plt.ticklabel_format(style='plain')
plt.plot(y, prediction, '.')
plt.plot(y, y)
plt.plot(y, y_less*0.8)
plt.plot(y, y_more*1.2)
#plt.legend(['predictions', 'ideal'])
plt.show()
