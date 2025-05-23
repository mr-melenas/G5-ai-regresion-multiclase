# ForestVision - API de Clasificación de Cobertura Forestal

Esta API permite predecir el tipo de cobertura forestal basado en variables cartográficas utilizando un modelo pre-entrenado.

## Clonar el Repositorio 
git clone "aca luego de copiarlo lo pegas y ya esta "

## Importamos librerias 
pandas,numpy,matplotlib,sklearn 
"destacar que esas son ejemplos de las principales ya que hay multiples ramas y las librerias varian de acuerdo a la rama en la que estes, tambien por eso instala el requirements"


## Requisitos

```
pip install -r requirements.txt
```

## Analisis exploratorio de datos 
se realizo un EDA al dataset de [https://archive.ics.uci.edu/dataset/31/covertype] de aqui sale la base de este proyecto y luego nos concentramos en los modelos de predicción en el cual vimos varios desde Logistic regression hasta Ramdon forest que es el que utilizamos 

## Estructura del Proyecto

- `main.py`: Aplicación FastAPI principal
- `app/`: Módulo de la aplicación
  - `schemas.py`: Esquemas de datos para la API
  - `model.py`: Clase para cargar y utilizar el modelo
- `Modelos/`: Directorio donde se almacena el modelo pre-entrenado
- `test_api.py`: Script para probar la API

## Ejecución

Para iniciar la API, ejecute:

```
uvicorn main:app --reload
```

La API estará disponible en http://localhost:8000

## Endpoints

### GET /

Ruta principal de la API.

### GET /info

Obtiene información sobre el modelo de clasificación.

### POST /predict

Realiza una predicción para un conjunto de características.

**Ejemplo de solicitud:**

```json
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
  ...
  "Soil_Type_40": 0
}
```

### POST /predict/batch

Realiza predicciones para múltiples conjuntos de características.

**Ejemplo de solicitud:**

```json
{
  "inputs": [
    {
      "Elevation": 2596,
      ...
    },
    {
      "Elevation": 2590,
      ...
    }
  ]
}
```

## Pruebas

Para probar la API, ejecute:

```
python test_api.py
```

Este script creará un modelo de prueba si no existe y realizará solicitudes a todos los endpoints de la API.

## Testing
implementaciones de testing desde test unitarios hasta test de integración 
para correr el test unitario es 
``python -m unittest test.py -v´´
o  para mayor facilidad simplemente ``python test.py´´

para correr el test de integración el comando es 
pytest test_database.py -v

## Implementación de docker 
docker compose up --build
docker run [nombre de la imagen]

## Diagrama de arquitecturas 

## Autores 
https://www.linkedin.com/in/andreina-suescum/

https://www.linkedin.com/in/alejandro-rajado-martín/

https://www.linkedin.com/in/orlando-david-71417411b/

https://www.linkedin.com/in/max-beltran/


