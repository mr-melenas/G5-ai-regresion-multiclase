import os
import sys
import joblib
import tempfile
import argparse
import shutil

# Añadir el directorio raíz al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.model import ForestCoverModel

def compress_and_split_model(input_path, output_dir, max_part_size_mb=50, compression_level=9):
    """
    Comprime un modelo scikit-learn y lo divide en partes más pequeñas
    
    Args:
        input_path: Ruta al archivo del modelo original
        output_dir: Directorio donde se guardarán las partes
        max_part_size_mb: Tamaño máximo de cada parte en MB
        compression_level: Nivel de compresión (1-9)
    """
    print(f"Comprimiendo modelo desde {input_path}")
    
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Cargar el modelo original
    try:
        print("Cargando modelo original...")
        model = joblib.load(input_path)
        print(f"Modelo cargado correctamente: {type(model)}")
    except Exception as e:
        print(f"Error al cargar el modelo original: {e}")
        try:
            import pickle
            print("Intentando cargar con pickle...")
            with open(input_path, 'rb') as f:
                model = pickle.load(f, encoding='latin1')
            print(f"Modelo cargado correctamente con pickle: {type(model)}")
        except Exception as e2:
            print(f"Error al cargar el modelo con pickle: {e2}")
            return False
    
    # Crear un archivo temporal para el modelo comprimido
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        print(f"Guardando modelo comprimido en archivo temporal...")
        # Guardar el modelo con alta compresión
        joblib.dump(model, temp_path, compress=('zlib', compression_level))
        
        # Obtener el tamaño del archivo comprimido
        file_size = os.path.getsize(temp_path)
        max_bytes = max_part_size_mb * 1024 * 1024  # Convertir MB a bytes
        
        # Calcular el número de partes necesarias
        num_parts = (file_size + max_bytes - 1) // max_bytes
        
        print(f"Modelo comprimido: {file_size/1024/1024:.2f} MB")
        print(f"Dividiendo en {num_parts} partes de {max_part_size_mb} MB...")
        
        # Leer el archivo y dividirlo en partes
        with open(temp_path, 'rb') as f:
            for i in range(num_parts):
                part_data = f.read(max_bytes)
                part_path = os.path.join(output_dir, f'model_part_{i:03d}.joblib')
                with open(part_path, 'wb') as part_file:
                    part_file.write(part_data)
                print(f"Parte {i+1}/{num_parts} guardada en {part_path} ({len(part_data)/1024/1024:.2f} MB)")
        
        # Eliminar el archivo temporal
        os.unlink(temp_path)
        
        print(f"Modelo dividido correctamente en {num_parts} partes")
        return True
    
    except Exception as e:
        print(f"Error al comprimir y dividir el modelo: {e}")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return False

