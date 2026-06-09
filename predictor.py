"""
predictor_v1_Grupo_1 — TP3 GPU Reservation Cancellation Predictor

Usage:
    from predictor import predictor_v1_Grupo_1
    predictions = predictor_v1_Grupo_1(X_new_df)
"""

import os
import pickle
import numpy as np
import pandas as pd

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PIPELINE_PATH = os.path.join(_BASE_DIR, "data", "processed", "final_pipeline.pkl")
_FEATURE_COLS_PATH = os.path.join(_BASE_DIR, "data", "processed", "final_feature_cols.txt")

_pipeline = None
_feature_cols = None

# Columnas derivadas/redundantes eliminadas en 01_limpieza (+ target si viene)
COLS_TO_DROP = ["total_gpu_hours", "total_processes", "request_month", "canceled_job"]


def _load_artifacts():
    global _pipeline, _feature_cols
    if _pipeline is None:
        with open(_PIPELINE_PATH, "rb") as f:
            _pipeline = pickle.load(f)
    if _feature_cols is None:
        with open(_FEATURE_COLS_PATH) as f:
            _feature_cols = f.read().splitlines()


def predictor_v1_Grupo_1(X_new: pd.DataFrame) -> np.ndarray:
    """
    Predice si una reserva GPU será cancelada antes de su ejecución.

    Args:
        X_new: DataFrame con las mismas columnas que gpu_resource_reservations.csv
               (sin 'canceled_job' — puede incluirla, se ignora automáticamente)

    Returns:
        np.ndarray de int64: 0 = no cancelado, 1 = cancelado
    """
    _load_artifacts()

    df = X_new.copy()

    # 1. Drop columnas derivadas / target si están presentes
    df = df.drop(columns=[c for c in COLS_TO_DROP if c in df.columns])

    # 2. Encoding cíclico de request_week (igual que en 01_limpieza)
    df["week_sin"] = np.sin(2 * np.pi * df["request_week"] / 53)
    df["week_cos"] = np.cos(2 * np.pi * df["request_week"] / 53)

    # 3. OHE robusto: drop_first=False + reindex equivale al encoding de train para
    #    cualquier fila y evita mis-encoding cuando faltan categorías (p.ej. un solo subgrupo)
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    df = pd.get_dummies(df, columns=cat_cols, drop_first=False, dtype=int)

    # 4. Alinear columnas al espacio de features del modelo entrenado
    df = df.reindex(columns=_feature_cols, fill_value=0)

    return _pipeline.predict(df).astype(int)
