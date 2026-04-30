# AI Business Insight Dashboard (Vietnam-ready)

## 1. Tổng quan

Dự án này xây dựng một hệ thống AI Agent kết hợp với dashboard (Streamlit) giúp doanh nghiệp tự động hóa quá trình phân tích dữ liệu và tạo báo cáo.

Người dùng chỉ cần upload file dữ liệu (CSV/Excel), hệ thống sẽ:
- Làm sạch và chuẩn hóa dữ liệu
- Tính toán các chỉ số kinh doanh
- Phát hiện bất thường
- Sinh insight bằng AI
- Hiển thị dashboard + xuất báo cáo PDF

Mục tiêu:
- Giảm thời gian làm báo cáo từ vài giờ xuống vài chục giây
- Giảm lỗi thủ công
- Tăng khả năng phát hiện insight

---

## 2. Use case thực tế tại Việt Nam

### 2.1 E-commerce (Shopee, TikTok Shop)
- Phân tích đơn hàng
- Doanh thu theo ngày
- Sản phẩm bán chạy
- Phát hiện ngày doanh thu giảm mạnh

### 2.2 Marketing (Facebook Ads, Google Ads)
- Phân tích chi phí quảng cáo
- ROAS, CAC
- Campaign kém hiệu quả

### 2.3 Doanh nghiệp nhỏ (SME)
- Báo cáo tuần/tháng tự động
- Theo dõi hiệu suất kinh doanh

---

## 3. Kiến trúc hệ thống

Flow tổng thể:

User Upload → Data Validation → Data Processing → Business Metrics → AI Insight → Visualization → Report

### 3.1 Data Validation Layer
- Kiểm tra cột bắt buộc
- Chuẩn hóa format (date, number)
- Xử lý missing value

### 3.2 Data Processing
- Sử dụng pandas
- Tính toán:
  - Tổng doanh thu
  - Doanh thu theo ngày
  - Top sản phẩm
  - Tăng trưởng

### 3.3 Business Metrics Layer (quan trọng)

Chuẩn hóa dữ liệu thành dạng structured:

```json
{
  "revenue_growth": -12,
  "top_product": "Áo thun",
  "worst_day": "2026-04-10",
  "avg_order_value": 120000
}
```

### 3.4 AI Insight Engine
- Sử dụng OpenAI API
- Prompt tiếng Việt
- Output:
  - Insight
  - Cảnh báo
  - Đề xuất

### 3.5 Visualization
- Line chart (trend)
- Bar chart (top product)

### 3.6 Report Generator
- Xuất PDF hoặc Markdown
- Nội dung:
  - Tổng quan
  - Xu hướng
  - Vấn đề
  - Đề xuất

---

## 4. Thiết kế Input (Semi-structured)

### 4.1 Expected schema

```json
{
  "date": "datetime",
  "product": "string",
  "revenue": "number",
  "orders": "number"
}
```

### 4.2 Auto mapping

Ví dụ mapping:

- date: ["date", "ngày", "created_at"]
- revenue: ["revenue", "doanh thu", "rev"]

### 4.3 AI-assisted mapping

Xử lý các trường hợp không rõ ràng bằng AI.

### 4.4 Validation rules
- Bắt buộc: date, revenue
- Kiểm tra kiểu dữ liệu
- Xử lý missing value

---

## 5. Dashboard (Streamlit)

Chức năng:
- Upload file
- Auto detect schema
- Hiển thị chart
- Hiển thị insight AI
- Download báo cáo

Flow:
1. Upload file
2. Click "Generate Report"
3. Xem kết quả

---

## 6. KPI đo hiệu quả

- Thời gian: 2–3 giờ → < 1 phút
- Tự động hóa: 80–90%
- Giảm lỗi manual
- Phát hiện anomaly tự động

---

## 7. Điểm mạnh khi đưa vào CV

- Có pipeline rõ ràng
- Có xử lý dữ liệu thực tế
- Có business logic
- Có AI integration
- Có dashboard

Ví dụ mô tả:

- Xây dựng hệ thống AI tự động phân tích dữ liệu kinh doanh và tạo báo cáo
- Thiết kế pipeline gồm validation, processing, AI insight, visualization
- Giảm thời gian làm báo cáo ~95%

---

## 8. Hướng mở rộng

- Chat với dữ liệu
- Lưu lịch sử báo cáo
- Gửi alert qua email khi có bất thường
- Multi-user

---

## 9. Demo khi phỏng vấn

Kịch bản:
- Upload file dữ liệu bán hàng
- System tự động phân tích
- Hiển thị insight:
  - Doanh thu giảm mạnh ngày X
  - Sản phẩm A chiếm 60%

---

## 10. Kết luận

Đây là một project mang tính thực tế cao, kết hợp:
- Data engineering
- AI
- Business analytics
- Product thinking

Nếu triển khai tốt, project này có thể đạt mức:

"junior có tư duy mid-level"

