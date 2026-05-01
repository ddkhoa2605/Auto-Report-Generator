import os
import json
import logging
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Cache kết quả trong bộ nhớ
_response_cache = {}

def generate_insight(metrics: dict) -> dict:
    """Gọi Coze API để lấy phân tích."""
    global _response_cache
    
    # Reload lại env để lấy key mới nhất trong trường hợp Streamlit chưa restart
    load_dotenv(override=True)
    coze_api_key = os.getenv("COZE_API_KEY")
    bot_id = os.getenv("COZE_BOT_ID")
    
    # ── 1. Đưa trực tiếp Metrics chuyên sâu vào Prompt ───────────────────
    # Dữ liệu hiện đã được nén, tính toán rất nhỏ (Không còn rác)
    
    # ── 2. Xây dựng Query chuẩn hóa cho Coze ─────────────────────────────
    query = f"""
Dữ liệu metrics:
{json.dumps(metrics, ensure_ascii=False, indent=2)}

HÃY ĐÓNG VAI LÀ CHUYÊN GIA PHÂN TÍCH KINH DOANH.
TRẢ VỀ ĐÚNG FORMAT JSON SAU (không giải thích thêm, không có ```json):
{{
    "summary": "1 câu tóm tắt",
    "insights": ["1 ý chính"],
    "warnings": ["1 cảnh báo"],
    "recommendations": ["1 đề xuất"],
    "sentiment": "Tích cực/Tiêu cực/Trung lập"
}}
"""

    # ── 3. Caching ────────────────────────────────────────────────────────
    cache_key = hashlib.md5(query.encode()).hexdigest()
    if cache_key in _response_cache:
        log.info("⚡ Sử dụng kết quả từ Cache.")
        return _response_cache[cache_key]

    if not coze_api_key or not bot_id:
        log.warning("Chưa cấu hình Coze API (.env). Dùng Fallback.")
        return _get_fallback_insight(metrics, "Chưa điền API Key hoặc Bot ID trong file .env")

    # ── 4. Gọi Coze API ───────────────────────────────────────────────────
    url = "https://api.coze.com/open_api/v2/chat"
    headers = {
        "Authorization": f"Bearer {coze_api_key}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    
    payload = {
        "bot_id": bot_id,
        "user": "report_user",
        "query": query,
        "stream": False
    }

    try:
        log.info("Đang gọi Coze API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return _get_fallback_insight(metrics, f"HTTP {response.status_code}: {response.text}")
            
        data = response.json()
        
        # Bắt lỗi logic từ Coze (vd: không có quyền, bot chưa publish)
        if data.get("code") != 0:
            error_msg = data.get("msg", "Unknown error")
            log.error(f"Coze API error: {error_msg}")
            return _get_fallback_insight(metrics, f"Lỗi Coze: {error_msg}")
            
        messages = data.get("messages", [])
        
        # Tìm tin nhắn trả về (type = answer)
        answer = ""
        for msg in messages:
            if msg.get("type") == "answer":
                answer = msg.get("content", "")
                break
                
        if not answer and messages:
            answer = messages[-1].get("content", "")
            
        if not answer:
            return _get_fallback_insight(metrics, "Coze trả về kết quả rỗng.")
            
        # Parse JSON
        content = answer.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            log.warning("Coze không trả về JSON. Đang tự động bóc tách văn bản (Text Parsing).")
            result = _parse_coze_text_to_json(answer, metrics)
            
        _response_cache[cache_key] = result
        return result
        
    except Exception as e:
        log.error(f"Lỗi khi xử lý kết quả Coze: {e}")
        return _get_fallback_insight(metrics, str(e))

def _parse_coze_text_to_json(text: str, metrics: dict) -> dict:
    """Tự động phân tách Text thông thường thành chuẩn JSON của Dashboard."""
    lines = text.strip().split('\n')
    
    summary = "Phân tích từ Coze AI"
    insights, warnings, recommendations = [], [], []
    current_section = "insights"
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        line_lower = line.lower()
        # Chuyển cờ section
        if "vấn đề" in line_lower or "cảnh báo" in line_lower or "rủi ro" in line_lower:
            current_section = "warnings"
            continue
        elif "đề xuất" in line_lower or "khắc phục" in line_lower or "giải pháp" in line_lower or "action" in line_lower:
            current_section = "recommendations"
            continue
        elif "insight" in line_lower or "tóm tắt" in line_lower or "điểm sáng" in line_lower:
            current_section = "insights"
            continue
            
        # Thu thập dữ liệu
        if line.startswith('-') or line.startswith('*'):
            clean_line = line[1:].strip()
            if current_section == "insights": insights.append(clean_line)
            elif current_section == "warnings": warnings.append(clean_line)
            elif current_section == "recommendations": recommendations.append(clean_line)
        else:
            if current_section == "insights" and len(insights) == 0:
                summary = line

    growth = metrics.get("growth_and_trend", {}).get("revenue_growth_rate", 0)
    
    # Điền mặc định nếu thiếu
    if not insights: insights.append("Đã phân tích xong dữ liệu từ hệ thống.")
    if not warnings: warnings.append("Chưa phát hiện rủi ro đáng kể.")
    if not recommendations: recommendations.append("Tiếp tục theo dõi các chỉ số quan trọng.")

    return {
        "summary": summary,
        "insights": insights,
        "warnings": warnings,
        "recommendations": recommendations,
        "sentiment": "Tích cực" if growth >= 0 else "Tiêu cực"
    }

def _get_fallback_insight(metrics: dict, error_msg: str) -> dict:
    """Tạo báo cáo cứng nếu API bị lỗi/chưa có cấu hình."""
    growth = metrics.get("growth_and_trend", {}).get("revenue_growth_rate", 0)
    sentiment = "Tích cực" if growth >= 0 else "Tiêu cực"
    
    top_products = metrics.get("distribution", {}).get("top_products", [])
    top_prd = top_products[0]["name"] if top_products else "Chưa rõ"
    
    anomaly_count = len(metrics.get("anomalies", []))
    
    return {
        "summary": f"Sử dụng AI thất bại: {error_msg}",
        "insights": [f"Doanh thu thay đổi {growth}% so với kỳ trước.", f"Sản phẩm nổi bật: {top_prd}"],
        "warnings": [f"Hệ thống phát hiện {anomaly_count} ngày có doanh thu bất thường."],
        "recommendations": [
            "Tăng cường marketing" if growth < 0 else "Phát huy chiến lược hiện tại"
        ],
        "sentiment": sentiment
    }

