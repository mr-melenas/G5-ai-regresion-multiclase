import pytest
import sys
import os
from unittest.mock import patch, MagicMock

def find_database_file():
    """Busca database.py en directorios cercanos"""
    search_paths = [
        os.path.dirname(os.path.abspath(__file__)),  # Directorio actual
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Directorio padre
        os.getcwd(),  # Directorio de trabajo actual
    ]
    
    for path in search_paths:
        database_path = os.path.join(path, 'database.py')
        if os.path.exists(database_path):
            if path not in sys.path:
                sys.path.insert(0, path)
            print(f"✓ Encontrado database.py en: {path}")
            return path
    
    raise FileNotFoundError("No se encontró database.py en ningún directorio")

# Buscar y configurar el path
try:
    database_dir = find_database_file()
    from database import save, save_data
    print("✓ database.py importado correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nEjecuta este comando para ver dónde están tus archivos:")
    print("find . -name 'database.py' -type f")
    print("o en Windows:")
    print("dir database.py /s")
    sys.exit(1)

class TestDatabase:
    
    @patch('database.supabase')
    def test_save_works(self, mock_supabase):
        """Test básico de save()"""
        mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()
        
        data = {"Elevation": 2500, "label": 1}
        result = save(data)
        
        assert result is not None
        mock_supabase.table.assert_called_with("forrest")

    @patch('database.supabase')
    def test_save_handles_errors(self, mock_supabase):
        """Test que save maneja errores"""
        mock_supabase.table.return_value.insert.return_value.execute.side_effect = Exception("Error")
        
        result = save({"test": "data"})
        assert result is None

    @patch('database.save')
    @patch('database.datetime')
    def test_save_data_works(self, mock_datetime, mock_save):
        """Test básico de save_data()"""
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T00:00:00"
        mock_save.return_value = MagicMock()
        
        features = {
            "Elevation": "2500", "Aspect": "180", "Slope": "15",
            "Horizontal_Distance_To_Hydrology": "100", "Vertical_Distance_To_Hydrology": "50",
            "Horizontal_Distance_To_Roadways": "200", "Hillshade_9am": "220",
            "Hillshade_Noon": "250", "Hillshade_3pm": "180",
            "Horizontal_Distance_To_Fire_Points": "300",
            "Wilderness_Area1": "1", "Wilderness_Area2": "0", 
            "Wilderness_Area3": "0", "Wilderness_Area4": "0",
            **{f"Soil_Type{i}": "0" for i in range(1, 41)}
        }
        features["Soil_Type1"] = "1"
        
        save_data(features, 2)
        
        mock_save.assert_called_once()
        args = mock_save.call_args[0][0]
        assert args["label"] == 2
        assert args["Elevation"] == 2500

    @patch('database.save')
    def test_save_data_invalid_input(self, mock_save):
        """Test con input inválido"""
        features = {"Elevation": "invalid"}
        result = save_data(features, 1)
        
        assert result is None
        mock_save.assert_not_called()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])