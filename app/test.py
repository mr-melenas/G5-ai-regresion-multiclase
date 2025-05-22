import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from model import ForestCoverModel


class TestForestCoverModel(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial"""
        self.model = ForestCoverModel()
        
        # Datos de ejemplo simples
        self.sample_data = {
            'Elevation': 2596,
            'Aspect': 51,
            'Slope': 3,
            'Horizontal_Distance_To_Hydrology': 258,
            'Vertical_Distance_To_Hydrology': 0,
            'Horizontal_Distance_To_Roadways': 510,
            'Hillshade_9am': 221,
            'Hillshade_Noon': 232,
            'Hillshade_3pm': 148,
            'Horizontal_Distance_To_Fire_Points': 6279,
            'Wilderness_Area1': 1,
            'Wilderness_Area2': 0,
            'Wilderness_Area3': 0,
            'Wilderness_Area4': 0,
            'Soil_Type10': 1
        }

    def test_init(self):
        """Test de inicialización"""
        self.assertIsNone(self.model.model)
        self.assertEqual(len(self.model.numeric_features), 10)
        self.assertEqual(len(self.model.wilderness_features), 4)
        self.assertEqual(len(self.model.soil_features), 40)

    @patch('os.path.exists', return_value=False)
    def test_load_model_file_not_found(self, mock_exists):
        """Test cuando no encuentra el archivo"""
        with self.assertRaises(FileNotFoundError):
            self.model.load_model()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open')
    @patch('pickle.load')
    def test_load_model_success(self, mock_pickle, mock_open, mock_exists):
        """Test de carga exitosa"""
        mock_model = MagicMock()
        mock_pickle.return_value = mock_model
        
        self.model.load_model()
        self.assertEqual(self.model.model, mock_model)

    def test_preprocess_dict_input(self):
        """Test preprocesamiento con diccionario"""
        result = self.model._preprocess_input(self.sample_data)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[1], 54)  # 54 columnas esperadas

    def test_preprocess_dataframe_input(self):
        """Test preprocesamiento con DataFrame"""
        df = pd.DataFrame([self.sample_data])
        result = self.model._preprocess_input(df)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[1], 54)

    def test_preprocess_missing_columns(self):
        """Test con columnas faltantes"""
        incomplete_data = {'Elevation': 2596, 'Aspect': 51}
        result = self.model._preprocess_input(incomplete_data)
        
        # Debe tener todas las 54 columnas, rellenando con 0
        self.assertEqual(result.shape[1], 54)
        self.assertEqual(result['Slope'].iloc[0], 0)

    def test_predict_no_model(self):
        """Test predicción sin modelo cargado"""
        with self.assertRaises(ValueError):
            self.model.predict(self.sample_data)

    def test_predict_success(self):
        """Test predicción exitosa"""
        # Mock del modelo
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([1])
        mock_model.predict_proba.return_value = np.array([[0.1, 0.9, 0.0]])
        
        self.model.model = mock_model
        
        predictions, probabilities = self.model.predict(self.sample_data)
        
        self.assertEqual(predictions[0], 1)
        self.assertEqual(probabilities.shape[0], 1)

    def test_predict_error(self):
        """Test error en predicción"""
        mock_model = MagicMock()
        mock_model.predict.side_effect = Exception("Error")
        
        self.model.model = mock_model
        
        with self.assertRaises(ValueError):
            self.model.predict(self.sample_data)

    def test_feature_lists(self):
        """Test listas de características"""
        # Verificar tamaños
        self.assertEqual(len(self.model.all_features), 54)
        
        # Verificar contenido
        self.assertIn('Elevation', self.model.numeric_features)
        self.assertIn('Wilderness_Area1', self.model.wilderness_features)
        self.assertIn('Soil_Type1', self.model.soil_features)


if __name__ == '__main__':
    unittest.main()