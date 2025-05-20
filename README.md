readme
# API de Clasificación de Cobertura Forestal

Este proyecto implementa una API REST utilizando FastAPI para realizar predicciones de tipos de cobertura forestal basadas en variables cartográficas. El modelo de clasificación multiclase está entrenado con el dataset Covertype.

## Descripción del Dataset

El dataset Forest Covertype contiene información cartográfica para predecir el tipo de cobertura forestal. Incluye 581,012 instancias con 54 atributos, representando 7 tipos de cobertura forestal:

1. Spruce/Fir
2. Lodgepole Pine
3. Ponderosa Pine
4. Cottonwood/Willow
5. Aspen
6. Douglas-fir
7. Krummholz

Las variables incluyen elevación, aspecto, pendiente, distancias a hidrología y carreteras, índices de sombra, y tipos de suelo y áreas silvestres (variables binarias).

## Estructura del Proyecto

```
.
├── app/                    # Directorio principal de la aplicación
│   ├── __init__.py         # Inicialización del paquete
│   ├── main.py             # Archivo principal de la API FastAPI
│   ├── model.py            # Implementación del modelo de clasificación
│   └── schemas.py          # Esquemas Pydantic para validación de datos
├── Data/                   # Datos de entrenamiento
│   ├── covtype.data        # Dataset de cobertura forestal
│   └── covtype.info        # Información sobre el dataset
├── models/                 # Directorio para guardar modelos entrenados (creado automáticamente)
├── requirements.txt        # Dependencias del proyecto
├── run.py                  # Script para ejecutar la API
└── README.md               # Este archivo
```

## Instalación

1. Clonar el repositorio o descargar los archivos

2. Crear un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
```

3. Activar el entorno virtual:

- En Windows:
```bash
venv\Scripts\activate
```

- En macOS/Linux:
```bash
source venv/bin/activate
```

4. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la API

Para iniciar la API, ejecute:

```bash
python run.py
```

La API estará disponible en `http://localhost:8000`.

### Documentación de la API

Una vez que la API esté en ejecución, puede acceder a la documentación interactiva en:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints Disponibles

- `GET /`: Página principal de la API
- `GET /info`: Obtener información sobre el modelo
- `POST /train`: Iniciar el entrenamiento del modelo en segundo plano
- `POST /predict`: Realizar una predicción individual
- `POST /predict/batch`: Realizar predicciones por lotes

### Ejemplos de Uso

#### Realizar una predicción individual

```python
import requests
import json

# URL de la API
url = "http://localhost:8000/predict"

# Datos de ejemplo
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
    "Wilderness_Area_1": 1,
    "Wilderness_Area_2": 0,
    "Wilderness_Area_3": 0,
    "Wilderness_Area_4": 0,
    "Soil_Type_1": 0,
    "Soil_Type_2": 0,
    # ... (resto de tipos de suelo)
    "Soil_Type_40": 0
}

# Realizar la solicitud POST
response = requests.post(url, json=data)

# Imprimir la respuesta
print(json.dumps(response.json(), indent=4))
```

#### Realizar predicciones por lotes

```python
import requests
import json

# URL de la API
url = "http://localhost:8000/predict/batch"

# Datos de ejemplo para lotes
data = {
    "inputs": [
        {
            "Elevation": 2596,
            "Aspect": 51,
            # ... (resto de características)
        },
        {
            "Elevation": 2590,
            "Aspect": 56,
            # ... (resto de características)
        }
    ]
}

# Realizar la solicitud POST
response = requests.post(url, json=data)

# Imprimir la respuesta
print(json.dumps(response.json(), indent=4))
```

## Entrenamiento del Modelo

El modelo se entrenará automáticamente la primera vez que se realice una predicción si no existe un modelo pre-entrenado. También puede iniciar el entrenamiento manualmente:

```python
import requests

# URL para entrenar el modelo
url = "http://localhost:8000/train"

# Iniciar el entrenamiento
response = requests.post(url)
print(response.json())
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web de alto rendimiento para crear APIs con Python
- **Scikit-learn**: Biblioteca de aprendizaje automático para el modelo de clasificación
- **Pandas**: Manipulación y análisis de datos
- **Pydantic**: Validación de datos y configuración
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI

## Notas

- El entrenamiento del modelo puede tardar varios minutos dependiendo del hardware.
- Para mejorar el rendimiento en producción, considere usar un modelo pre-entrenado.
- La API está configurada para permitir solicitudes CORS desde cualquier origen para facilitar el desarrollo.