import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_ecommerce_sample():
    np.random.seed(42)
    days = 90
    start_date = datetime(2026, 1, 1)
    data = []
    products = ["Áo thun basic", "Quần Jean nam", "Váy hoa nhí", "Giày sneaker", "Túi xách nữ"]
    for i in range(500):
        date = start_date + timedelta(days=np.random.randint(0, days))
        product = np.random.choice(products)
        price = np.random.randint(10, 50) * 10000
        quantity = np.random.randint(1, 5)
        revenue = price * quantity
        if date == datetime(2026, 4, 10):
            revenue = revenue * 0.1
        data.append({
            "Ngày đặt hàng": date.strftime("%Y-%m-%d"),
            "Tên sản phẩm": product,
            "Doanh thu": revenue,
            "Số lượng": quantity
        })
    df = pd.DataFrame(data)
    df.to_csv("data/sample/ecommerce_sample.csv", index=False, encoding="utf-8-sig")

def generate_marketing_ads():
    start_date = datetime(2026, 4, 1)
    data = []
    campaigns = ["Sale 4.4", "New Arrival", "Branding Brand"]
    for i in range(30):
        date = start_date + timedelta(days=i)
        for cp in campaigns:
            spend = np.random.randint(50, 200) * 10000
            revenue = spend * np.random.uniform(2, 6)
            orders = int(revenue / 200000)
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "campaign": cp,
                "revenue": revenue,
                "spend": spend,
                "orders": orders
            })
    df = pd.DataFrame(data)
    df.to_csv("data/sample/marketing_ads.csv", index=False)

def generate_sme_weekly():
    data = [
        {"Ngày": "2026-04-01", "Doanh thu": 5000000, "Đơn hàng": 20},
        {"Ngày": "2026-04-02", "Doanh thu": 4500000, "Đơn hàng": 18},
        {"Ngày": "2026-04-03", "Doanh thu": 7000000, "Đơn hàng": 30},
        {"Ngày": "2026-04-04", "Doanh thu": 12000000, "Đơn hàng": 50},
        {"Ngày": "2026-04-05", "Doanh thu": 11000000, "Đơn hàng": 45},
        {"Ngày": "2026-04-06", "Doanh thu": 200000, "Đơn hàng": 2},
        {"Ngày": "2026-04-07", "Doanh thu": 5200000, "Đơn hàng": 22},
    ]
    df = pd.DataFrame(data)
    df.to_csv("data/sample/sme_weekly.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    os.makedirs("data/sample", exist_ok=True)
    generate_ecommerce_sample()
    generate_marketing_ads()
    generate_sme_weekly()
