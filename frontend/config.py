import os
from typing import Dict, List

# Configuración de la API
API_BASE_URL = os.getenv("http://localhost:8000", "https://forestvision.onrender.com:8000")
API_TIMEOUT = 30  # segundos

# Configuración del Dashboard
DASH_HOST = os.getenv("DASH_HOST", "0.0.0.0")
DASH_PORT = int(os.getenv("DASH_PORT", "8050"))
DASH_DEBUG = os.getenv("DASH_DEBUG", "True").lower() == "true"

# Mapeo de tipos de cobertura forestal
COVER_TYPE_MAPPING: Dict[int, str] = {
    1: "Spruce/Fir",
    2: "Lodgepole Pine", 
    3: "Ponderosa Pine",
    4: "Cottonwood/Willow",
    5: "Aspen",
    6: "Douglas-fir",
    7: "Krummholz"
}

# Colores para cada tipo de cobertura
COVER_TYPE_COLORS: Dict[str, str] = {
    "Spruce/Fir": "#2E8B57",
    "Lodgepole Pine": "#228B22",
    "Ponderosa Pine": "#32CD32", 
    "Cottonwood/Willow": "#9ACD32",
    "Aspen": "#ADFF2F",
    "Douglas-fir": "#008000",
    "Krummholz": "#006400"
}

# Variables del modelo organizadas por categorías
NUMERIC_FEATURES: List[str] = [
    'Elevation', 'Aspect', 'Slope', 
    'Horizontal_Distance_To_Hydrology',
    'Vertical_Distance_To_Hydrology', 
    'Horizontal_Distance_To_Roadways',
    'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
    'Horizontal_Distance_To_Fire_Points'
]

WILDERNESS_FEATURES: List[str] = [
    f'Wilderness_Area{i}' for i in range(1, 5)
]

SOIL_FEATURES: List[str] = [
    f'Soil_Type{i}' for i in range(1, 41)
]

ALL_FEATURES: List[str] = NUMERIC_FEATURES + WILDERNESS_FEATURES + SOIL_FEATURES

# Configuración de formularios
FORM_DEFAULTS: Dict[str, any] = {
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
    "wilderness_areas": ["wilderness_1"],
    "soil_type": 29
}

# Descripciones de las variables para tooltips
VARIABLE_DESCRIPTIONS: Dict[str, str] = {
    "Elevation": "Elevación en metros sobre el nivel del mar",
    "Aspect": "Orientación de la pendiente en grados azimut (0-360)",
    "Slope": "Inclinación de la pendiente en grados (0-90)",
    "Horizontal_Distance_To_Hydrology": "Distancia horizontal al cuerpo de agua más cercano (metros)",
    "Vertical_Distance_To_Hydrology": "Distancia vertical al cuerpo de agua más cercano (metros)",
    "Horizontal_Distance_To_Roadways": "Distancia horizontal a la carretera más cercana (metros)",
    "Hillshade_9am": "Índice de sombra de colina a las 9:00 AM (0-255)",
    "Hillshade_Noon": "Índice de sombra de colina al mediodía (0-255)",
    "Hillshade_3pm": "Índice de sombra de colina a las 3:00 PM (0-255)",
    "Horizontal_Distance_To_Fire_Points": "Distancia horizontal al punto de ignición más cercano (metros)"
}

# Configuración de gráficos
CHART_CONFIG: Dict[str, any] = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "pan2d", "lasso2d", "select2d", "autoScale2d",
        "hoverClosestCartesian", "hoverCompareCartesian"
    ],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "forest_cover_prediction",
        "height": 500,
        "width": 700,
        "scale": 1
    }
}

# Configuración de tablas
TABLE_STYLE_CELL: Dict[str, str] = {
    'textAlign': 'left',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '14px',
    'padding': '10px'
}

TABLE_STYLE_HEADER: Dict[str, str] = {
    'backgroundColor': 'rgb(230, 230, 230)',
    'fontWeight': 'bold',
    'textAlign': 'center'
}

TABLE_STYLE_DATA: Dict[str, str] = {
    'backgroundColor': 'rgb(248, 248, 248)',
    'border': '1px solid rgb(230, 230, 230)'
}

# Mensajes de la aplicación
MESSAGES: Dict[str, str] = {
    "welcome": "Bienvenido al Dashboard de Predicción de Cobertura Forestal",
    "prediction_success": "Predicción realizada exitosamente",
    "prediction_error": "Error al realizar la predicción",
    "file_upload_success": "Archivo cargado correctamente",
    "file_upload_error": "Error al cargar el archivo",
    "api_connection_error": "Error de conexión con la API",
    "invalid_format": "Formato de archivo inválido"
}

# Límites de validación
VALIDATION_LIMITS: Dict[str, Dict[str, float]] = {
    "Elevation": {"min": 1000, "max": 4500},
    "Aspect": {"min": 0, "max": 360},
    "Slope": {"min": 0, "max": 90},
    "Horizontal_Distance_To_Hydrology": {"min": 0, "max": 10000},
    "Vertical_Distance_To_Hydrology": {"min": -500, "max": 500},
    "Horizontal_Distance_To_Roadways": {"min": 0, "max": 10000},
    "Hillshade_9am": {"min": 0, "max": 255},
    "Hillshade_Noon": {"min": 0, "max": 255},
    "Hillshade_3pm": {"min": 0, "max": 255},
    "Horizontal_Distance_To_Fire_Points": {"min": 0, "max": 15000}
}