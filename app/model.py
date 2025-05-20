import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import os

class ForestCoverModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
            'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
            'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
            'Horizontal_Distance_To_Fire_Points'
        ]
        self.wilderness_areas = ['Wilderness_Area_' + str(i) for i in range(1, 5)]
        self.soil_types = ['Soil_Type_' + str(i) for i in range(1, 41)]
        self.all_features = self.feature_names + self.wilderness_areas + self.soil_types
        self.target_name = 'Cover_Type'
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        os.makedirs(self.model_path, exist_ok=True)
    
    def load_data(self, data_path):
        """Carga los datos desde el archivo CSV"""
        # El dataset tiene 54 columnas: 10 numéricas + 4 wilderness areas + 40 soil types + 1 target
        column_names = self.feature_names + self.wilderness_areas + self.soil_types + [self.target_name]
        
        # Cargar datos sin encabezados
        data = pd.read_csv(data_path, header=None, names=column_names)
        
        return data
    
    def preprocess_data(self, data):
        """Preprocesa los datos para el entrenamiento"""
        X = data[self.all_features]
        y = data[self.target_name]
        
        # Escalar solo las características numéricas
        X_numeric = X[self.feature_names]
        X_numeric_scaled = self.scaler.fit_transform(X_numeric)
        
        # Reemplazar las columnas numéricas con sus versiones escaladas
        X_scaled = X.copy()
        X_scaled[self.feature_names] = X_numeric_scaled
        
        return X_scaled, y
    
    def train(self, X, y):
        """Entrena el modelo de clasificación"""
        # Dividir datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entrenar el modelo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.model.fit(X_train, y_train)
        
        # Evaluar el modelo
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(report)
        
        return accuracy, report
    
    def save_model(self, model_filename='forest_cover_model.joblib', scaler_filename='scaler.joblib'):
        """Guarda el modelo entrenado y el scaler"""
        if self.model is None:
            raise ValueError("El modelo no ha sido entrenado aún")
        
        model_path = os.path.join(self.model_path, model_filename)
        scaler_path = os.path.join(self.model_path, scaler_filename)
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        print(f"Modelo guardado en: {model_path}")
        print(f"Scaler guardado en: {scaler_path}")
        
        return model_path, scaler_path
    
    def load_model(self, model_filename='forest_cover_model.joblib', scaler_filename='scaler.joblib'):
        """Carga un modelo previamente entrenado"""
        model_path = os.path.join(self.model_path, model_filename)
        scaler_path = os.path.join(self.model_path, scaler_filename)
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError(f"No se encontró el modelo en {model_path} o el scaler en {scaler_path}")
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        return self.model, self.scaler
    
    def predict(self, features):
        """Realiza predicciones con el modelo entrenado"""
        if self.model is None:
            raise ValueError("El modelo no ha sido cargado o entrenado")
        
        # Asegurarse de que las características estén en el formato correcto
        if isinstance(features, pd.DataFrame):
            # Si es un DataFrame, asegurarse de que tenga las columnas correctas
            missing_cols = set(self.all_features) - set(features.columns)
            if missing_cols:
                raise ValueError(f"Faltan las siguientes columnas: {missing_cols}")
            
            # Ordenar las columnas para que coincidan con el orden de entrenamiento
            features = features[self.all_features]
        elif isinstance(features, dict):
            # Si es un diccionario, convertirlo a DataFrame
            features = pd.DataFrame([features])
            
            # Asegurarse de que todas las características binarias estén presentes
            for col in self.wilderness_areas + self.soil_types:
                if col not in features:
                    features[col] = 0
        else:
            raise ValueError("Las características deben ser un DataFrame o un diccionario")
        
        # Escalar las características numéricas
        features_numeric = features[self.feature_names]
        features_numeric_scaled = self.scaler.transform(features_numeric)
        features_scaled = features.copy()
        features_scaled[self.feature_names] = features_numeric_scaled
        
        # Realizar la predicción
        prediction = self.model.predict(features_scaled)
        probabilities = self.model.predict_proba(features_scaled)
        
        return prediction, probabilities


def train_and_save_model():
    """Función para entrenar y guardar el modelo"""
    # Ruta al archivo de datos
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'covtype.data')
    
    # Crear y entrenar el modelo
    model = ForestCoverModel()
    data = model.load_data(data_path)
    X, y = model.preprocess_data(data)
    accuracy, report = model.train(X, y)
    model.save_model()
    
    return model, accuracy, report


if __name__ == "__main__":
    train_and_save_model()