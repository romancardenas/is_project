import pandas as pd

from keras.models import model_from_json
from keras import optimizers


class Predictor:
    def __init__(self):
        # load json and create model
        json_file = open('data/ann_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("data/ann_weights.h5")
        adam = optimizers.Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.00000001)
        loaded_model.compile(loss='mean_squared_error', optimizer=adam)
        self.model = loaded_model
        self.model._make_predict_function()
        # load normalization data
        norm_data = pd.read_csv('data/ann_normalization.csv')
        self.mean = norm_data.values[:, [0]].T
        self.std = norm_data.values[:, [1]].T

        print("(ANN predictor) Loaded model from disk")

    def predict(self, data):
        aux = {i: [j] for i, j in data.items()}
        del aux['status']
        del aux['time']
        df = pd.DataFrame.from_dict(aux)
        input_data = df.values[:, 1:]
        input_data = (input_data - self.mean) / self.std
        return self.model.predict(input_data)


if __name__ == '__main__':
    predictor = Predictor()
    # This is the first raw from data_simulation.csv
    data = {'status': 'active', 'time': '2010-01-01 00:00:00+01:00', 'output_power': 2350610.791859267, 'wind_speed': 5.326969999999998,
            'temperature': 267.6, 'pressure': 98405.7}
    prediction = predictor.predict(data)
    if prediction < data['output_power']*0.8:
        print("TOO LOW")
    elif prediction > data['output_power']*1.2:
        print("TOO HIGH")
    else:
        print("GOOD PREDICTION")
