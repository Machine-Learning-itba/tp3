"""
predictor_v1_Grupo_X — TP3 GPU Reservation Cancellation Predictor

Usage:
    from predictor import predictor_v1_Grupo_X
    predictions = predictor_v1_Grupo_X(X_new_df)
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

COLS_TO_DROP = ["total_gpu_hours", "total_processes", "canceled_job"]


def _load_artifacts():
    global _pipeline, _feature_cols
    if _pipeline is None:
        with open(_PIPELINE_PATH, "rb") as f:
            _pipeline = pickle.load(f)
    if _feature_cols is None:
        with open(_FEATURE_COLS_PATH) as f:
            _feature_cols = f.read().splitlines()


def predictor_v1_Grupo_X(X_new: pd.DataFrame) -> np.ndarray:
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

    # Drop columnas derivadas / target si están presentes
    df = df.drop(columns=[c for c in COLS_TO_DROP if c in df.columns])

    # OHE: mismas transformaciones que notebook 01_limpieza
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=int)

    # Alinear columnas al espacio de features del modelo entrenado
    for col in _feature_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[_feature_cols]

    return _pipeline.predict(df).astype(int)
