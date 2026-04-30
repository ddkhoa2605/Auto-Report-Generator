# AI Business Insight Dashboard (Vietnam-ready)

Hệ thống AI Agent tự động hóa quá trình phân tích dữ liệu và tạo báo cáo cho doanh nghiệp Việt Nam.

## 🚀 Tính năng chính
- Tự động nhận diện schema dữ liệu (CSV/Excel)
- Tính toán Business Metrics tự động
- Phát hiện bất thường (Anomaly Detection)
- Sinh Insight thông minh bằng AI (OpenAI)
- Dashboard trực quan bằng Streamlit
- Xuất báo cáo PDF chuyên nghiệp

## 🛠️ Cài đặt

1. Clone repository
2. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Cấu hình API Key trong file `.env`:
   ```
   OPENAI_API_KEY=your_actual_key
   ```
4. Chạy ứng dụng:
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```
