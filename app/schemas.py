from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

class PredictionInput(BaseModel):
    """Esquema para la entrada de predicción individual"""
    Elevation: float = Field(..., description="Elevación en metros")
    Aspect: float = Field(..., description="Aspecto en grados azimut")
    Slope: float = Field(..., description="Pendiente en grados")
    Horizontal_Distance_To_Hydrology: float = Field(..., description="Distancia horizontal a la hidrología más cercana")
    Vertical_Distance_To_Hydrology: float = Field(..., description="Distancia vertical a la hidrología más cercana")
    Horizontal_Distance_To_Roadways: float = Field(..., description="Distancia horizontal a la carretera más cercana")
    Hillshade_9am: int = Field(..., description="Índice de sombra de colina a las 9am, de 0 a 255")
    Hillshade_Noon: int = Field(..., description="Índice de sombra de colina al mediodía, de 0 a 255")
    Hillshade_3pm: int = Field(..., description="Índice de sombra de colina a las 3pm, de 0 a 255")
    Horizontal_Distance_To_Fire_Points: float = Field(..., description="Distancia horizontal al punto de incendio más cercano")
    Wilderness_Area_1: int = Field(..., ge=0, le=1, description="Área silvestre 1 (0 o 1)")
    Wilderness_Area_2: int = Field(..., ge=0, le=1, description="Área silvestre 2 (0 o 1)")
    Wilderness_Area_3: int = Field(..., ge=0, le=1, description="Área silvestre 3 (0 o 1)")
    Wilderness_Area_4: int = Field(..., ge=0, le=1, description="Área silvestre 4 (0 o 1)")
    
    # Tipos de suelo (40 variables binarias)
    Soil_Type_1: int = Field(..., ge=0, le=1, description="Tipo de suelo 1 (0 o 1)")
    Soil_Type_2: int = Field(..., ge=0, le=1, description="Tipo de suelo 2 (0 o 1)")
    Soil_Type_3: int = Field(..., ge=0, le=1, description="Tipo de suelo 3 (0 o 1)")
    Soil_Type_4: int = Field(..., ge=0, le=1, description="Tipo de suelo 4 (0 o 1)")
    Soil_Type_5: int = Field(..., ge=0, le=1, description="Tipo de suelo 5 (0 o 1)")
    Soil_Type_6: int = Field(..., ge=0, le=1, description="Tipo de suelo 6 (0 o 1)")
    Soil_Type_7: int = Field(..., ge=0, le=1, description="Tipo de suelo 7 (0 o 1)")
    Soil_Type_8: int = Field(..., ge=0, le=1, description="Tipo de suelo 8 (0 o 1)")
    Soil_Type_9: int = Field(..., ge=0, le=1, description="Tipo de suelo 9 (0 o 1)")
    Soil_Type_10: int = Field(..., ge=0, le=1, description="Tipo de suelo 10 (0 o 1)")
    Soil_Type_11: int = Field(..., ge=0, le=1, description="Tipo de suelo 11 (0 o 1)")
    Soil_Type_12: int = Field(..., ge=0, le=1, description="Tipo de suelo 12 (0 o 1)")
    Soil_Type_13: int = Field(..., ge=0, le=1, description="Tipo de suelo 13 (0 o 1)")
    Soil_Type_14: int = Field(..., ge=0, le=1, description="Tipo de suelo 14 (0 o 1)")
    Soil_Type_15: int = Field(..., ge=0, le=1, description="Tipo de suelo 15 (0 o 1)")
    Soil_Type_16: int = Field(..., ge=0, le=1, description="Tipo de suelo 16 (0 o 1)")
    Soil_Type_17: int = Field(..., ge=0, le=1, description="Tipo de suelo 17 (0 o 1)")
    Soil_Type_18: int = Field(..., ge=0, le=1, description="Tipo de suelo 18 (0 o 1)")
    Soil_Type_19: int = Field(..., ge=0, le=1, description="Tipo de suelo 19 (0 o 1)")
    Soil_Type_20: int = Field(..., ge=0, le=1, description="Tipo de suelo 20 (0 o 1)")
    Soil_Type_21: int = Field(..., ge=0, le=1, description="Tipo de suelo 21 (0 o 1)")
    Soil_Type_22: int = Field(..., ge=0, le=1, description="Tipo de suelo 22 (0 o 1)")
    Soil_Type_23: int = Field(..., ge=0, le=1, description="Tipo de suelo 23 (0 o 1)")
    Soil_Type_24: int = Field(..., ge=0, le=1, description="Tipo de suelo 24 (0 o 1)")
    Soil_Type_25: int = Field(..., ge=0, le=1, description="Tipo de suelo 25 (0 o 1)")
    Soil_Type_26: int = Field(..., ge=0, le=1, description="Tipo de suelo 26 (0 o 1)")
    Soil_Type_27: int = Field(..., ge=0, le=1, description="Tipo de suelo 27 (0 o 1)")
    Soil_Type_28: int = Field(..., ge=0, le=1, description="Tipo de suelo 28 (0 o 1)")
    Soil_Type_29: int = Field(..., ge=0, le=1, description="Tipo de suelo 29 (0 o 1)")
    Soil_Type_30: int = Field(..., ge=0, le=1, description="Tipo de suelo 30 (0 o 1)")
    Soil_Type_31: int = Field(..., ge=0, le=1, description="Tipo de suelo 31 (0 o 1)")
    Soil_Type_32: int = Field(..., ge=0, le=1, description="Tipo de suelo 32 (0 o 1)")
    Soil_Type_33: int = Field(..., ge=0, le=1, description="Tipo de suelo 33 (0 o 1)")
    Soil_Type_34: int = Field(..., ge=0, le=1, description="Tipo de suelo 34 (0 o 1)")
    Soil_Type_35: int = Field(..., ge=0, le=1, description="Tipo de suelo 35 (0 o 1)")
    Soil_Type_36: int = Field(..., ge=0, le=1, description="Tipo de suelo 36 (0 o 1)")
    Soil_Type_37: int = Field(..., ge=0, le=1, description="Tipo de suelo 37 (0 o 1)")
    Soil_Type_38: int = Field(..., ge=0, le=1, description="Tipo de suelo 38 (0 o 1)")
    Soil_Type_39: int = Field(..., ge=0, le=1, description="Tipo de suelo 39 (0 o 1)")
    Soil_Type_40: int = Field(..., ge=0, le=1, description="Tipo de suelo 40 (0 o 1)")

    class Config:
        schema_extra = {
            "example": {
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
            }
        }

class BatchPredictionInput(BaseModel):
    """Esquema para la entrada de predicción por lotes"""
    inputs: List[PredictionInput]

class PredictionOutput(BaseModel):
    """Esquema para la salida de predicción individual"""
    cover_type: int
    cover_type_name: str
    probabilities: Dict[str, float]

class BatchPredictionOutput(BaseModel):
    """Esquema para la salida de predicción por lotes"""
    predictions: List[PredictionOutput]

class ModelInfo(BaseModel):
    """Esquema para la información del modelo"""
    name: str
    version: str
    description: str
    cover_type_mapping: Dict[int, str]
    features: List[str]
    accuracy: Optional[float] = None

class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    error: str
    detail: Optional[str] = None