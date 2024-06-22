import joblib
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras import losses, utils


def root_mean_squared_error(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_pred - y_true)))

with utils.custom_object_scope({'root_mean_squared_error': root_mean_squared_error}):
    model = load_model("./routes/modelsave/modelo.h5")
scaler = joblib.load("./routes/modelsave/scaler.pkl")


def predecir(x, model, scaler):
    x_s = scaler.transform(np.array(x).reshape(-1, 1))
    x_s = x_s.reshape((1, x_s.shape[0], x_s.shape[1]))
    y_pred_s = model.predict(x_s)
    y_pred = scaler.inverse_transform(y_pred_s)
    return y_pred.flatten()


# Ejemplo de uso
# x = [100, 120, 210, 300, 200]
# prediccion = pronosticar(x, model, scaler)
# print(prediccion)
