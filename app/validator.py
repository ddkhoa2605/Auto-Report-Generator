import pandas as pd
import numpy as np
import os

def load_file(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        try: return pd.read_csv(path, encoding='utf-8')
        except: return pd.read_csv(path, encoding='latin-1')
    return pd.read_excel(path)

def validate_pipeline(path: str) -> pd.DataFrame:
    df = load_file(path)
    
    # 1. Rule-based Mapping siêu tốc
    COLUMN_MAPPING = {
        'date': ['date', 'ngày', 'time', 'created_at', 'order_date', 'thời gian', 'ngay', 'ngày đặt hàng', 'ngay_dat_hang', 'thời điểm'],
        'revenue': ['revenue', 'doanh thu', 'rev', 'total', 'amount', 'tiền', 'doanhthu', 'tong_tien', 'doanh thu', 'giá trị'],
        'product': ['product', 'sản phẩm', 'item', 'product_name', 'tên sp', 'san_pham', 'ten_san_pham', 'tên sản phẩm'],
        'orders': ['orders', 'đơn hàng', 'count', 'quantity', 'số đơn', 'so_luong', 'don_hang', 'số lượng']
    }
    
    new_cols = {}
    for col in df.columns:
        col_clean = str(col).lower().strip()
        for target, aliases in COLUMN_MAPPING.items():
            if col_clean in aliases:
                new_cols[col] = target
                break
    
    df = df.rename(columns=new_cols)
    
    # Phương án dự phòng: Tự gán 2 cột đầu tiên nếu không nhận ra
    if 'date' not in df.columns or 'revenue' not in df.columns:
        if len(df.columns) >= 2:
            df = df.rename(columns={df.columns[0]: 'date', df.columns[1]: 'revenue'})
    
    # 2. Ép kiểu và làm sạch
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    for col in ['revenue', 'orders']:
        if col in df.columns:
            if df[col].dtype == object:
                # Xóa các ký tự không phải số (đ, $, phẩy...)
                df[col] = df[col].astype(str).str.replace(r'[^0-9.-]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Gán mặc định 1 đơn hàng nếu bị NaN
            if col == 'orders':
                df[col] = df[col].fillna(1)
    
    # Xóa dòng rỗng
    df = df.dropna(subset=['date', 'revenue'])
    
    if df.empty:
        raise ValueError("Dữ liệu sau khi xử lý bị trống. Hãy kiểm tra định dạng cột Ngày và Doanh thu.")
        
    return df
