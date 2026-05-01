import pandas as pd
from app.processor import (
    compute_daily_revenue,
    compute_top_products,
    compute_growth_metrics,
    compute_efficiency_metrics,
    detect_anomalies
)

def format_currency_vnd(amount: float) -> str:
    """Định dạng số tiền sang VNĐ, thu gọn thành Triệu/Tỷ nếu số quá lớn."""
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.2f}".replace(".", ",") + " Tỷ VNĐ"
    elif amount >= 1_000_000:
        return f"{amount / 1_000_000:.2f}".replace(".", ",") + " Tr VNĐ"
    else:
        return f"{amount:,.0f} VNĐ".replace(",", ".")

def build_metrics_payload(df: pd.DataFrame) -> dict:
    """
    Tổng hợp toàn bộ các chỉ số kinh doanh chuyên sâu.
    """
    total_rev = float(df['revenue'].sum())
    total_ord = int(df['orders'].sum() if 'orders' in df.columns else len(df))
    
    # 1. Growth & Trend
    growth = compute_growth_metrics(df)
    
    # 2. Efficiency
    efficiency = compute_efficiency_metrics(df)
    
    # 3. Distribution (Top products)
    top_products_df = compute_top_products(df, n=5)
    top_products = []
    if not top_products_df.empty:
        for _, row in top_products_df.iterrows():
            top_products.append({
                "name": str(row['product']),
                "revenue": float(row['revenue']),
                "share_percent": round(row['revenue'] / total_rev * 100, 2) if total_rev > 0 else 0
            })
            
    # 4. Anomaly
    anomalies_df = detect_anomalies(df)
    anomalies = []
    if not anomalies_df.empty:
        for _, row in anomalies_df.iterrows():
            anomalies.append({
                "date": str(row['date'].date()),
                "revenue": float(row['revenue']),
                "anomaly_percent": float(row['anomaly_percent']),
                "status": "Tăng đột biến" if row['anomaly_percent'] > 0 else "Giảm sốc"
            })

    # Cấu trúc Payload chuẩn
    payload = {
        "summary": {
            "period": f"{df['date'].min().date()} to {df['date'].max().date()}",
            "total_revenue": total_rev,
            "total_orders": total_ord,
            "avg_order_value": efficiency['revenue_per_order']
        },
        "growth_and_trend": growth,
        "efficiency": efficiency,
        "distribution": {
            "top_products": top_products
        },
        "anomalies": anomalies
    }
    
    return payload
