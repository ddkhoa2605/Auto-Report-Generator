import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load môi trường
load_dotenv()

# Khởi tạo OpenAI client (Lazy loading)
_client = None

def get_openai_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY không tìm thấy trong file .env")
        _client = OpenAI(api_key=api_key)
    return _client

def generate_insight(metrics: dict) -> dict:
    """
    Gửi metrics cho OpenAI và nhận lại báo cáo phân tích thông minh.
    """
    prompt = f"""
    Bạn là một chuyên gia phân tích dữ liệu kinh doanh cao cấp (Business Analyst) dành cho thị trường Việt Nam.
    Dựa trên dữ liệu kinh doanh dưới đây, hãy đưa ra báo cáo phân tích chi tiết.

    DỮ LIỆU KINH DOANH:
    {json.dumps(metrics, indent=2, ensure_ascii=False)}

    YÊU CẦU:
    1. Phân tích xu hướng doanh thu và sự tăng trưởng.
    2. Đánh giá hiệu suất sản phẩm (Top products).
    3. Nhận diện các điểm bất thường (Anomalies) và giải thích nguyên nhân có thể có.
    4. Đưa ra các CẢNH BÁO nếu thấy rủi ro.
    5. Đưa ra 3-5 ĐỀ XUẤT hành động cụ thể để tăng doanh thu hoặc giảm rủi ro.

    ĐỊNH DẠNG TRẢ VỀ (JSON):
    {{
        "summary": "Đoạn văn tóm tắt tổng quan tình hình kinh doanh...",
        "insights": ["insight 1", "insight 2", ...],
        "warnings": ["cảnh báo 1", "cảnh báo 2", ...],
        "recommendations": ["đề xuất 1", "đề xuất 2", ...],
        "sentiment": "Tích cực/Tiêu cực/Trung lập"
    }}

    LƯU Ý: Viết bằng tiếng Việt, ngôn ngữ chuyên nghiệp nhưng dễ hiểu cho chủ doanh nghiệp.
    """

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia phân tích dữ liệu kinh doanh chuyên nghiệp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"Lỗi khi gọi AI Engine: {e}")
        return {
            "summary": "Không thể tạo báo cáo AI lúc này.",
            "insights": [],
            "warnings": ["Lỗi kết nối AI"],
            "recommendations": [],
            "sentiment": "N/A"
        }
