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
    Wilderness_Area1: int = Field(..., ge=0, le=1, description="Área silvestre 1 (0 o 1)")
    Wilderness_Area2: int = Field(..., ge=0, le=1, description="Área silvestre 2 (0 o 1)")
    Wilderness_Area3: int = Field(..., ge=0, le=1, description="Área silvestre 3 (0 o 1)")
    Wilderness_Area4: int = Field(..., ge=0, le=1, description="Área silvestre 4 (0 o 1)")
    
    # Tipos de suelo (40 variables binarias)
    Soil_Type1: int = Field(..., ge=0, le=1, description="Tipo de suelo 1 (0 o 1)")
    Soil_Type2: int = Field(..., ge=0, le=1, description="Tipo de suelo 2 (0 o 1)")
    Soil_Type3: int = Field(..., ge=0, le=1, description="Tipo de suelo 3 (0 o 1)")
    Soil_Type4: int = Field(..., ge=0, le=1, description="Tipo de suelo 4 (0 o 1)")
    Soil_Type5: int = Field(..., ge=0, le=1, description="Tipo de suelo 5 (0 o 1)")
    Soil_Type6: int = Field(..., ge=0, le=1, description="Tipo de suelo 6 (0 o 1)")
    Soil_Type7: int = Field(..., ge=0, le=1, description="Tipo de suelo 7 (0 o 1)")
    Soil_Type8: int = Field(..., ge=0, le=1, description="Tipo de suelo 8 (0 o 1)")
    Soil_Type9: int = Field(..., ge=0, le=1, description="Tipo de suelo 9 (0 o 1)")
    Soil_Type10: int = Field(..., ge=0, le=1, description="Tipo de suelo 10 (0 o 1)")
    Soil_Type11: int = Field(..., ge=0, le=1, description="Tipo de suelo 11 (0 o 1)")
    Soil_Type12: int = Field(..., ge=0, le=1, description="Tipo de suelo 12 (0 o 1)")
    Soil_Type13: int = Field(..., ge=0, le=1, description="Tipo de suelo 13 (0 o 1)")
    Soil_Type14: int = Field(..., ge=0, le=1, description="Tipo de suelo 14 (0 o 1)")
    Soil_Type15: int = Field(..., ge=0, le=1, description="Tipo de suelo 15 (0 o 1)")
    Soil_Type16: int = Field(..., ge=0, le=1, description="Tipo de suelo 16 (0 o 1)")
    Soil_Type17: int = Field(..., ge=0, le=1, description="Tipo de suelo 17 (0 o 1)")
    Soil_Type18: int = Field(..., ge=0, le=1, description="Tipo de suelo 18 (0 o 1)")
    Soil_Type19: int = Field(..., ge=0, le=1, description="Tipo de suelo 19 (0 o 1)")
    Soil_Type20: int = Field(..., ge=0, le=1, description="Tipo de suelo 20 (0 o 1)")
    Soil_Type21: int = Field(..., ge=0, le=1, description="Tipo de suelo 21 (0 o 1)")
    Soil_Type22: int = Field(..., ge=0, le=1, description="Tipo de suelo 22 (0 o 1)")
    Soil_Type23: int = Field(..., ge=0, le=1, description="Tipo de suelo 23 (0 o 1)")
    Soil_Type24: int = Field(..., ge=0, le=1, description="Tipo de suelo 24 (0 o 1)")
    Soil_Type25: int = Field(..., ge=0, le=1, description="Tipo de suelo 25 (0 o 1)")
    Soil_Type26: int = Field(..., ge=0, le=1, description="Tipo de suelo 26 (0 o 1)")
    Soil_Type27: int = Field(..., ge=0, le=1, description="Tipo de suelo 27 (0 o 1)")
    Soil_Type28: int = Field(..., ge=0, le=1, description="Tipo de suelo 28 (0 o 1)")
    Soil_Type29: int = Field(..., ge=0, le=1, description="Tipo de suelo 29 (0 o 1)")
    Soil_Type30: int = Field(..., ge=0, le=1, description="Tipo de suelo 30 (0 o 1)")
    Soil_Type31: int = Field(..., ge=0, le=1, description="Tipo de suelo 31 (0 o 1)")
    Soil_Type32: int = Field(..., ge=0, le=1, description="Tipo de suelo 32 (0 o 1)")
    Soil_Type33: int = Field(..., ge=0, le=1, description="Tipo de suelo 33 (0 o 1)")
    Soil_Type34: int = Field(..., ge=0, le=1, description="Tipo de suelo 34 (0 o 1)")
    Soil_Type35: int = Field(..., ge=0, le=1, description="Tipo de suelo 35 (0 o 1)")
    Soil_Type36: int = Field(..., ge=0, le=1, description="Tipo de suelo 36 (0 o 1)")
    Soil_Type37: int = Field(..., ge=0, le=1, description="Tipo de suelo 37 (0 o 1)")
    Soil_Type38: int = Field(..., ge=0, le=1, description="Tipo de suelo 38 (0 o 1)")
    Soil_Type39: int = Field(..., ge=0, le=1, description="Tipo de suelo 39 (0 o 1)")
    Soil_Type40: int = Field(..., ge=0, le=1, description="Tipo de suelo 40 (0 o 1)")

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

