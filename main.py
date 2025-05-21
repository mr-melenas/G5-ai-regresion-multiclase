from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import os
from typing import List, Dict

from app.schemas import (
    PredictionInput, 
    BatchPredictionInput, 
    PredictionOutput, 
    BatchPredictionOutput, 
    ModelInfo
)
from app.model import ForestCoverModel

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Clasificación de Cobertura Forestal",
    description="API para predecir el tipo de cobertura forestal basado en variables cartográficas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador de excepciones global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_msg = f"Error no manejado: {str(exc)}"
    print(f"ERROR GLOBAL: {error_msg}")
    return JSONResponse(
        status_code=500,
        content={"error": error_msg}
    )

# Mapeo de tipos de cobertura forestal
COVER_TYPE_MAPPING = {
    1: "Spruce/Fir",
    2: "Lodgepole Pine",
    3: "Ponderosa Pine",
    4: "Cottonwood/Willow",
    5: "Aspen",
    6: "Douglas-fir",
    7: "Krummholz"
}

# Variable global para el modelo
forest_cover_model = ForestCoverModel()

# Cargar el modelo al iniciar la aplicación
try:
    forest_cover_model.load_model()
    print("Modelo cargado correctamente al iniciar la aplicación")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

# Función para obtener el modelo
def get_model():
    return forest_cover_model

# Ruta principal
@app.get("/")
async def root():
    return {"mensaje": "API de Clasificación de Cobertura Forestal. Accede a /docs para la documentación."}



# Ruta para obtener información del modelo
@app.get("/info", response_model=ModelInfo)
async def get_model_info():
    """Obtiene información sobre el modelo de clasificación"""
    model = get_model()
    return ModelInfo(
        name="Forest Cover Type Classifier",
        version="1.0.0",
        description="Modelo de clasificación para predecir el tipo de cobertura forestal basado en variables cartográficas",
        cover_type_mapping=COVER_TYPE_MAPPING,
        features=model.all_features
    )

# Ruta para realizar una predicción individual
@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput, model: ForestCoverModel = Depends(get_model)):
    """Realiza una predicción para un conjunto de características"""
    try:
        # Convertir la entrada a un diccionario
        features = input_data.dict()
        print(f"Procesando predicción con características: {features}")
        
        # Verificar que el modelo esté cargado
        if model.model is None:
            print("Error: El modelo no está cargado correctamente")
            raise HTTPException(status_code=500, detail="El modelo no está cargado correctamente. Por favor, reinicie la aplicación.")
        
        # Realizar la predicción
        prediction, probabilities = model.predict(features)
        
        # Obtener la clase predicha (el primer elemento ya que solo hay una muestra)
        predicted_class = int(prediction[0])
        
        # Verificar que la clase predicha esté en el mapeo
        if predicted_class not in COVER_TYPE_MAPPING:
            print(f"Advertencia: La clase predicha {predicted_class} no está en el mapeo. Usando clase 1 por defecto.")
            predicted_class = 1
            
        # Obtener las probabilidades para cada clase
        prob_dict = {COVER_TYPE_MAPPING[i+1]: float(probabilities[0][i]) for i in range(len(probabilities[0]))}
        
        print(f"Predicción exitosa: clase {predicted_class} ({COVER_TYPE_MAPPING[predicted_class]})")
        
        # Crear la respuesta
        return PredictionOutput(
            cover_type=predicted_class,
            cover_type_name=COVER_TYPE_MAPPING[predicted_class],
            probabilities=prob_dict
        )
    except ValueError as e:
        error_msg = f"Error de valor en la predicción: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except KeyError as e:
        error_msg = f"Error de clave en la predicción: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"Error inesperado en la predicción: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)



# Ruta para realizar predicciones por lotes
@app.post("/predict/batch", response_model=BatchPredictionOutput)
async def predict_batch(input_data: BatchPredictionInput, model: ForestCoverModel = Depends(get_model)):
    """Realiza predicciones para múltiples conjuntos de características"""
    try:
        # Verificar que el modelo esté cargado
        if model.model is None:
            print("Error: El modelo no está cargado correctamente")
            raise HTTPException(status_code=500, detail="El modelo no está cargado correctamente. Por favor, reinicie la aplicación.")
            
        # Convertir la entrada a una lista de diccionarios
        features_list = [item.dict() for item in input_data.inputs]
        print(f"Procesando predicción por lotes con {len(features_list)} muestras")
        
        # Crear un DataFrame con todas las muestras
        features_df = pd.DataFrame(features_list)
        
        # Realizar las predicciones
        predictions, probabilities = model.predict(features_df)
        
        # Crear la lista de resultados
        results = []
        for i, pred in enumerate(predictions):
            predicted_class = int(pred)
            
            # Verificar que la clase predicha esté en el mapeo
            if predicted_class not in COVER_TYPE_MAPPING:
                print(f"Advertencia: La clase predicha {predicted_class} no está en el mapeo. Usando clase 1 por defecto.")
                predicted_class = 1
                
            prob_dict = {COVER_TYPE_MAPPING[j+1]: float(probabilities[i][j]) for j in range(len(probabilities[i]))}
            
            results.append(PredictionOutput(
                cover_type=predicted_class,
                cover_type_name=COVER_TYPE_MAPPING[predicted_class],
                probabilities=prob_dict
            ))
        
        print(f"Predicción por lotes exitosa: {len(results)} resultados generados")
        
        # Crear la respuesta
        return BatchPredictionOutput(predictions=results)
    except ValueError as e:
        error_msg = f"Error de valor en la predicción por lotes: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except KeyError as e:
        error_msg = f"Error de clave en la predicción por lotes: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"Error inesperado en la predicción por lotes: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

# Manejador de excepciones personalizado
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor", "detail": str(exc)}
    )