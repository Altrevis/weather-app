import pandas as pd
import joblib

model = joblib.load('weather_model.pkl')
scaler = joblib.load('scaler.pkl')

new_data = pd.DataFrame({
    'Minimum temperature at 2 metres': [10],
    'Maximum temperature at 2 metres': [20]
})

new_data_scaled = scaler.transform(new_data)
predicted_temperature = model.predict(new_data_scaled)
print(f"Température prédite : {predicted_temperature[0]:.2f}°C")