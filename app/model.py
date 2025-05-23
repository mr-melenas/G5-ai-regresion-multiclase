import os
import pickle
import pandas as pd
import numpy as np
import joblib
import gdown
from sklearn.pipeline import Pipeline


class ForestCoverModel:
    def __init__(self):
        self.model = None
        # Características numéricas
        self.numeric_features = [
            'Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
            'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
            'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
            'Horizontal_Distance_To_Fire_Points'
        ]
        
        # Características de área silvestre (sin guion bajo adicional para coincidir con la API)
        self.wilderness_features = [
            f'Wilderness_Area{i}' for i in range(1, 5)
        ]
        
        # Características de tipo de suelo (sin guion bajo adicional para coincidir con la API)
        self.soil_features = [
            f'Soil_Type{i}' for i in range(1, 41)
        ]
        
        # Lista completa de características que el modelo espera
        self.all_features = self.numeric_features + self.wilderness_features + self.soil_features
    
    def load_model(self):
        """Carga el modelo pipeline pre-entrenado desde un archivo pickle"""
        #model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Modelos', 'modelo_pipeline.pkl')

        #nuevo code prueba-----------------------------------------------------------
        file_id = "1GN0VQ_E3BBkpYWICEx9yehcwxm0BAFxC"
        output_path = "modelo_pipeline.pkl"
        gdown.download(url, output_path, quiet=False)
        if not os.path.exists(output_path):
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, output_path, quiet=False)

        with open(output_path, "rb") as f:
            modelo = pickle.load(f)

        
        #nuevo code prueba-------------------------------------------------------
        
        # if not os.path.exists(model_path):
        #     raise FileNotFoundError(f"No se encontró el modelo en {model_path}")
        
        # try:
        #     # Intentar cargar el modelo con diferentes opciones
        #     with open(model_path, 'rb') as f:
        #         self.model = pickle.load(f, encoding='latin1')
        # except Exception as e:
        #     # Si falla, intentar con joblib
        #     try:
        #         self.model = joblib.load(model_path)
        #     except Exception as e2:
        #         error_msg = f"Error al cargar el modelo: {str(e)} / {str(e2)}"
        #         print(error_msg)
        #         raise ValueError(error_msg)
        
        # # Verificar que el modelo sea un pipeline válido
        # if self.model is None:
        #     raise ValueError("El modelo cargado es None")
        # #preprando cambio de modelo
        # print(f"Modelo cargado correctamente desde {model_path}")
        # print(f"Tipo de modelo: {type(self.model)}")

        return modelo
        
    
    def _preprocess_input(self, features):
        """Preprocesa los datos de entrada para asegurar que tienen el formato correcto"""
        if isinstance(features, dict):
            # Convertir un solo diccionario a DataFrame
            df = pd.DataFrame([features])
        else:
            # Ya es un DataFrame
            df = features
        
        # Mapeo de nombres de columnas: convertir de 'Soil_Type1' a 'Soil_Type_1' y viceversa
        column_mapping = {}
        
        # Crear mapeo para Wilderness_Area
        for i in range(1, 5):
            input_col = f'Wilderness_Area{i}'
            model_col = f'Wilderness_Area_{i}'
            if input_col in df.columns:
                column_mapping[input_col] = model_col
            elif model_col in df.columns:
                column_mapping[model_col] = input_col
        
        # Crear mapeo para Soil_Type
        for i in range(1, 41):
            input_col = f'Soil_Type{i}'
            model_col = f'Soil_Type_{i}'
            if input_col in df.columns:
                column_mapping[input_col] = model_col
            elif model_col in df.columns:
                column_mapping[model_col] = input_col
        
        # Renombrar columnas si es necesario
        if column_mapping:
            df = df.rename(columns=column_mapping)
        
        # Asegurar que todas las características necesarias estén presentes
        for feature in self.all_features:
            if feature not in df.columns:
                df[feature] = 0
        
        # Seleccionar solo las columnas necesarias en el orden correcto
        return df[self.all_features]
    
    def predict(self, features):
        """Realiza predicciones utilizando el modelo pipeline cargado"""
        if self.model is None:
            raise ValueError("El modelo no ha sido cargado. Llame a load_model() primero.")
        
        try:
            # Preprocesar los datos de entrada
            X = self._preprocess_input(features)
            
            # Realizar la predicción usando el pipeline completo
            # (el pipeline ya incluye el preprocesamiento y escalado)
            predictions = self.model.predict(X)
            
            # Obtener las probabilidades para cada clase
            probabilities = self.model.predict_proba(X)
            
            return predictions, probabilities
        except Exception as e:
            error_msg = f"Error durante la predicción: {str(e)}"
            print(error_msg)
            raise ValueError(error_msg)

