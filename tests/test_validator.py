import pytest
import pandas as pd
import numpy as np
from app.validator import detect_columns, validate_schema, handle_missing_values, normalize_formats

def test_detect_columns():
    df = pd.DataFrame({
        'Ngày': ['2026-04-01'],
        'Doanh thu': [1000000],
        'Sản phẩm': ['A']
    })
    df_mapped = detect_columns(df)
    assert 'date' in df_mapped.columns
    assert 'revenue' in df_mapped.columns
    assert 'product' in df_mapped.columns

def test_validate_schema():
    df_valid = pd.DataFrame({'date': [], 'revenue': []})
    is_valid, _ = validate_schema(df_valid)
    assert is_valid == True
    df_invalid = pd.DataFrame({'date': []})
    is_valid, _ = validate_schema(df_invalid)
    assert is_valid == False

def test_handle_missing_values():
    df = pd.DataFrame({
        'date': ['2026-04-01', np.nan],
        'revenue': [100, 200],
        'product': [np.nan, 'B']
    })
    df_cleaned = handle_missing_values(df)
    assert len(df_cleaned) == 1 
    assert df_cleaned.iloc[0]['product'] == 'Unknown'

def test_normalize_formats():
    df = pd.DataFrame({
        'date': ['2026-04-01'],
        'revenue': ['1,000,000']
    })
    df_norm = normalize_formats(df)
    assert pd.api.types.is_datetime64_any_dtype(df_norm['date'])
    assert df_norm.iloc[0]['revenue'] == 1000000.0
