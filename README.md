# ForestVision - API de Clasificación de Cobertura Forestal

Esta API permite predecir el tipo de cobertura forestal basado en variables cartográficas utilizando un modelo pre-entrenado.

## Clonar el Repositorio 
git clone "aca luego de copiarlo lo pegas y ya esta "

## Importamos librerias 
"destacar que esas son ejemplos de las principales ya que hay multiples ramas y las librerias varian de acuerdo a la rama en la que estes, tambien por eso instala el requirements"

---
## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/-Jupyter-FF3C00?logo=jupyter&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white)
![Render](https://img.shields.io/badge/-Render-46B7C8?logo=render&logoColor=white)
![Gradio](https://img.shields.io/badge/-Gradio-FFB400?logo=python&logoColor=black)
![Supabase](https://img.shields.io/badge/-Supabase-3ECF8E?logo=supabase&logoColor=white)


## Dependencias

![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/-Scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![Uvicorn](https://img.shields.io/badge/-Uvicorn-7A2A8B?logo=uvicorn&logoColor=white)

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

[https://cdn.discordapp.com/attachments/1372149881963024462/1375400197156376627/diagrama_er.png?ex=68318cc0&is=68303b40&hm=6d02c5c535b977f2576efc6b5740e29ceb7dd74e854334307d9ca6b64ca9f672&]

## Autores 
 Andreina Suescum https://www.linkedin.com/in/andreina-suescum/

Alejandro Rajado Martin https://www.linkedin.com/in/alejandro-rajado-martín/

Orlando Alcalá https://www.linkedin.com/in/orlando-david-71417411b/

Max Beltran https://www.linkedin.com/in/max-beltran/

## Documentación 
https://deepwiki.com/mr-melenas/G5-ai-regresion-multiclase aca el enlace de la documentación 
nota: puede durar un poco a cargar la pagina entre 15-25 min


