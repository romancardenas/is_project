import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


from keras.models import model_from_json
from keras import optimizers

sns.set()
colors = ["silver", "amber", "dark turquoise", "faded green", "dusty purple"]
sns.set_palette(sns.xkcd_palette(colors))

json_file = open('../data/ann_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("../data/ann_weights.h5")
adam = optimizers.Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.00000001)
loaded_model.compile(loss='mean_squared_error', optimizer=adam)
model = loaded_model
model._make_predict_function()
# load normalization data
norm_data = pd.read_csv('../data/ann_normalization.csv')
mean = norm_data.values[:, [0]].T
std = norm_data.values[:, [1]].T

print("(ANN predictor) Loaded model from disk")

data = pd.read_csv('../data/data_training.csv', index_col=0)  # Read the CSV file
y = data.values[:, [0]]
X = data.values[:, 1:]
X = (X - mean) / std
prediction = model.predict(X)

#y_s = y.copy()
y_s = prediction.copy()
y_s.sort(axis=0)

y_l = y_s - 2e5
y_m = y_s + 2e5
y_more = y_s.copy()
y_less = y_s.copy()



y_less[:, 0] = 7.3e6
y_less[y_s[:, 0] < 8.2e6] = y_l[y_s[:, 0] < 8.2e6]*0.8 + 0.8e6 # TODO
y_less[y_s[:, 0] < 5.6e6] = (y_l[y_s[:, 0] < 5.6e6]) * 1.12 - 0.9e6
y_less[y_s[:, 0] < 2.8e6] = y_l[y_s[:, 0] < 2.8e6] * 0.8

y_more[:, 0] = 7.7e6 # TODO
y_more[y_s[:, 0] < 7.8e6] = y_m[y_s[:, 0] < 7.8e6] * 0.65 + 2.5e6
y_more[y_s[:, 0] < 5.6e6] = y_m[y_s[:, 0] < 5.6e6] * 0.76 + 1.9e6
y_more[y_s[:, 0] < 5e6] = y_m[y_s[:, 0] < 5e6] * 1.1 + 0.2e6
y_more[y_s[:, 0] < 2.5e6] = y_m[y_s[:, 0] < 2.5e6] * 1.2

# Plot final model performance
#plt.figure(figsize=(24, 18))

plt.figure(figsize=(24, 18))
plt.title('Train Values vs Prediction', fontsize=60)
plt.ylabel('Actual Power (MWatts)', fontsize=50)
plt.xlabel('Predicted Power (MWatts)', fontsize=50)
plt.ticklabel_format(style='plain')
plt.plot(prediction/1e6, y/1e6, '.', markersize=10)
plt.plot(y/1e6, y/1e6, linewidth=4)
plt.plot(y_s/1e6, y_less/1e6, '--', linewidth=4)
plt.plot(y_s/1e6, y_more/1e6, '--',  linewidth=4)
plt.tick_params(labelsize=35)
#plt.legend(['Predictions', 'Linear'])
plt.legend(['Predictions', 'Linear', 'Lower Limit', 'Upper Limit'], fontsize=50)
plt.show()
