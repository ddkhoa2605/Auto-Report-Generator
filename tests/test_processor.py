import pytest
import pandas as pd
import numpy as np
from app.processor import (
    compute_daily_revenue, 
    compute_top_products, 
    compute_revenue_growth, 
    compute_avg_order_value, 
    detect_anomalies
)

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'date': pd.to_datetime(['2026-04-01', '2026-04-01', '2026-04-02', '2026-04-03', '2026-04-04']),
        'revenue': [100, 200, 300, 400, 2000],
        'product': ['A', 'B', 'A', 'C', 'A'],
        'orders': [1, 2, 1, 1, 5]
    })

def test_compute_daily_revenue(sample_df):
    res = compute_daily_revenue(sample_df)
    assert len(res) == 4
    assert res.iloc[0]['revenue'] == 300

def test_compute_top_products(sample_df):
    res = compute_top_products(sample_df, n=2)
    assert res.iloc[0]['product'] == 'A'
    assert res.iloc[0]['revenue'] == 2400

def test_compute_revenue_growth(sample_df):
    growth = compute_revenue_growth(sample_df)
    assert growth == 800.0

def test_compute_avg_order_value(sample_df):
    aov = compute_avg_order_value(sample_df)
    assert aov == 300.0

def test_detect_anomalies(sample_df):
    anomalies = detect_anomalies(sample_df, threshold=1.0)
    assert len(anomalies) > 0
    assert 2000 in anomalies['revenue'].values
