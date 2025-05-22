import dash
from dash import dcc, html, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from datetime import datetime
import numpy as np

# Configuración de la API
API_BASE_URL = "http://localhost:8000"  # Cambiar por tu URL de producción

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

# Colores para cada tipo de cobertura
COVER_TYPE_COLORS = {
    "Spruce/Fir": "#2E8B57",
    "Lodgepole Pine": "#228B22",
    "Ponderosa Pine": "#32CD32", 
    "Cottonwood/Willow": "#9ACD32",
    "Aspen": "#ADFF2F",
    "Douglas-fir": "#008000",
    "Krummholz": "#006400"
}

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Forest Cover Prediction Dashboard"

# Layout principal
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🌲 Forest Cover Prediction Dashboard", 
                   className="text-center mb-4 text-success"),
            html.P("Predice el tipo de cobertura forestal basado en variables cartográficas",
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # Tabs principales
    dbc.Tabs([
        # Tab 1: Predicción Individual
        dbc.Tab(label="Predicción Individual", tab_id="prediction-tab"),
        # Tab 2: Predicción por Lotes
        dbc.Tab(label="Predicción por Lotes", tab_id="batch-tab"),
        # Tab 3: Visualización de Resultados
        dbc.Tab(label="Análisis de Resultados", tab_id="analysis-tab"),
        # Tab 4: Información del Modelo
        dbc.Tab(label="Información del Modelo", tab_id="info-tab")
    ], id="main-tabs", active_tab="prediction-tab"),
    
    html.Div(id="tab-content", className="mt-4")
], fluid=True)

# Callback para el contenido de las tabs
@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "prediction-tab":
        return create_prediction_tab()
    elif active_tab == "batch-tab":
        return create_batch_tab()
    elif active_tab == "analysis-tab":
        return create_analysis_tab()
    elif active_tab == "info-tab":
        return create_info_tab()
    return html.Div("Selecciona una pestaña")

def create_prediction_tab():
    return dbc.Row([
        # Columna izquierda: Formulario de entrada
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Variables de Entrada"),
                dbc.CardBody([
                    # Variables geográficas principales
                    html.H5("Variables Topográficas", className="text-primary"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Elevación (m)"),
                            dbc.Input(id="elevation", type="number", value=2596, step=1),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Aspecto (grados)"),
                            dbc.Input(id="aspect", type="number", value=51, step=1, min=0, max=360),
                        ], width=6),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Pendiente (grados)"),
                            dbc.Input(id="slope", type="number", value=3, step=0.1, min=0, max=90),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Dist. Horizontal a Hidrología"),
                            dbc.Input(id="hydrology-h", type="number", value=258, step=1),
                        ], width=6),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Dist. Vertical a Hidrología"),
                            dbc.Input(id="hydrology-v", type="number", value=0, step=1),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Dist. Horizontal a Carreteras"),
                            dbc.Input(id="roadways", type="number", value=510, step=1),
                        ], width=6),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Dist. Horizontal a Puntos de Fuego"),
                            dbc.Input(id="fire-points", type="number", value=6279, step=1),
                        ], width=12),
                    ], className="mb-4"),
                    
                    # Variables de sombra
                    html.H5("Índices de Sombra (0-255)", className="text-primary"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Sombra 9am"),
                            dbc.Input(id="hillshade-9am", type="number", value=221, min=0, max=255),
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Sombra Mediodía"),
                            dbc.Input(id="hillshade-noon", type="number", value=232, min=0, max=255),
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Sombra 3pm"),
                            dbc.Input(id="hillshade-3pm", type="number", value=148, min=0, max=255),
                        ], width=4),
                    ], className="mb-4"),
                    
                    # Áreas silvestres
                    html.H5("Áreas Silvestres", className="text-primary"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Checklist(
                                options=[
                                    {"label": "Área Silvestre 1", "value": "wilderness_1"},
                                    {"label": "Área Silvestre 2", "value": "wilderness_2"},
                                    {"label": "Área Silvestre 3", "value": "wilderness_3"},
                                    {"label": "Área Silvestre 4", "value": "wilderness_4"},
                                ],
                                value=["wilderness_1"],
                                id="wilderness-areas",
                                inline=True
                            )
                        ])
                    ], className="mb-4"),
                    
                    # Tipos de suelo (selector simplificado)
                    html.H5("Tipo de Suelo", className="text-primary"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Select(
                                id="soil-type-select",
                                options=[{"label": f"Tipo de Suelo {i}", "value": i} for i in range(1, 41)],
                                value=29
                            )
                        ])
                    ], className="mb-4"),
                    
                    # Botón de predicción
                    dbc.Button("Realizar Predicción", id="predict-btn", color="success", size="lg", className="w-100")
                ])
            ])
        ], width=6),
        
        # Columna derecha: Resultados
        dbc.Col([
            # Resultado de la predicción
            dbc.Card([
                dbc.CardHeader("🎯 Resultado de la Predicción"),
                dbc.CardBody(id="prediction-result")
            ], className="mb-4"),
            
            # Gráfico de probabilidades
            dbc.Card([
                dbc.CardHeader("📈 Probabilidades por Tipo de Cobertura"),
                dbc.CardBody([
                    dcc.Graph(id="probability-chart")
                ])
            ])
        ], width=6)
    ])

