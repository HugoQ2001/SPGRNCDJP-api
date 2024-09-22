import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

# Definir la arquitectura del modelo (debe ser la misma con la que entrenaste el modelo)
class GastoPredictor(nn.Module):
    def __init__(self):
        super(GastoPredictor, self).__init__()
        self.fc1 = nn.Linear(5, 10)  # 5 entradas -> 10 neuronas ocultas
        self.fc2 = nn.Linear(10, 1)  # 10 neuronas ocultas -> 1 salida (el gasto futuro)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def predecirgasto(nuevos_gastos_otra_persona, model_path='./modelornn/modelo_rnn.pth', 
                   scaler_gastos_path='./modelornn/scaler_gastos.pkl', scaler_futuro_path='./modelornn/scaler_futuro.pkl'):
    # Cargar el modelo
    model = GastoPredictor()
    model.load_state_dict(torch.load(model_path))
    model.eval()  # Poner el modelo en modo evaluación

    # Cargar los escaladores previamente entrenados
    scaler_gastos = joblib.load(scaler_gastos_path)  # Escalador para los gastos de entrada
    scaler_futuro = joblib.load(scaler_futuro_path)  # Escalador para los gastos futuros (salida)

    # Escalar los nuevos gastos utilizando el mismo escalador usado para los datos de entrenamiento
    nuevos_gastos_scaled = scaler_gastos.transform(nuevos_gastos_otra_persona)

    # Convertir a tensor de PyTorch
    nuevos_gastos_tensor = torch.FloatTensor(nuevos_gastos_scaled)

    # Hacer la predicción usando el modelo cargado
    with torch.no_grad():  # Deshabilitar el cálculo del gradiente para predicción
        prediccion_nuevos_gastos = model(nuevos_gastos_tensor)
        prediccion_gasto = scaler_futuro.inverse_transform(prediccion_nuevos_gastos.numpy())  # Desescalar

    return prediccion_gasto[0][0]

# Ejemplo de uso
nuevos_gastos_otra_persona = np.array([[400, 500, 600, 700, 800]])  # Nuevos gastos de prueba
prediccion = predecirgasto(nuevos_gastos_otra_persona)
print(f"Predicción del sexto gasto para la nueva persona: {prediccion}")
