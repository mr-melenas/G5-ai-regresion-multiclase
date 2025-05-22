import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# Configuración de la API
API_BASE_URL = "http://localhost:8000"  # Cambiar por tu URL de producción

# Funciones para manejo de datos y visualizaciones

def validate_csv_format(df):
    """
    Valida que el CSV tenga el formato correcto para las predicciones
    """
    required_columns = [
        'Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
        'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
        'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
        'Horizontal_Distance_To_Fire_Points'
    ]
    
    # Columnas de áreas silvestres
    wilderness_cols = [f'Wilderness_Area{i}' for i in range(1, 5)]
    
    # Columnas de tipos de suelo
    soil_cols = [f'Soil_Type{i}' for i in range(1, 41)]
    
    all_required = required_columns + wilderness_cols + soil_cols
    
    missing_cols = [col for col in all_required if col not in df.columns]
    
    return len(missing_cols) == 0, missing_cols

def process_batch_predictions(df):
    """
    Procesa un DataFrame para realizar predicciones por lotes
    """
    try:
        # Validar formato
        is_valid, missing_cols = validate_csv_format(df)
        if not is_valid:
            return None, f"Faltan columnas: {', '.join(missing_cols)}"
        
        # Convertir DataFrame a lista de diccionarios
        records = df.to_dict('records')
        
        # Preparar payload para la API
        payload = {"inputs": records}
        
        # Realizar petición a la API
        response = requests.post(f"{API_BASE_URL}/predict/batch", json=payload)
        
        if response.status_code == 200:
            results = response.json()
            return results['predictions'], None
        else:
            return None, f"Error en la API: {response.status_code} - {response.text}"
            
    except Exception as e:
        return None, f"Error procesando datos: {str(e)}"

def create_batch_results_table(predictions):
    """
    Crea una tabla con los resultados de las predicciones por lotes
    """
    if not predictions:
        return pd.DataFrame()
    
    results_data = []
    for i, pred in enumerate(predictions):
        results_data.append({
            'Muestra': i + 1,
            'Tipo_Cobertura': pred['cover_type'],
            'Nombre_Cobertura': pred['cover_type_name'],
            'Confianza': max(pred['probabilities'].values())
        })
    
    return pd.DataFrame(results_data)

def create_prediction_distribution_chart(predictions):
    """
    Crea un gráfico de distribución de las predicciones por lotes
    """
    if not predictions:
        return {}
    
    # Contar frecuencia de cada tipo de cobertura
    cover_counts = {}
    for pred in predictions:
        cover_name = pred['cover_type_name']
        cover_counts[cover_name] = cover_counts.get(cover_name, 0) + 1
    
    # Crear gráfico de barras
    fig = px.bar(
        x=list(cover_counts.keys()),
        y=list(cover_counts.values()),
        title="Distribución de Tipos de Cobertura Predichos",
        labels={'x': 'Tipo de Cobertura', 'y': 'Frecuencia'}
    )
    
    return fig

def create_confidence_distribution_chart(predictions):
    """
    Crea un gráfico de distribución de confianza de las predicciones
    """
    if not predictions:
        return {}
    
    confidences = [max(pred['probabilities'].values()) for pred in predictions]
    
    fig.update_layout(
        title="Distribución de Confianza en las Predicciones",
        xaxis_title="Confianza",
        yaxis_title="Frecuencia",
        xaxis_tickformat=".2%"
    )
    
    return fig

def create_feature_importance_chart():
    """
    Crea un gráfico conceptual de importancia de características
    (esto sería mejor si tuvieras acceso a las importancias reales del modelo)
    """
    # Importancias simuladas - en producción estas vendrían del modelo
    features = [
        'Elevation', 'Horizontal_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
        'Hillshade_Noon', 'Hillshade_9am', 'Aspect', 'Slope', 'Vertical_Distance_To_Hydrology',
        'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points'
    ]
    
    # Valores simulados - reemplazar con datos reales
    importances = [0.15, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04]
    
    fig = px.bar(
        x=importances,
        y=features,
        orientation='h',
        title="Importancia de Características (Conceptual)",
        labels={'x': 'Importancia Relativa', 'y': 'Características'}
    )
    
    return fig

def generate_sample_data():
    """
    Genera datos de muestra para demostración
    """
    np.random.seed(42)
    
    samples = []
    for i in range(10):
        # Generar valores aleatorios pero realistas
        sample = {
            'Elevation': np.random.randint(1500, 3500),
            'Aspect': np.random.randint(0, 360),
            'Slope': np.random.randint(0, 60),
            'Horizontal_Distance_To_Hydrology': np.random.randint(0, 1000),
            'Vertical_Distance_To_Hydrology': np.random.randint(-200, 200),
            'Horizontal_Distance_To_Roadways': np.random.randint(0, 5000),
            'Hillshade_9am': np.random.randint(100, 255),
            'Hillshade_Noon': np.random.randint(100, 255),
            'Hillshade_3pm': np.random.randint(100, 255),
            'Horizontal_Distance_To_Fire_Points': np.random.randint(0, 8000),
        }
        
        # Añadir áreas silvestres (solo una activa por muestra)
        for j in range(1, 5):
            sample[f'Wilderness_Area{j}'] = 1 if j == (i % 4 + 1) else 0
        
        # Añadir tipos de suelo (solo uno activo por muestra)
        for j in range(1, 41):
            sample[f'Soil_Type{j}'] = 1 if j == (i % 40 + 1) else 0
        
        samples.append(sample)
    
    return pd.DataFrame(samples)

def create_correlation_heatmap(df):
    """
    Crea un heatmap de correlación para las variables numéricas
    """
    numeric_cols = [
        'Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
        'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
        'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
        'Horizontal_Distance_To_Fire_Points'
    ]
    
    if not all(col in df.columns for col in numeric_cols):
        return {}
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        title="Matriz de Correlación de Variables Numéricas",
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    
    return fig

def get_prediction_statistics(predictions):
    """
    Calcula estadísticas de las predicciones
    """
    if not predictions:
        return {}
    
    stats = {
        'total_predictions': len(predictions),
        'unique_types': len(set(pred['cover_type_name'] for pred in predictions)),
        'avg_confidence': np.mean([max(pred['probabilities'].values()) for pred in predictions]),
        'min_confidence': min(max(pred['probabilities'].values()) for pred in predictions),
        'max_confidence': max(max(pred['probabilities'].values()) for pred in predictions)
    }
    
    # Contar por tipo de cobertura
    type_counts = {}
    for pred in predictions:
        cover_name = pred['cover_type_name']
        type_counts[cover_name] = type_counts.get(cover_name, 0) + 1
    
    stats['type_distribution'] = type_counts
    stats['most_common_type'] = max(type_counts, key=type_counts.get)
    
    return stats

def export_results_to_csv(predictions, filename="predictions_results.csv"):
    """
    Exporta los resultados a un archivo CSV
    """
    if not predictions:
        return None
    
    results_df = create_batch_results_table(predictions)
    results_df.to_csv(filename, index=False)
    return filename