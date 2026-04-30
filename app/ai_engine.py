import os
import json
from google import genai
from dotenv import load_dotenv

# Load môi trường
load_dotenv()

# Khởi tạo Gemini client (lazy loading)
_client = None

def get_gemini_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY không tìm thấy trong file .env")
        _client = genai.Client(api_key=api_key)
    return _client

def generate_insight(metrics: dict) -> dict:
    """
    Gửi metrics cho Gemini và nhận lại báo cáo phân tích thông minh.
    """
    prompt = f"""
    Bạn là chuyên gia phân tích dữ liệu kinh doanh cao cấp dành cho thị trường Việt Nam.
    Dựa trên dữ liệu kinh doanh dưới đây, hãy đưa ra báo cáo phân tích chi tiết.

    DỮ LIỆU KINH DOANH:
    {json.dumps(metrics, indent=2, ensure_ascii=False)}

    YÊU CẦU:
    1. Phân tích xu hướng doanh thu và sự tăng trưởng.
    2. Đánh giá hiệu suất sản phẩm (Top products).
    3. Nhận diện các điểm bất thường và giải thích nguyên nhân có thể có.
    4. Đưa ra CẢNH BÁO nếu thấy rủi ro.
    5. Đưa ra 3-5 ĐỀ XUẤT hành động cụ thể.

    ĐỊNH DẠNG TRẢ VỀ: Chỉ trả về JSON, không giải thích thêm.
    {{
        "summary": "Đoạn văn tóm tắt tổng quan tình hình kinh doanh...",
        "insights": ["insight 1", "insight 2", "insight 3"],
        "warnings": ["cảnh báo 1", "cảnh báo 2"],
        "recommendations": ["đề xuất 1", "đề xuất 2", "đề xuất 3"],
        "sentiment": "Tích cực hoặc Tiêu cực hoặc Trung lập"
    }}

    Viết bằng tiếng Việt, chuyên nghiệp nhưng dễ hiểu cho chủ doanh nghiệp.
    """

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"temperature": 0.3}
        )
        content = response.text.strip()

        # Xử lý markdown code block nếu Gemini trả về
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)

    except Exception as e:
        print(f"Lỗi khi gọi Gemini AI Engine: {e}")
        return {
            "summary": "Không thể tạo báo cáo AI lúc này.",
            "insights": [],
            "warnings": ["Lỗi kết nối AI"],
            "recommendations": [],
            "sentiment": "N/A"
        }
