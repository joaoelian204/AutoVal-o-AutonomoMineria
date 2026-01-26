import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    GradientBoostingRegressor,
)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler


class CarPricePredictor:
    """
    Clase para manejar el modelo de predicción de precios de vehículos usados.
    Implementa el pipeline completo de ML: preprocesamiento, entrenamiento y predicción.
    """

    def __init__(self, model_path='models/car_price_model.pkl',
                 scaler_path='models/scaler.pkl'):
        self.model = None
        self.scaler = None
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.feature_names = None
        self.metrics = {}

        # Intentar cargar modelo existente
        self._load_model()

    def _load_model(self):
        """Cargar modelo y scaler guardados si existen"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("✓ Modelo y scaler cargados exitosamente")
        except Exception as e:
            print(f"No se pudo cargar el modelo existente: {e}")

    def _save_model(self):
        """Guardar modelo y scaler entrenados"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.scaler_path), exist_ok=True)

            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            print("✓ Modelo y scaler guardados exitosamente")
        except Exception as e:
            print(f"Error al guardar el modelo: {e}")

    def preprocess_data(self, df, is_training=True):
        """
        Preprocesar los datos: limpiar, escalar y codificar variables categóricas

        Args:
            df: DataFrame con los datos
            is_training: Si es True, ajusta el scaler. Si es False, solo transforma.

        Returns:
            DataFrame procesado
        """
        df = df.copy()

        # Obtener el año actual para calcular la edad
        current_year = pd.Timestamp.now().year

        # 1. Ingeniería de características
        # Crear nueva característica: Edad del vehículo
        df['Vehicle_Age'] = current_year - df['Year']

        # Crear característica: Kilometraje por año (uso promedio)
        df['Kms_Per_Year'] = df['Kms_Driven'] / (df['Vehicle_Age'] + 1)

        # Crear característica: Ratio de depreciación esperada
        df['Age_Squared'] = df['Vehicle_Age'] ** 2

        # 1. Eliminar duplicados (solo en entrenamiento)
        if is_training:
            df.drop_duplicates(inplace=True)

            # 2. Eliminar outliers usando IQR (solo en entrenamiento)
            # Para Selling_Price
            if 'Selling_Price' in df.columns:
                Q1 = df['Selling_Price'].quantile(0.05)
                Q3 = df['Selling_Price'].quantile(0.95)
                df = df[(df['Selling_Price'] >= Q1) &
                        (df['Selling_Price'] <= Q3)]

            # Eliminar vehículos con kilometraje extremo
            df = df[df['Kms_Driven'] < 500000]

        # 3. Estandarización de variables numéricas
        cols_to_scale = ['Present_Price', 'Kms_Driven',
                         'Vehicle_Age', 'Kms_Per_Year', 'Age_Squared']

        if is_training:
            self.scaler = StandardScaler()
            df[cols_to_scale] = self.scaler.fit_transform(df[cols_to_scale])
        else:
            if self.scaler is None:
                raise ValueError(
                    "El scaler no ha sido ajustado. Entrena el modelo primero.")
            df[cols_to_scale] = self.scaler.transform(df[cols_to_scale])

        # 4. One-Hot Encoding para variables categóricas
        categorical_cols = ['Fuel_Type', 'Seller_Type', 'Transmission']
        df_encoded = pd.get_dummies(
            df, columns=categorical_cols, drop_first=True)

        # Eliminar columna Year ya que tenemos Vehicle_Age
        if 'Year' in df_encoded.columns:
            df_encoded = df_encoded.drop('Year', axis=1)

        return df_encoded

    def train_model(self, data_path):
        """
        Entrenar el modelo con datos desde un archivo CSV

        Args:
            data_path: Ruta al archivo CSV con los datos de entrenamiento

        Returns:
            Dictionary con las métricas de evaluación
        """
        print(f"📚 Cargando datos desde {data_path}...")
        df = pd.read_csv(data_path)

        print(f"✓ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")

        # Preprocesar datos
        print("🔧 Preprocesando datos...")
        df_processed = self.preprocess_data(df, is_training=True)

        # Separar características (X) y variable objetivo (y)
        # Eliminar 'Car_Name' si existe y 'Selling_Price' que es el target
        cols_to_drop = ['Selling_Price']
        if 'Car_Name' in df_processed.columns:
            cols_to_drop.append('Car_Name')

        X = df_processed.drop(cols_to_drop, axis=1)
        y = df_processed['Selling_Price']

        # Guardar nombres de características
        self.feature_names = list(X.columns)

        print(f"✓ Características: {X.shape[1]}")
        print(f"✓ Muestras después de limpieza: {X.shape[0]}")

        # Dividir en entrenamiento y prueba (80/20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"✓ Conjunto de entrenamiento: {X_train.shape[0]} muestras")
        print(f"✓ Conjunto de prueba: {X_test.shape[0]} muestras")

        # Usar Gradient Boosting con búsqueda de hiperparámetros expandida
        print("🔍 Buscando mejores hiperparámetros con Gradient Boosting...")
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7, 10],
            'learning_rate': [0.01, 0.05, 0.1],
            'min_samples_split': [2, 5],
            'subsample': [0.8, 1.0]
        }

        gb_grid = GridSearchCV(
            estimator=GradientBoostingRegressor(random_state=42),
            param_grid=param_grid,
            cv=5,
            scoring='r2',
            n_jobs=-1,
            verbose=1
        )

        # Entrenar modelo
        print("🚀 Entrenando modelo Gradient Boosting...")
        gb_grid.fit(X_train, y_train)

        # Guardar el mejor modelo
        self.model = gb_grid.best_estimator_

        print(f"✓ Mejores hiperparámetros: {gb_grid.best_params_}")

        # Evaluar modelo
        print("📊 Evaluando modelo...")
        y_pred = self.model.predict(X_test)

        # Calcular métricas
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        self.metrics = {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'r2_score': float(r2),
            'best_params': gb_grid.best_params_
        }

        print("\n" + "="*50)
        print("📈 RESULTADOS DEL ENTRENAMIENTO")
        print("="*50)
        print(f"MAE (Error Absoluto Medio):     {mae:.4f}")
        print(f"RMSE (Raíz del Error Cuadrático): {rmse:.4f}")
        print(f"R² Score (Bondad de ajuste):    {r2:.4f}")
        print("="*50 + "\n")

        # Guardar modelo
        self._save_model()

        return self.metrics

    def predict(self, input_data):
        """
        Predecir el precio de un vehículo

        Args:
            input_data: Dictionary con las características del vehículo

        Returns:
            Precio predicho (float)
        """
        if self.model is None:
            print("Error: El modelo no está entrenado")
            return None

        # Crear DataFrame con los datos de entrada
        df = pd.DataFrame([input_data])

        # Preprocesar datos
        df_processed = self.preprocess_data(df, is_training=False)

        # Asegurar que tenemos todas las características necesarias
        # (el one-hot encoding puede crear diferentes columnas)
        for col in self.feature_names:
            if col not in df_processed.columns:
                df_processed[col] = 0

        # Ordenar columnas para que coincidan con el entrenamiento
        df_processed = df_processed[self.feature_names]

        # Realizar predicción
        prediction = self.model.predict(df_processed)[0]

        return prediction

    def is_trained(self):
        """Verificar si el modelo está entrenado"""
        return self.model is not None

    def get_model_confidence(self):
        """Obtener el nivel de confianza del modelo (R² score)"""
        if 'r2_score' in self.metrics:
            return self.metrics['r2_score']
        return 0.0

    def get_model_info(self):
        """Obtener información sobre el modelo entrenado"""
        if not self.is_trained():
            return None

        return {
            'algorithm': 'Gradient Boosting Regressor',
            'n_features': len(self.feature_names) if self.feature_names else 0,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'trained': True
        }

    def get_feature_importance(self):
        """Obtener la importancia de cada característica"""
        if not self.is_trained() or self.feature_names is None:
            return None

        importances = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)

        return feature_importance.to_dict('records')
