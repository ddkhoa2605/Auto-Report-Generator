import pandas as pd
import numpy as np

def compute_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Tính toán doanh thu và đơn hàng tổng theo từng ngày."""
    if 'orders' not in df.columns:
        df['orders'] = 1
    return df.groupby('date').agg({'revenue': 'sum', 'orders': 'sum'}).reset_index().sort_values('date')

def compute_top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Tính toán Top N sản phẩm theo doanh thu."""
    if 'product' not in df.columns:
        return pd.DataFrame()
    top_res = df.groupby('product')['revenue'].sum().reset_index()
    return top_res.sort_values('revenue', ascending=False).head(n)

def compute_growth_metrics(df: pd.DataFrame) -> dict:
    """Tính % tăng trưởng đa chiều: Doanh thu, Đơn hàng, AOV (kỳ này vs kỳ trước)."""
    df = df.sort_values('date')
    mid_point = len(df) // 2
    if mid_point == 0:
        return {"revenue_growth_rate": 0.0, "orders_growth_rate": 0.0, "aov_growth_rate": 0.0}
    
    fh = df.iloc[:mid_point]
    sh = df.iloc[mid_point:]
    
    fh_rev = fh['revenue'].sum()
    sh_rev = sh['revenue'].sum()
    rev_growth = ((sh_rev - fh_rev) / fh_rev * 100) if fh_rev > 0 else 0.0
    
    fh_ord = fh['orders'].sum() if 'orders' in fh.columns else len(fh)
    sh_ord = sh['orders'].sum() if 'orders' in sh.columns else len(sh)
    ord_growth = ((sh_ord - fh_ord) / fh_ord * 100) if fh_ord > 0 else 0.0
    
    fh_aov = fh_rev / fh_ord if fh_ord > 0 else 0
    sh_aov = sh_rev / sh_ord if sh_ord > 0 else 0
    aov_growth = ((sh_aov - fh_aov) / fh_aov * 100) if fh_aov > 0 else 0.0
    
    return {
        "revenue_growth_rate": round(rev_growth, 2),
        "orders_growth_rate": round(ord_growth, 2),
        "aov_growth_rate": round(aov_growth, 2)
    }

def compute_efficiency_metrics(df: pd.DataFrame) -> dict:
    """Tính toán hiệu suất: Số đơn/ngày, Doanh thu/đơn."""
    total_rev = df['revenue'].sum()
    total_orders = df['orders'].sum() if 'orders' in df.columns else len(df)
    unique_days = df['date'].nunique()
    
    return {
        "avg_orders_per_day": round(total_orders / unique_days, 1) if unique_days > 0 else 0,
        "revenue_per_order": round(total_rev / total_orders, 2) if total_orders > 0 else 0
    }

def detect_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """Phát hiện bất thường với đầy đủ % tăng/giảm so với trung bình."""
    daily_rev = compute_daily_revenue(df)
    if len(daily_rev) < 3:
        return pd.DataFrame()
        
    mean_rev = daily_rev['revenue'].mean()
    std_rev = daily_rev['revenue'].std()
    
    if std_rev == 0:
        return pd.DataFrame()
        
    daily_rev['z_score'] = (daily_rev['revenue'] - mean_rev) / std_rev
    daily_rev['anomaly_percent'] = ((daily_rev['revenue'] - mean_rev) / mean_rev * 100).round(2)
    
    return daily_rev[daily_rev['z_score'].abs() > threshold].copy()