def test_model_loading_from_parts(parts_dir):
    """
    Prueba cargar el modelo desde las partes divididas
    
    Args:
        parts_dir: Directorio donde se encuentran las partes
    """
    print(f"\nProbando carga de modelo desde partes en {parts_dir}...")
    
    try:
        # Crear un modelo vacío
        model = ForestCoverModel()
        
        # Obtener la lista de partes
        import glob
        part_paths = sorted(glob.glob(os.path.join(parts_dir, 'model_part_*.joblib')))
        
        if not part_paths:
            print(f"No se encontraron partes en {parts_dir}")
            return False
        
        print(f"Encontradas {len(part_paths)} partes")
        
        # Crear un archivo temporal para reconstruir el modelo
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        # Reconstruir el archivo del modelo
        with open(temp_path, 'wb') as f:
            for part_path in part_paths:
                print(f"Añadiendo parte {part_path}...")
                with open(part_path, 'rb') as part_file:
                    f.write(part_file.read())
        
        # Cargar el modelo reconstruido
        print("Cargando modelo reconstruido...")
        model.model = joblib.load(temp_path)
        
        # Eliminar el archivo temporal
        os.unlink(temp_path)
        
        print(f"Modelo cargado correctamente desde {len(part_paths)} partes")
        print(f"Tipo de modelo: {type(model.model)}")
        
        # Realizar una predicción de prueba
        test_data = {
            'Elevation': 2500,
            'Aspect': 150,
            'Slope': 10,
            'Horizontal_Distance_To_Hydrology': 200,
            'Vertical_Distance_To_Hydrology': 50,
            'Horizontal_Distance_To_Roadways': 500,
            'Hillshade_9am': 200,
            'Hillshade_Noon': 220,
            'Hillshade_3pm': 180,
            'Horizontal_Distance_To_Fire_Points': 1000,
            'Wilderness_Area1': 1,
            'Wilderness_Area2': 0,
            'Wilderness_Area3': 0,
            'Wilderness_Area4': 0,
            'Soil_Type1': 0,
            'Soil_Type2': 1,
            'Soil_Type3': 0,
            'Soil_Type4': 0,
            'Soil_Type5': 0,
            'Soil_Type6': 0,
            'Soil_Type7': 0,
            'Soil_Type8': 0,
            'Soil_Type9': 0,
            'Soil_Type10': 0,
            'Soil_Type11': 0,
            'Soil_Type12': 0,
            'Soil_Type13': 0,
            'Soil_Type14': 0,
            'Soil_Type15': 0,
            'Soil_Type16': 0,
            'Soil_Type17': 0,
            'Soil_Type18': 0,
            'Soil_Type19': 0,
            'Soil_Type20': 0,
            'Soil_Type21': 0,
            'Soil_Type22': 0,
            'Soil_Type23': 0,
            'Soil_Type24': 0,
            'Soil_Type25': 0,
            'Soil_Type26': 0,
            'Soil_Type27': 0,
            'Soil_Type28': 0,
            'Soil_Type29': 0,
            'Soil_Type30': 0,
            'Soil_Type31': 0,
            'Soil_Type32': 0,
            'Soil_Type33': 0,
            'Soil_Type34': 0,
            'Soil_Type35': 0,
            'Soil_Type36': 0,
            'Soil_Type37': 0,
            'Soil_Type38': 0,
            'Soil_Type39': 0,
            'Soil_Type40': 0
        }
        
        predictions, probabilities = model.predict(test_data)
        print(f"Predicción de prueba exitosa: {predictions}")
        
        return True
    
    except Exception as e:
        print(f"Error al probar la carga del modelo: {e}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        return False

def upload_parts_to_cloud(parts_dir, output_urls_file):
    """
    Instrucciones para subir las partes a un servicio de almacenamiento en la nube
    
    Args:
        parts_dir: Directorio donde se encuentran las partes
        output_urls_file: Archivo donde se guardarán las URLs de las partes
    """
    print(f"\nPara subir las partes a un servicio de almacenamiento en la nube:")
    print(f"1. Sube cada archivo en {parts_dir} a Google Drive, Dropbox, GitHub, etc.")
    print(f"2. Obtén las URLs públicas de cada archivo")
    print(f"3. Guarda las URLs en el archivo {output_urls_file}")
    print(f"4. Actualiza la variable 'model_parts_urls' en app/model.py con estas URLs")
    
    # Crear archivo de ejemplo para las URLs
    with open(output_urls_file, 'w') as f:
        part_paths = sorted(os.listdir(parts_dir))
        for part_path in part_paths:
            if part_path.startswith('model_part_') and part_path.endswith('.joblib'):
                f.write(f"# {part_path}\n")
                f.write(f"# https://drive.google.com/file/d/XXXX/view?usp=drive_link\n\n")
    
    print(f"Se ha creado un archivo de ejemplo en {output_urls_file}")

def main():
    parser = argparse.ArgumentParser(description='Comprimir y dividir modelo scikit-learn')
    parser.add_argument('--input', type=str, help='Ruta al archivo del modelo original',
                        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                            'Modelos', 'modelo_pipeline.pkl'))
    parser.add_argument('--output-dir', type=str, help='Directorio donde se guardarán las partes',
                        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                            'Modelos', 'model_parts'))
    parser.add_argument('--max-part-size', type=int, help='Tamaño máximo de cada parte en MB', default=50)
    parser.add_argument('--compression-level', type=int, help='Nivel de compresión (1-9)', default=9)
    parser.add_argument('--test', action='store_true', help='Probar la carga del modelo desde las partes')
    parser.add_argument('--clean', action='store_true', help='Limpiar directorio de salida antes de comprimir')
    
    args = parser.parse_args()
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(args.input):
        print(f"Error: El archivo {args.input} no existe")
        return 1
    
    # Limpiar directorio de salida si se solicita
    if args.clean and os.path.exists(args.output_dir):
        print(f"Limpiando directorio {args.output_dir}...")
        shutil.rmtree(args.output_dir)
    
    # Comprimir y dividir el modelo
    success = compress_and_split_model(
        args.input, 
        args.output_dir, 
        args.max_part_size, 
        args.compression_level
    )
    
    if not success:
        print("Error al comprimir y dividir el modelo")
        return 1
    
    # Probar la carga del modelo si se solicita
    if args.test:
        success = test_model_loading_from_parts(args.output_dir)
        if not success:
            print("Error al probar la carga del modelo")
            return 1
    
    # Generar instrucciones para subir las partes a la nube
    urls_file = os.path.join(os.path.dirname(args.output_dir), 'model_parts_urls.txt')
    upload_parts_to_cloud(args.output_dir, urls_file)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())