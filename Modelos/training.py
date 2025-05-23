import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score
import joblib

# Cargar el dataset
df = pd.read_csv("covtype.csv")

columnas_cuantitativas = [
    'Elevation', 'Aspect', 'Slope',
    'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
    'Horizontal_Distance_To_Roadways',
    'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
    'Horizontal_Distance_To_Fire_Points'
]

columnas_wilderness = [f'Wilderness_Area{i}' for i in range(1, 5)]

columnas_soil = [f'Soil_Type{i}' for i in range(1, 41)]

columna_target = ['Cover_Type']

todas_columnas = columnas_cuantitativas + columnas_wilderness + columnas_soil + columna_target

df.columns = todas_columnas

#Conviene meter un df.describe para comprobar que la variable objetivo tiene 7 tipos

# Separar X e y
X = df.drop('Cover_Type', axis=1)
y = df['Cover_Type']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Aplicar SMOTE para balancear clases en el conjunto de entrenamiento
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# -----------------------------
# PREPROCESADOR
# -----------------------------

# Escalador solo para columnas cuantitativas
preprocessor = ColumnTransformer(
    transformers=[
        ('scaler', StandardScaler(), columnas_cuantitativas)
    ],
    remainder='passthrough'  # Deja las demás columnas sin tocar (como las binarias)
)


# Definir el modelo base
rf_model = RandomForestClassifier(random_state=42)

# Pipeline para grid search
pipe_cv = Pipeline([
    ('preprocessing', preprocessor),
    ('model', rf_model)
])

# -----------------------------
# ENTRENAMIENTO FINAL
# -----------------------------

# Pipeline final con mejores hiperparámetros
final_pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42
    ))
])

# Entrenar pipeline final
final_pipeline.fit(X_train_resampled, y_train_resampled)

# Evaluar sobre conjunto de prueba
y_pred = final_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Precisión en el conjunto de prueba: {accuracy:.4f}")

# -----------------------------
# GUARDAR PIPELINE
# -----------------------------

joblib.dump(final_pipeline, 'modelo_pipeline.pkl')
print("✅ Pipeline completo guardado como 'modelo_pipeline.pkl'")