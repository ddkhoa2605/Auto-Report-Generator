import pandas as pd
from app.processor import (
    compute_daily_revenue,
    compute_top_products,
    compute_revenue_growth,
    compute_avg_order_value,
    detect_anomalies
)

def format_currency_vnd(amount: float) -> str:
    """Định dạng số tiền sang VNĐ (ví dụ: 1.250.000 VNĐ)."""
    return f"{amount:,.0f} VNĐ".replace(",", ".")

def build_metrics_payload(df: pd.DataFrame) -> dict:
    """
    Tổng hợp tất cả các chỉ số kinh doanh thành một dictionary cấu trúc
    để chuẩn bị gửi cho AI Engine hoặc Dashboard.
    """
    total_revenue = df['revenue'].sum()
    growth = compute_revenue_growth(df)
    aov = compute_avg_order_value(df)
    total_orders = df['orders'].sum() if 'orders' in df.columns else len(df)
    
    # Lấy top 5 sản phẩm
    top_products_df = compute_top_products(df, n=5)
    top_products = []
    if not top_products_df.empty:
        for _, row in top_products_df.iterrows():
            top_products.append({
                "name": row['product'],
                "revenue": float(row['revenue']),
                "share": round(row['revenue'] / total_revenue, 2) if total_revenue > 0 else 0
            })
            
    # Lấy thông tin ngày tệ nhất/tốt nhất
    daily_rev = compute_daily_revenue(df)
    best_day_row = daily_rev.loc[daily_rev['revenue'].idxmax()]
    worst_day_row = daily_rev.loc[daily_rev['revenue'].idxmin()]
    
    # Phát hiện bất thường
    anomalies_df = detect_anomalies(df)
    anomalies = []
    if not anomalies_df.empty:
        for _, row in anomalies_df.iterrows():
            anomalies.append({
                "date": str(row['date'].date()),
                "revenue": float(row['revenue']),
                "type": "high" if row['z_score'] > 0 else "low"
            })

    # Tạo payload cuối cùng
    payload = {
        "summary": {
            "period": f"{df['date'].min().date()} to {df['date'].max().date()}",
            "total_revenue": float(total_revenue),
            "total_orders": int(total_orders),
            "avg_order_value": float(aov),
            "revenue_growth_percent": float(growth)
        },
        "top_products": top_products,
        "performance_highlights": {
            "best_day": {
                "date": str(best_day_row['date'].date()),
                "revenue": float(best_day_row['revenue'])
            },
            "worst_day": {
                "date": str(worst_day_row['date'].date()),
                "revenue": float(worst_day_row['revenue'])
            }
        },
        "anomalies": anomalies
    }
    
    return payload
