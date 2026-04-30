import pandas as pd
import numpy as np

def compute_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Tính toán doanh thu tổng theo từng ngày."""
    daily_res = df.groupby('date')['revenue'].sum().reset_index()
    return daily_res.sort_values('date')

def compute_top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Tính toán Top N sản phẩm theo doanh thu."""
    if 'product' not in df.columns:
        return pd.DataFrame()
    top_res = df.groupby('product')['revenue'].sum().reset_index()
    return top_res.sort_values('revenue', ascending=False).head(n)

def compute_revenue_growth(df: pd.DataFrame) -> float:
    """Tính % tăng trưởng doanh thu."""
    df = df.sort_values('date')
    mid_point = len(df) // 2
    if mid_point == 0:
        return 0.0
    first_half_rev = df.iloc[:mid_point]['revenue'].sum()
    second_half_rev = df.iloc[mid_point:]['revenue'].sum()
    if first_half_rev == 0:
        return 0.0
    growth = ((second_half_rev - first_half_rev) / first_half_rev) * 100
    return round(growth, 2)

def compute_avg_order_value(df: pd.DataFrame) -> float:
    """Tính giá trị đơn hàng trung bình (AOV)."""
    total_revenue = df['revenue'].sum()
    total_orders = df['orders'].sum() if 'orders' in df.columns else len(df)
    if total_orders == 0:
        return 0.0
    return round(total_revenue / total_orders, 2)

def detect_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """Phát hiện bất thường trong doanh thu hàng ngày bằng Z-score."""
    daily_rev = compute_daily_revenue(df)
    if len(daily_rev) < 3:
        return pd.DataFrame()
    mean_rev = daily_rev['revenue'].mean()
    std_rev = daily_rev['revenue'].std()
    if std_rev == 0:
        return pd.DataFrame()
    daily_rev['z_score'] = (daily_rev['revenue'] - mean_rev) / std_rev
    anomalies = daily_rev[daily_rev['z_score'].abs() > threshold].copy()
    return anomalies
