# 📊 AI Business Insight Dashboard

**AI Business Insight Dashboard** là một giải pháp phân tích dữ liệu kinh doanh thông minh, tự động chuyển đổi các file báo cáo thô (CSV/Excel) thành các biểu đồ trực quan và nhận xét chuyên sâu từ trí tuệ nhân tạo (Gemini 2.0 Flash).

Dự án được thiết kế để hỗ trợ các doanh nghiệp SME, người bán hàng E-commerce (Shopee, Lazada, TikTok Shop) nắm bắt tình hình kinh doanh chỉ trong vài giây.

---

## 🔥 Tính năng nổi bật

- **🤖 AI-Powered Mapping**: Tự động nhận diện và ánh xạ các cột dữ liệu (Ngày tháng, Doanh thu, Sản phẩm) bằng AI, hỗ trợ cả tiếng Anh và tiếng Việt.
- **📈 Phân tích KPI tự động**: Tính toán ngay lập tức Tổng doanh thu, Tăng trưởng, AOV (Giá trị đơn hàng trung bình).
- **🚨 Phát hiện bất thường (Anomaly Detection)**: Sử dụng thuật toán Z-Score để cảnh báo các ngày có biến động doanh thu lạ.
- **💡 AI Business Consultant**: Tích hợp Gemini 2.0 Flash để đưa ra nhận xét, cảnh báo rủi ro và đề xuất hành động cụ thể.
- **📄 Xuất báo cáo chuyên nghiệp**: Tải về bản phân tích dưới dạng file PDF chỉ với một cú click.
- **💎 Giao diện cao cấp**: UI hiện đại, responsive, hiệu ứng Glassmorphism tinh tế.

---

## 🛠 Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.9+
- **Giao diện**: Streamlit (Custom CSS)
- **AI Engine**: Google Gemini 2.0 Flash SDK
- **Xử lý dữ liệu**: Pandas, NumPy
- **Trực quan hóa**: Plotly Express
- **Báo cáo**: ReportLab (PDF Generator)

---

## 🚀 Hướng dẫn cài đặt

### 1. Clone repository
```bash
git clone https://github.com/ddkhoa2605/report_generator.git
cd report_generator
```

### 2. Cài đặt môi trường
Khuyên dùng `venv` hoặc `conda`:
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Cấu hình API Key
1. Copy file `.env.example` thành `.env`:
   ```bash
   cp .env.example .env
   ```
2. Mở file `.env` và điền **GEMINI_API_KEY** của bạn (Lấy key tại [Google AI Studio](https://aistudio.google.com/)).

### 4. Chạy ứng dụng
```bash
streamlit run streamlit_app.py
```

---

## 📂 Cấu trúc thư mục

```text
├── app/
│   ├── validator.py   # Làm sạch & Ánh xạ dữ liệu
│   ├── processor.py   # Tính toán KPI & Bất thường
│   ├── metrics.py     # Tổng hợp dữ liệu cho AI
│   ├── ai_engine.py   # Kết nối Gemini AI
│   ├── visualizer.py  # Logic vẽ biểu đồ Plotly
│   └── reporter.py    # Xuất báo cáo PDF
├── data/
│   └── sample/        # Dữ liệu mẫu (Ecommerce, Ads, SME)
├── tests/             # Unit tests & Integration tests
├── streamlit_app.py   # File chạy chính giao diện
└── requirements.txt   # Danh sách thư viện
```

---

## 📝 Giấy phép
Dự án được phát hành dưới giấy phép MIT. Tự do sử dụng và đóng góp!

---
*Phát triển bởi **Đoàn Đăng Khoa** - 2026*