def create_batch_tab():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📁 Predicción por Lotes"),
                dbc.CardBody([
                    html.P("Sube un archivo CSV con múltiples muestras para realizar predicciones en lote."),
                    dcc.Upload(
                        id='upload-data',
                        children=dbc.Button([
                            html.I(className="fa fa-upload me-2"),
                            "Subir archivo CSV"
                        ], color="primary", size="lg"),
                        style={'textAlign': 'center'},
                        multiple=False
                    ),
                    html.Div(id="upload-status", className="mt-3"),
                    html.Div(id="batch-results", className="mt-4")
                ])
            ])
        ])
    ])

def create_analysis_tab():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Análisis de Predicciones"),
                dbc.CardBody([
                    html.P("Aquí se mostrarán estadísticas y visualizaciones de las predicciones realizadas."),
                    dcc.Graph(id="analysis-chart"),
                    html.Div(id="analysis-stats")
                ])
            ])
        ])
    ])

def create_info_tab():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("ℹ️ Información del Modelo"),
                dbc.CardBody(id="model-info")
            ])
        ])
    ])

# Callback para la predicción individual
@app.callback(
    [Output("prediction-result", "children"),
     Output("probability-chart", "figure")],
    Input("predict-btn", "n_clicks"),
    [State("elevation", "value"),
     State("aspect", "value"),
     State("slope", "value"),
     State("hydrology-h", "value"),
     State("hydrology-v", "value"),
     State("roadways", "value"),
     State("fire-points", "value"),
     State("hillshade-9am", "value"),
     State("hillshade-noon", "value"),
     State("hillshade-3pm", "value"),
     State("wilderness-areas", "value"),
     State("soil-type-select", "value")]
)
def make_prediction(n_clicks, elevation, aspect, slope, hydrology_h, hydrology_v, 
                   roadways, fire_points, hillshade_9am, hillshade_noon, hillshade_3pm,
                   wilderness_areas, soil_type):
    
    if not n_clicks:
        return "Presiona el botón para realizar una predicción", {}
    
    try:
        # Preparar los datos de entrada
        wilderness_dict = {f"Wilderness_Area{i}": 0 for i in range(1, 5)}
        for area in (wilderness_areas or []):
            area_num = int(area.split('_')[1])
            wilderness_dict[f"Wilderness_Area{area_num}"] = 1
        
        soil_dict = {f"Soil_Type{i}": 0 for i in range(1, 41)}
        if soil_type:
            soil_dict[f"Soil_Type{soil_type}"] = 1
        
        # Crear el payload para la API
        payload = {
            "Elevation": elevation,
            "Aspect": aspect,
            "Slope": slope,
            "Horizontal_Distance_To_Hydrology": hydrology_h,
            "Vertical_Distance_To_Hydrology": hydrology_v,
            "Horizontal_Distance_To_Roadways": roadways,
            "Hillshade_9am": hillshade_9am,
            "Hillshade_Noon": hillshade_noon,
            "Hillshade_3pm": hillshade_3pm,
            "Horizontal_Distance_To_Fire_Points": fire_points,
            **wilderness_dict,
            **soil_dict
        }
        

        response = requests.post(f"{API_BASE_URL}/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            # Crear el resultado visual
            prediction_card = dbc.Alert([
                html.H4(f"🌲 {result['cover_type_name']}", className="alert-heading"),
                html.P(f"Tipo de Cobertura: {result['cover_type']}"),
                html.P(f"Confianza: {max(result['probabilities'].values()):.2%}")
            ], color="success")
            
            # Crear el gráfico de probabilidades
            prob_data = result['probabilities']
            fig = px.bar(
                x=list(prob_data.keys()),
                y=list(prob_data.values()),
                title="Probabilidades por Tipo de Cobertura",
                color=list(prob_data.keys()),
                color_discrete_map=COVER_TYPE_COLORS
            )
            fig.update_layout(
                showlegend=False, 
                xaxis_title="Tipo de Cobertura", 
                yaxis_title="Probabilidad",
                yaxis_tickformat=".2%"
            )
            
            return prediction_card, fig
            
        else:
            error_msg = f"Error en la API: {response.status_code}"
            return dbc.Alert(error_msg, color="danger"), {}
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return dbc.Alert(error_msg, color="danger"), {}

# Callback para cargar información del modelo
@app.callback(
    Output("model-info", "children"),
    Input("main-tabs", "active_tab")
)
def load_model_info(active_tab):
    if active_tab != "info-tab":
        return ""
    
    try:
        response = requests.get(f"{API_BASE_URL}/info")
        if response.status_code == 200:
            info = response.json()
            
            features_table = dash_table.DataTable(
                data=[{"Feature": f} for f in info['features']],
                columns=[{"name": "Características del Modelo", "id": "Feature"}],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                page_size=10
            )
            
            cover_types_cards = []
            for ct_id, ct_name in info['cover_type_mapping'].items():
                cover_types_cards.append(
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6(f"Tipo {ct_id}", className="card-title"),
                                html.P(ct_name, className="card-text")
                            ], style={"backgroundColor": COVER_TYPE_COLORS.get(ct_name, "#f8f9fa")})
                        ])
                    ], width=3, className="mb-2")
                )
            
            return [
                html.H5("Información General"),
                html.P(f"Nombre: {info['name']}"),
                html.P(f"Versión: {info['version']}"),
                html.P(f"Descripción: {info['description']}"),
                html.Hr(),
                html.H5("Tipos de Cobertura Forestal"),
                dbc.Row(cover_types_cards),
                html.Hr(),
                html.H5("Características del Modelo"),
                features_table
            ]
        else:
            return dbc.Alert("Error al cargar información del modelo", color="warning")
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)