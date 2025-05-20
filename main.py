from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import os
import sys
from typing import List, Dict, Any

from app.schemas import (
    PredictionInput, 
    BatchPredictionInput, 
    PredictionOutput, 
    BatchPredictionOutput, 
    ModelInfo, 
    ErrorResponse
)
from app.model import ForestCoverModel, train_and_save_model

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
forest_cover_model = None

# Función para obtener el modelo
def get_model():
    global forest_cover_model
    if forest_cover_model is None:
        forest_cover_model = ForestCoverModel()
        try:
            # Intentar cargar el modelo pre-entrenado
            forest_cover_model.load_model()
        except FileNotFoundError:
            # Si no existe, entrenar un nuevo modelo
            print("No se encontró un modelo pre-entrenado. Entrenando un nuevo modelo...")
            train_and_save_model()
            forest_cover_model.load_model()
    return forest_cover_model

# Ruta para entrenar el modelo en segundo plano
@app.post("/train", response_model=Dict[str, str])
async def train_model(background_tasks: BackgroundTasks):
    """Entrena el modelo en segundo plano"""
    background_tasks.add_task(train_and_save_model)
    return {"message": "El entrenamiento del modelo ha comenzado en segundo plano"}

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
        
        # Realizar la predicción
        prediction, probabilities = model.predict(features)
        
        # Obtener la clase predicha (el primer elemento ya que solo hay una muestra)
        predicted_class = int(prediction[0])
        
        # Obtener las probabilidades para cada clase
        prob_dict = {COVER_TYPE_MAPPING[i+1]: float(probabilities[0][i]) for i in range(len(probabilities[0]))}
        
        # Crear la respuesta
        return PredictionOutput(
            cover_type=predicted_class,
            cover_type_name=COVER_TYPE_MAPPING[predicted_class],
            probabilities=prob_dict
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para realizar predicciones por lotes
@app.post("/predict/batch", response_model=BatchPredictionOutput)
async def predict_batch(input_data: BatchPredictionInput, model: ForestCoverModel = Depends(get_model)):
    """Realiza predicciones para múltiples conjuntos de características"""
    try:
        # Convertir la entrada a una lista de diccionarios
        features_list = [item.dict() for item in input_data.inputs]
        
        # Crear un DataFrame con todas las muestras
        features_df = pd.DataFrame(features_list)
        
        # Realizar las predicciones
        predictions, probabilities = model.predict(features_df)
        
        # Crear la lista de resultados
        results = []
        for i, pred in enumerate(predictions):
            predicted_class = int(pred)
            prob_dict = {COVER_TYPE_MAPPING[j+1]: float(probabilities[i][j]) for j in range(len(probabilities[i]))}
            
            results.append(PredictionOutput(
                cover_type=predicted_class,
                cover_type_name=COVER_TYPE_MAPPING[predicted_class],
                probabilities=prob_dict
            ))
        
        # Crear la respuesta
        return BatchPredictionOutput(predictions=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Manejador de excepciones personalizado
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=str(exc.detail)).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="Error interno del servidor", detail=str(exc)).dict()
    )

# Ruta raíz
@app.get("/")
async def root():
    """Ruta principal de la API"""
    return {
        "message": "API de Clasificación de Cobertura Forestal",
        "docs": "/docs",
        "info": "/info"
    }