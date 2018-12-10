import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, preprocessing
from sklearn.model_selection import train_test_split
from neupy import algorithms, layers, environment


def rmsle(expected, predicted):
    log_expected = np.log1p(expected + 1)
    log_predicted = np.log1p(predicted + 1)
    squared_log_error = np.square(log_expected - log_predicted)
    return np.sqrt(np.mean(squared_log_error))


environment.reproducible()
plt.style.use('ggplot')

dataset = datasets.load_boston()
data = dataset.data
target = dataset.target.reshape((-1, 1))

data_scaler = preprocessing.MinMaxScaler((-3, 3))
target_scaler = preprocessing.MinMaxScaler()

data = data_scaler.fit_transform(data)
target = target_scaler.fit_transform(target)

x_train, x_test, y_train, y_test = train_test_split(
    data, target, test_size=0.15
)

cgnet = algorithms.Hessian(
    connection=[
        layers.Input(13),
        layers.Sigmoid(50),
        layers.Sigmoid(10),
        layers.Sigmoid(1),
    ],
    verbose=True,
)

cgnet.train(x_train, y_train, x_test, y_test, epochs=3)
y_predict = cgnet.predict(x_test)

y_test = target_scaler.inverse_transform(y_test.reshape((-1, 1)))
y_predict = target_scaler.inverse_transform(y_predict).T.round(1)
error = rmsle(y_predict, y_test)
print("RMSLE = {}".format(error))