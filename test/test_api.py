import requests
import json
import os
import sys
import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Añadir el directorio raíz del proyecto al path para poder importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import save_data

# Verificar que el modelo pre-entrenado existe
def create_test_model():
    print("Verificando modelo pre-entrenado...")
    # Ruta al modelo pre-entrenado en la carpeta principal del proyecto
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Modelos', 'modelo_pipeline.pkl')
    
    # Verificar si el modelo existe
    if os.path.exists(model_path):
        print(f"✅ El modelo pre-entrenado existe en: {model_path}")
    else:
        print(f"❌ ERROR: No se encontró el modelo pre-entrenado en: {model_path}")
        print("Por favor, asegúrate de que el modelo existe en la ruta correcta antes de ejecutar las pruebas.")
        exit(1)  # Salir con error si no se encuentra el modelo

# Crear el modelo de prueba
create_test_model()

# URL base de la API
BASE_URL = "http://127.0.0.1:8000"

# Probar la ruta de información
def test_info():
    print("\nProbando ruta /info...")
    response = requests.get(f"{BASE_URL}/info")
    if response.status_code == 200:
        print("✅ Éxito: Ruta /info funciona correctamente")
        #print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Error - test_info() : {response.status_code} - {response.text}")

# Probar la ruta de predicción individual
def test_predict():
    print("\nProbando ruta /predict...")
    # Datos de ejemplo para la predicción
    data = {
        "Elevation": 2596,
        "Aspect": 51,
        "Slope": 3,
        "Horizontal_Distance_To_Hydrology": 258,
        "Vertical_Distance_To_Hydrology": 0,
        "Horizontal_Distance_To_Roadways": 510,
        "Hillshade_9am": 221,
        "Hillshade_Noon": 232,
        "Hillshade_3pm": 148,
        "Horizontal_Distance_To_Fire_Points": 6279,
        "Wilderness_Area1": 1,
        "Wilderness_Area2": 0,
        "Wilderness_Area3": 0,
        "Wilderness_Area4": 0,
        "Soil_Type1": 0,
        "Soil_Type2": 0,
        "Soil_Type3": 0,
        "Soil_Type4": 0,
        "Soil_Type5": 0,
        "Soil_Type6": 0,
        "Soil_Type7": 0,
        "Soil_Type8": 0,
        "Soil_Type9": 0,
        "Soil_Type10": 0,
        "Soil_Type11": 0,
        "Soil_Type12": 0,
        "Soil_Type13": 0,
        "Soil_Type14": 0,
        "Soil_Type15": 0,
        "Soil_Type16": 0,
        "Soil_Type17": 0,
        "Soil_Type18": 0,
        "Soil_Type19": 0,
        "Soil_Type20": 0,
        "Soil_Type21": 0,
        "Soil_Type22": 0,
        "Soil_Type23": 0,
        "Soil_Type24": 0,
        "Soil_Type25": 0,
        "Soil_Type26": 0,
        "Soil_Type27": 0,
        "Soil_Type28": 0,
        "Soil_Type29": 1,
        "Soil_Type30": 0,
        "Soil_Type31": 0,
        "Soil_Type32": 0,
        "Soil_Type33": 0,
        "Soil_Type34": 0,
        "Soil_Type35": 0,
        "Soil_Type36": 0,
        "Soil_Type37": 0,
        "Soil_Type38": 0,
        "Soil_Type39": 0,
        "Soil_Type40": 0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=data, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            print("✅ Éxito: Ruta /predict funciona correctamente")
            print(f"Respuesta: {json.dumps(response.json(), indent=2)}")

            print(f"cover_type: {response_json['cover_type']}")
            #print(f"Tipo de cobertura: {response.json()['cover_type']}")
            save_data(data, int(response_json['cover_type']))
            # Añadir el cover_type al diccionario `data`
            #data["label"] = response_json["cover_type"]
            
            print(data)
        else:
            error_detail = ""
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            print(f"❌ Error - test_predict(): {response.status_code} - {error_detail}")
            print("Detalles de la solicitud:")
            print(f"URL: {BASE_URL}/predict")
            print(f"Datos enviados: {json.dumps(data, indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en test_predict(): {str(e)}")

# Probar la ruta de predicción por lotes
def test_batch_predict():
    print("\nProbando ruta /predict/batch...")
    # Datos de ejemplo para la predicción por lotes
    data = {
        "inputs": [
            {
                "Elevation": 2596,
                "Aspect": 51,
                "Slope": 3,
                "Horizontal_Distance_To_Hydrology": 258,
                "Vertical_Distance_To_Hydrology": 0,
                "Horizontal_Distance_To_Roadways": 510,
                "Hillshade_9am": 221,
                "Hillshade_Noon": 232,
                "Hillshade_3pm": 148,
                "Horizontal_Distance_To_Fire_Points": 6279,
                "Wilderness_Area_1": 1,
                "Wilderness_Area_2": 0,
                "Wilderness_Area_3": 0,
                "Wilderness_Area_4": 0,
                "Soil_Type_1": 0,
                "Soil_Type_2": 0,
                "Soil_Type_3": 0,
                "Soil_Type_4": 0,
                "Soil_Type_5": 0,
                "Soil_Type_6": 0,
                "Soil_Type_7": 0,
                "Soil_Type_8": 0,
                "Soil_Type_9": 0,
                "Soil_Type_10": 0,
                "Soil_Type_11": 0,
                "Soil_Type_12": 0,
                "Soil_Type_13": 0,
                "Soil_Type_14": 0,
                "Soil_Type_15": 0,
                "Soil_Type_16": 0,
                "Soil_Type_17": 0,
                "Soil_Type_18": 0,
                "Soil_Type_19": 0,
                "Soil_Type_20": 0,
                "Soil_Type_21": 0,
                "Soil_Type_22": 0,
                "Soil_Type_23": 0,
                "Soil_Type_24": 0,
                "Soil_Type_25": 0,
                "Soil_Type_26": 0,
                "Soil_Type_27": 0,
                "Soil_Type_28": 0,
                "Soil_Type_29": 1,
                "Soil_Type_30": 0,
                "Soil_Type_31": 0,
                "Soil_Type_32": 0,
                "Soil_Type_33": 0,
                "Soil_Type_34": 0,
                "Soil_Type_35": 0,
                "Soil_Type_36": 0,
                "Soil_Type_37": 0,
                "Soil_Type_38": 0,
                "Soil_Type_39": 0,
                "Soil_Type_40": 0
            },
            {
                "Elevation": 2590,
                "Aspect": 56,
                "Slope": 2,
                "Horizontal_Distance_To_Hydrology": 212,
                "Vertical_Distance_To_Hydrology": -6,
                "Horizontal_Distance_To_Roadways": 390,
                "Hillshade_9am": 220,
                "Hillshade_Noon": 235,
                "Hillshade_3pm": 151,
                "Horizontal_Distance_To_Fire_Points": 6225,
                "Wilderness_Area_1": 1,
                "Wilderness_Area_2": 0,
                "Wilderness_Area_3": 0,
                "Wilderness_Area_4": 0,
                "Soil_Type_1": 0,
                "Soil_Type_2": 0,
                "Soil_Type_3": 0,
                "Soil_Type_4": 0,
                "Soil_Type_5": 0,
                "Soil_Type_6": 0,
                "Soil_Type_7": 0,
                "Soil_Type_8": 0,
                "Soil_Type_9": 0,
                "Soil_Type_10": 0,
                "Soil_Type_11": 0,
                "Soil_Type_12": 0,
                "Soil_Type_13": 0,
                "Soil_Type_14": 0,
                "Soil_Type_15": 0,
                "Soil_Type_16": 0,
                "Soil_Type_17": 0,
                "Soil_Type_18": 0,
                "Soil_Type_19": 0,
                "Soil_Type_20": 0,
                "Soil_Type_21": 0,
                "Soil_Type_22": 0,
                "Soil_Type_23": 0,
                "Soil_Type_24": 0,
                "Soil_Type_25": 0,
                "Soil_Type_26": 0,
                "Soil_Type_27": 0,
                "Soil_Type_28": 0,
                "Soil_Type_29": 1,
                "Soil_Type_30": 0,
                "Soil_Type_31": 0,
                "Soil_Type_32": 0,
                "Soil_Type_33": 0,
                "Soil_Type_34": 0,
                "Soil_Type_35": 0,
                "Soil_Type_36": 0,
                "Soil_Type_37": 0,
                "Soil_Type_38": 0,
                "Soil_Type_39": 0,
                "Soil_Type_40": 0
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/predict/batch", json=data)
    if response.status_code == 200:
        print("✅ Éxito: Ruta /predict/batch funciona correctamente")
        print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Error - test_batch_predict : {response.status_code} - {response.text}")

# Ejecutar las pruebas
if __name__ == "__main__":
    print("=== Iniciando pruebas de la API ===")
    print("Nota: Asegúrate de que la API esté en ejecución en http://localhost:8000")
    print("Para iniciar la API, ejecuta: uvicorn main:app --reload")
    
    # Ejecutar las pruebas
    test_info()
    test_predict()
    #test_batch_predict()
    
    print("\n=== Pruebas completadas ===")