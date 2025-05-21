import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class ForestCoverModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.all_features = [
            'Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
            'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
            'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
            'Horizontal_Distance_To_Fire_Points',
            'Wilderness_Area_1', 'Wilderness_Area_2', 'Wilderness_Area_3', 'Wilderness_Area_4',
            'Soil_Type_1', 'Soil_Type_2', 'Soil_Type_3', 'Soil_Type_4', 'Soil_Type_5',
            'Soil_Type_6', 'Soil_Type_7', 'Soil_Type_8', 'Soil_Type_9', 'Soil_Type_10',
            'Soil_Type_11', 'Soil_Type_12', 'Soil_Type_13', 'Soil_Type_14', 'Soil_Type_15',
            'Soil_Type_16', 'Soil_Type_17', 'Soil_Type_18', 'Soil_Type_19', 'Soil_Type_20',
            'Soil_Type_21', 'Soil_Type_22', 'Soil_Type_23', 'Soil_Type_24', 'Soil_Type_25',
            'Soil_Type_26', 'Soil_Type_27', 'Soil_Type_28', 'Soil_Type_29', 'Soil_Type_30',
            'Soil_Type_31', 'Soil_Type_32', 'Soil_Type_33', 'Soil_Type_34', 'Soil_Type_35',
            'Soil_Type_36', 'Soil_Type_37', 'Soil_Type_38', 'Soil_Type_39', 'Soil_Type_40'
        ]
    
    def load_model(self):
        """Carga el modelo pre-entrenado y el escalador desde un archivo pickle"""
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Modelos', 'modelo_y_scaler.pkl')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No se encontró el modelo en {model_path}")
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            
        # Extraer el modelo y el escalador del diccionario cargado
        self.model = model_data['modelo']
        self.scaler = model_data['escalador']
    
    def _preprocess_input(self, features):
        """Preprocesa los datos de entrada para asegurar que tienen el formato correcto"""
        if isinstance(features, dict):
            # Convertir un solo diccionario a DataFrame
            df = pd.DataFrame([features])
        else:
            # Ya es un DataFrame
            df = features
        
        # Asegurar que todas las características necesarias estén presentes
        for feature in self.all_features:
            if feature not in df.columns:
                df[feature] = 0
        
        # Seleccionar solo las columnas necesarias en el orden correcto
        return df[self.all_features]
    
    def predict(self, features):
        """Realiza predicciones utilizando el modelo cargado"""
        if self.model is None:
            raise ValueError("El modelo no ha sido cargado. Llame a load_model() primero.")
        
        # Preprocesar los datos de entrada
        X = self._preprocess_input(features)
        
        # Obtener las columnas cuantitativas que necesitan ser escaladas
        columnas_cuantitativas = [
            'Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
            'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
            'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
            'Horizontal_Distance_To_Fire_Points'
        ]
        
        # Aplicar el escalador a las columnas cuantitativas
        X[columnas_cuantitativas] = self.scaler.transform(X[columnas_cuantitativas])
        
        # Realizar la predicción
        predictions = self.model.predict(X)
        
        # Obtener las probabilidades para cada clase
        probabilities = self.model.predict_proba(X)
        
        return predictions, probabilities

