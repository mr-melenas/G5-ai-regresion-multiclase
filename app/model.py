import os
import pickle
import pandas as pd
import numpy as np
import joblib
import tempfile
from sklearn.pipeline import Pipeline


class ForestCoverModel:
    def __init__(self):
        self.model = None
        self.scaler = None
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
        """Carga el modelo pipeline pre-entrenado desde Google Drive o desde partes comprimidas"""
        import gdown
        import glob
        import tempfile
        
        # Directorio para almacenar el modelo descargado
        models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Modelos')
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, 'modelo_pipeline.pkl')
        model_parts_dir = os.path.join(models_dir, 'model_parts')
        os.makedirs(model_parts_dir, exist_ok=True)
        
        # URL de Google Drive (mantener como respaldo)
        url = 'https://drive.google.com/file/d/1GN0VQ_E3BBkpYWICEx9yehcwxm0BAFxC/view?usp=drive_link'
        
        # URLs para las partes del modelo (reemplazar con las URLs reales cuando estén disponibles)
        model_parts_urls = [
            'https://drive.google.com/file/d/1KU13D-G7KOzrs7uCWYNiCjC2Xgi6l7uu/view?usp=drive_link',
            'https://drive.google.com/file/d/1_9HcL6JLvgHkUS51QwRCz0PpRGie35BZ/view?usp=drive_link',
            'https://drive.google.com/file/d/1u4Mih3tvZ6NUp3HDjxz0SgC-phyHs61t/view?usp=drive_link',
            'https://drive.google.com/file/d/14cQ_sEVIoAsFHr0lZzVBRkD94osHiSXw/view?usp=drive_link',
            'https://drive.google.com/file/d/142DbxSzfi_Cr1k5AxRtFuZnythSiAoo_/view?usp=drive_link',
            'https://drive.google.com/file/d/10fYIEs7C7jth4AiTt-Jm4FEFHoQQ2N8A/view?usp=drive_link',
            'https://drive.google.com/file/d/1ZCBZjAJWuUzKbhk3k9Y9hkk0bVeDQp6p/view?usp=drive_link',
            'https://drive.google.com/file/d/1a9J2ahmZQuPdHMwaSeYmAgF69YsMEhZD/view?usp=drive_link',
            'https://drive.google.com/file/d/1oYad0b9UhEjyJF3yIOsfd0Ijpy7QHPyK/view?usp=drive_link'
        ]
        
        try:
            # Verificar si el modelo ya existe localmente
            if os.path.exists(model_path):
                print(f"Usando modelo existente en {model_path}")
                try:
                    # Intentar cargar el modelo completo
                    self.model = joblib.load(model_path)
                    print(f"Modelo cargado correctamente")
                    return
                except Exception as e:
                    print(f"Error al cargar el modelo completo: {str(e)}. Intentando cargar desde partes...")
            
            # Verificar si existen partes del modelo
            model_parts = sorted(glob.glob(os.path.join(model_parts_dir, 'model_part_*.joblib')))
            
            if model_parts:
                print(f"Cargando modelo desde {len(model_parts)} partes...")
                # Cargar el modelo desde partes
                self._load_model_from_parts(model_parts)
                return
            
            # Si no hay modelo ni partes, intentar descargar las partes
            if model_parts_urls:
                print("Descargando partes del modelo...")
                downloaded_parts = []
                for i, url in enumerate(model_parts_urls):
                    part_path = os.path.join(model_parts_dir, f'model_part_{i:03d}.joblib')
                    if not os.path.exists(part_path):
                        print(f"Descargando parte {i+1}/{len(model_parts_urls)}...")
                        gdown.download(url=url, output=part_path, quiet=False, fuzzy=True)
                    downloaded_parts.append(part_path)
                
                # Cargar el modelo desde las partes descargadas
                if downloaded_parts:
                    self._load_model_from_parts(downloaded_parts)
                    return
            
            # Si todo lo anterior falla, intentar descargar el modelo completo
            print(f"Descargando modelo completo desde Google Drive...")
            gdown.download(url=url, output=model_path, quiet=False, fuzzy=True)
            print(f"Modelo descargado correctamente en {model_path}")
            
            # Intentar cargar el modelo completo
            try:
                self.model = joblib.load(model_path)
            except Exception as e:
                # Si falla, intentar con pickle
                try:
                    with open(model_path, 'rb') as f:
                        self.model = pickle.load(f, encoding='latin1')
                except Exception as e2:
                    raise ValueError(f"Error al cargar el modelo: {str(e)} / {str(e2)}")
            
            # Si se cargó correctamente, dividir en partes para futuros usos
            print("Dividiendo el modelo en partes más pequeñas para futuros usos...")
            self._split_model_into_parts(model_parts_dir)
            
            print(f"Modelo cargado correctamente")
            print(f"Tipo de modelo: {type(self.model)}")
            
        except Exception as e:
            raise ValueError(f"Error al descargar o cargar el modelo: {str(e)}")

    def _split_model_into_parts(self, output_dir, max_part_size_mb=50):
        """Divide el modelo en partes más pequeñas y las guarda comprimidas"""
        if self.model is None:
            raise ValueError("No hay modelo para dividir")
        
        try:
            # Crear un archivo temporal para el modelo completo con alta compresión
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Guardar el modelo con alta compresión
            joblib.dump(self.model, temp_path, compress=('zlib', 9))
            
            # Obtener el tamaño del archivo comprimido
            file_size = os.path.getsize(temp_path)
            max_bytes = max_part_size_mb * 1024 * 1024  # Convertir MB a bytes
            
            # Calcular el número de partes necesarias
            num_parts = (file_size + max_bytes - 1) // max_bytes
            
            print(f"Dividiendo modelo de {file_size/1024/1024:.2f} MB en {num_parts} partes de {max_part_size_mb} MB...")
            
            # Leer el archivo y dividirlo en partes
            with open(temp_path, 'rb') as f:
                for i in range(num_parts):
                    part_data = f.read(max_bytes)
                    part_path = os.path.join(output_dir, f'model_part_{i:03d}.joblib')
                    with open(part_path, 'wb') as part_file:
                        part_file.write(part_data)
                    print(f"Parte {i+1}/{num_parts} guardada en {part_path}")
            
            # Eliminar el archivo temporal
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"Error al dividir el modelo: {str(e)}")
    
    def _load_model_from_parts(self, part_paths):
        """Carga el modelo desde partes divididas"""
        try:
            # Crear un archivo temporal para reconstruir el modelo
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Reconstruir el archivo del modelo
            with open(temp_path, 'wb') as f:
                for part_path in part_paths:
                    with open(part_path, 'rb') as part_file:
                        f.write(part_file.read())
            
            # Cargar el modelo reconstruido
            self.model = joblib.load(temp_path)
            
            # Eliminar el archivo temporal
            os.unlink(temp_path)
            
            print(f"Modelo cargado correctamente desde {len(part_paths)} partes")
            
        except Exception as e:
            raise ValueError(f"Error al cargar el modelo desde partes: {str(e)}")
        
    
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
        
        # Preprocesar los datos de entrada
        X = self._preprocess_input(features)
        
        # Realizar la predicción usando el pipeline completo
        # (el pipeline ya incluye el preprocesamiento y escalado)
        predictions = self.model.predict(X)
        
        # Obtener las probabilidades para cada clase
        probabilities = self.model.predict_proba(X)
        
        return predictions, probabilities

