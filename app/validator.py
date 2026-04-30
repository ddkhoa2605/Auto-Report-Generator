import pandas as pd
import numpy as np
import os
import json
from typing import List, Tuple
from google import genai
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Khởi tạo Gemini client (lazy loading)
_client = None

def get_gemini_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY không được tìm thấy trong môi trường.")
        _client = genai.Client(api_key=api_key)
    return _client

# Từ điển ánh xạ các cột phổ biến
COLUMN_MAPPING = {
    'date': ['date', 'ngày', 'created_at', 'order_date', 'thời gian', 'ngay', 'ngày đặt hàng', 'ngay_dat_hang'],
    'revenue': ['revenue', 'doanh thu', 'rev', 'total', 'amount', 'tiền', 'doanhthu', 'tong_tien', 'doanh thu'],
    'product': ['product', 'sản phẩm', 'item', 'product_name', 'tên sp', 'san_pham', 'ten_san_pham', 'tên sản phẩm'],
    'orders': ['orders', 'đơn hàng', 'count', 'quantity', 'số đơn', 'so_luong', 'don_hang', 'số lượng']
}

def load_file(path: str) -> pd.DataFrame:
    """Đọc file từ đường dẫn, hỗ trợ CSV và Excel."""
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(path)
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Định dạng file {ext} không được hỗ trợ.")

def detect_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Tự động ánh xạ tên cột dựa trên alias."""
    new_columns = {}
    for col in df.columns:
        col_lower = str(col).lower().strip()
        for target, aliases in COLUMN_MAPPING.items():
            if col_lower in aliases:
                new_columns[col] = target
                break
    
    return df.rename(columns=new_columns)

def ai_column_mapping(
    df: pd.DataFrame,
    target_columns: List[str]
) -> Tuple[pd.DataFrame, dict]:
    """
    Sử dụng Gemini để mapping các cột không rõ ràng về schema chuẩn.
    Chỉ được gọi khi rule-based mapping không đủ.
    """
    input_columns = df.columns.tolist()

    prompt = f"""
    Bạn là chuyên gia xử lý dữ liệu.

    Hãy map các cột input sang các cột chuẩn.

    Input columns:
    {input_columns}

    Target columns:
    {target_columns}

    Trả về JSON format:
    {{"input_column": "target_column"}}

    Chỉ map khi chắc chắn. Chỉ trả về JSON. Không giải thích.
    """

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"temperature": 0}
        )
        content = response.text.strip()

        # Xử lý markdown code block nếu Gemini trả về
        content = content.replace("```json", "").replace("```", "").strip()
        mapping = json.loads(content)

    except Exception as e:
        print("Gemini mapping failed:", e)
        return df, {}

    # Chỉ áp dụng mapping hợp lệ
    valid_mapping = {
        k: v for k, v in mapping.items()
        if k in input_columns and v in target_columns
    }

    df_renamed = df.rename(columns=valid_mapping)
    return df_renamed, valid_mapping

def validate_schema(df: pd.DataFrame) -> tuple:
    """Kiểm tra xem các cột bắt buộc có tồn tại không."""
    required = ['date', 'revenue']
    missing = [col for col in required if col not in df.columns]
    if missing:
        return False, f"Thiếu các cột bắt buộc: {', '.join(missing)}"
    return True, "Hợp lệ"

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Xử lý giá trị trống trong các cột quan trọng."""
    df = df.copy()
    if 'date' in df.columns and 'revenue' in df.columns:
        df = df.dropna(subset=['date', 'revenue'])
    
    if 'product' in df.columns:
        df.loc[:, 'product'] = df['product'].fillna('Unknown')
    if 'orders' in df.columns:
        df.loc[:, 'orders'] = df['orders'].fillna(1)
        
    return df

def normalize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa định dạng ngày tháng và số."""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    for col in ['revenue', 'orders']:
        if col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].replace('[^0-9.]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df.dropna(subset=['date', 'revenue'])

def validate_pipeline(path: str) -> pd.DataFrame:
    """Pipeline tổng thể để validate dữ liệu."""
    df = load_file(path)
    df = detect_columns(df)
    
    current_cols = df.columns.tolist()
    if 'date' not in current_cols or 'revenue' not in current_cols:
        df, ai_mapping = ai_column_mapping(df, list(COLUMN_MAPPING.keys()))
    
    is_valid, msg = validate_schema(df)
    if not is_valid:
        raise ValueError(msg)
        
    df = handle_missing_values(df)
    df = normalize_formats(df)
    
    return df
