# 📊 AI Business Insight Dashboard — Project Plan

> **Mục tiêu:** Xây dựng hệ thống AI Agent tự động hóa phân tích dữ liệu kinh doanh và tạo báo cáo thông minh cho doanh nghiệp Việt Nam.

---

## 🗂️ Tổng quan dự án

| Thuộc tính | Chi tiết |
|---|---|
| **Tên dự án** | AI Business Insight Dashboard (Vietnam-ready) |
| **Stack chính** | Python, Streamlit, Pandas, OpenAI API, ReportLab/FPDF |
| **Target user** | SME, E-commerce seller, Marketing team |
| **Thời gian dự kiến** | 4 tuần (28 ngày) |
| **Trạng thái** | 🟡 Đang lên kế hoạch |

---

## 🗓️ Timeline Tổng Thể

```
Tuần 1 (Day 1–7)   → PHASE 1: Foundation & Data Pipeline
Tuần 2 (Day 8–14)  → PHASE 2: Business Metrics & AI Engine
Tuần 3 (Day 15–21) → PHASE 3: Dashboard & Report Generator
Tuần 4 (Day 22–28) → PHASE 4: Polish, Testing & Demo
```

---

## 📌 PHASE 1 — Foundation & Data Pipeline
**⏱️ Timeline: Day 1 – 7 (Tuần 1)**
**🎯 Mục tiêu:** Dựng xong skeleton project + pipeline đọc & validate dữ liệu đầu vào.

### 1.1 Project Setup (Day 1)

- [ ] Tạo cấu trúc thư mục project
  ```
  report_generator/
  ├── app/
  │   ├── __init__.py
  │   ├── validator.py       # Data Validation Layer
  │   ├── processor.py       # Data Processing Layer
  │   ├── metrics.py         # Business Metrics Layer
  │   ├── ai_engine.py       # AI Insight Engine
  │   ├── visualizer.py      # Visualization Layer
  │   └── report.py          # Report Generator
  ├── dashboard/
  │   └── streamlit_app.py   # Streamlit UI
  ├── data/
  │   └── sample/            # Sample CSV/Excel files
  ├── output/
  │   └── reports/           # Generated PDFs
  ├── tests/
  │   └── test_*.py
  ├── .env                   # API keys
  ├── requirements.txt
  └── README.md
  ```
- [ ] Tạo `requirements.txt`
  ```
  streamlit
  pandas
  openpyxl
  openai
  reportlab
  matplotlib
  seaborn
  plotly
  python-dotenv
  ```
- [ ] Tạo `.env` template với `OPENAI_API_KEY`
- [ ] Init git repo, tạo `.gitignore`

---

### 1.2 Data Validation Layer (Day 2–3)

**File:** `app/validator.py`

#### Schema mong đợi (Expected Schema)

```json
{
  "date": "datetime",
  "product": "string",
  "revenue": "number",
  "orders": "number"
}
```

#### Auto Column Mapping

| Field chuẩn | Alias hỗ trợ |
|---|---|
| `date` | `ngày`, `created_at`, `order_date`, `thời gian` |
| `revenue` | `doanh thu`, `rev`, `total`, `amount`, `tiền` |
| `product` | `sản phẩm`, `item`, `product_name`, `tên sp` |
| `orders` | `đơn hàng`, `count`, `quantity`, `số đơn` |

#### Tasks

- [ ] Viết function `load_file(path)` — đọc CSV/Excel bằng pandas
- [ ] Viết function `detect_columns(df)` — auto mapping tên cột theo alias
- [ ] Viết function `ai_column_mapping(df, columns)` — gọi AI nếu không match alias
- [ ] Viết function `validate_schema(df)` — kiểm tra cột bắt buộc (`date`, `revenue`)
- [ ] Viết function `handle_missing_values(df)` — điền/xóa NaN theo rule
- [ ] Viết function `normalize_formats(df)` — chuẩn hóa date format, số (int/float)
- [ ] Viết unit test cho validator

---

### 1.3 Data Processing Layer (Day 4–5)

**File:** `app/processor.py`

- [ ] Viết function `compute_daily_revenue(df)` — doanh thu theo ngày
- [ ] Viết function `compute_top_products(df, n=10)` — top N sản phẩm
- [ ] Viết function `compute_revenue_growth(df)` — % tăng trưởng so với kỳ trước
- [ ] Viết function `compute_avg_order_value(df)` — giá trị đơn hàng trung bình
- [ ] Viết function `detect_anomalies(df)` — phát hiện ngày doanh thu bất thường (Z-score hoặc IQR)
- [ ] Viết unit test cho processor

---

### 1.4 Sample Data (Day 6–7)

- [ ] Tạo file `data/sample/ecommerce_sample.csv` (~500 rows, 3 tháng)
- [ ] Tạo file `data/sample/marketing_ads.csv` (chi phí ads, ROAS, CAC)
- [ ] Tạo file `data/sample/sme_weekly.csv` (báo cáo tuần SME)
- [ ] Test pipeline validator + processor với sample data
- [ ] Fix bug nếu có

---

### ✅ Phase 1 — Definition of Done

- [ ] Load được CSV/Excel ✓
- [ ] Auto mapping cột thành công với ≥ 3 alias ✓
- [ ] Validate schema và báo lỗi rõ ràng ✓
- [ ] Tính được daily revenue, top product, growth ✓
- [ ] Detect được anomaly (ngày doanh thu bất thường) ✓

---

## 📌 PHASE 2 — Business Metrics & AI Insight Engine
**⏱️ Timeline: Day 8 – 14 (Tuần 2)**
**🎯 Mục tiêu:** Hoàn thiện Business Metrics Layer + tích hợp OpenAI để sinh insight tiếng Việt.

### 2.1 Business Metrics Layer (Day 8–9)

**File:** `app/metrics.py`

- [x] Viết function `build_metrics_payload(df)` — tổng hợp tất cả metrics thành dict
- [x] Viết function `format_currency_vnd(value)` — format số tiền VND
- [x] Viết unit test cho metrics

---

### 2.2 AI Insight Engine (Day 10–12)

**File:** `app/ai_engine.py`

- [x] Setup OpenAI client với API key từ `.env`
- [x] Viết function `generate_insight(metrics: dict) -> dict` — gọi GPT-4o-mini
- [x] Thiết kế output schema (insights, warnings, recommendations)
- [x] Xử lý lỗi: rate limit, timeout, invalid API key

---

### 2.3 Integration Test (Day 13–14)

- [x] Test full pipeline: `load → validate → process → metrics → AI insight`
- [x] Đo thời gian chạy (target: < 30 giây end-to-end)
- [x] Xử lý edge case

**File:** `app/metrics.py`

Chuẩn hóa output thành structured JSON để feed cho AI:

```json
{
  "period": "2026-04-01 to 2026-04-30",
  "total_revenue": 125000000,
  "revenue_growth": -12.5,
  "top_product": "Áo thun basic",
  "top_product_share": 0.60,
  "worst_day": "2026-04-10",
  "worst_day_revenue": 800000,
  "avg_order_value": 120000,
  "total_orders": 1042,
  "anomaly_days": ["2026-04-10", "2026-04-23"],
  "anomaly_type": "drop"
}
```

- [ ] Viết function `build_metrics_payload(df)` — tổng hợp tất cả metrics thành dict
- [ ] Viết function `format_currency_vnd(value)` — format số tiền VND
- [ ] Viết function `compute_roas(df)` — (nếu có ads data)
- [ ] Viết function `compute_cac(df)` — (nếu có ads data)
- [ ] Viết unit test cho metrics

---

### 2.2 AI Insight Engine (Day 10–12)

**File:** `app/ai_engine.py`

#### Prompt Engineering (Tiếng Việt)

```
System: Bạn là chuyên gia phân tích dữ liệu kinh doanh cho doanh nghiệp Việt Nam.
Hãy phân tích các chỉ số sau và đưa ra:
1. INSIGHT chính (3-5 điểm quan trọng nhất)
2. CẢNH BÁO (rủi ro, bất thường cần chú ý)
3. ĐỀ XUẤT hành động cụ thể (ít nhất 3 đề xuất)

Viết bằng tiếng Việt, ngắn gọn, dễ hiểu cho chủ doanh nghiệp không phải kỹ thuật.
```

- [ ] Setup OpenAI client với API key từ `.env`
- [ ] Viết function `generate_insight(metrics: dict) -> dict` — gọi GPT-4o-mini
- [ ] Thiết kế output schema:
  ```json
  {
    "insights": ["...", "...", "..."],
    "warnings": ["...", "..."],
    "recommendations": ["...", "...", "..."],
    "summary": "Tổng quan một đoạn văn ngắn..."
  }
  ```
- [ ] Viết function `stream_insight(metrics)` — streaming output cho UX tốt hơn
- [ ] Xử lý lỗi: rate limit, timeout, invalid API key
- [ ] Viết mock function `mock_generate_insight()` để test không tốn token
- [ ] Test với 3 loại data (E-commerce, Ads, SME)

---

### 2.3 Integration Test (Day 13–14)

- [ ] Test full pipeline: `load → validate → process → metrics → AI insight`
- [ ] Đo thời gian chạy (target: < 30 giây end-to-end)
- [ ] Xử lý edge case:
  - [ ] File rỗng
  - [ ] Chỉ có 1 ngày dữ liệu
  - [ ] Revenue toàn bộ = 0
  - [ ] Ngày không đúng format
- [ ] Ghi log lỗi vào `app/logger.py`

---

### ✅ Phase 2 — Definition of Done

- [ ] Metrics payload đúng format JSON ✓
- [ ] AI trả về insight, warning, recommendation bằng tiếng Việt ✓
- [ ] Thời gian AI response < 10 giây ✓
- [ ] Xử lý được edge case không crash ✓

---

## 📌 PHASE 3 — Dashboard & Report Generator
**⏱️ Timeline: Day 15 – 21 (Tuần 3)**
**🎯 Mục tiêu:** Xây dựng Streamlit dashboard trực quan + xuất báo cáo PDF chuyên nghiệp.

### 3.1 Visualization Layer (Day 15–16)

**File:** `app/visualizer.py`

| Chart | Mô tả | Thư viện |
|---|---|---|
| Line chart | Doanh thu theo ngày (trend) | Plotly |
| Bar chart | Top 10 sản phẩm | Plotly |
| Pie chart | Tỷ trọng sản phẩm | Plotly |
| Heatmap | Doanh thu theo ngày/tuần | Plotly |
| KPI cards | Tổng doanh thu, tăng trưởng, AOV | Streamlit metric |

- [ ] Viết function `plot_daily_revenue(df)` — line chart doanh thu + anomaly markers
- [ ] Viết function `plot_top_products(df)` — horizontal bar chart
- [ ] Viết function `plot_revenue_pie(df)` — pie/donut chart
- [ ] Viết function `plot_heatmap(df)` — revenue heatmap
- [ ] Style đồng bộ: màu chính `#1a73e8`, font tiếng Việt hỗ trợ

---

### 3.2 Streamlit Dashboard (Day 17–19)

**File:** `dashboard/streamlit_app.py`

#### UI Flow

```
[1] Upload File
     ↓
[2] Auto Schema Detection (hiển thị mapping)
     ↓
[3] Click "Generate Report"
     ↓
[4] Loading spinner (processing...)
     ↓
[5] Dashboard hiển thị:
     ├── KPI Cards (Revenue, Growth, AOV, Orders)
     ├── Line chart (Daily Revenue)
     ├── Bar chart (Top Products)
     ├── AI Insight Panel (Insights / Warnings / Recommendations)
     └── Download Button (PDF / Markdown)
```

#### Streamlit Components

- [ ] **Sidebar:** Upload widget, config options (ngôn ngữ, loại báo cáo)
- [ ] **Header:** Logo, tên app, breadcrumb
- [ ] **KPI Row:** 4 metric cards — Tổng doanh thu | Tăng trưởng | AOV | Tổng đơn
- [ ] **Chart Section:** Tabs — `Xu hướng | Top sản phẩm | Phân tích chi tiết`
- [ ] **AI Insight Panel:**
  - Expandable section với icon
  - Hiển thị dạng bullet points màu sắc
  - Warning hiển thị màu đỏ/cam
  - Recommendation hiển thị màu xanh lá
- [ ] **Download Section:** Nút PDF + Markdown
- [ ] Xử lý state management (st.session_state)
- [ ] Loading spinner khi đang xử lý
- [ ] Error message user-friendly (không show stack trace)

---

### 3.3 Report Generator (Day 20–21)

**File:** `app/report.py`

#### PDF Report Structure

```
[Trang 1] Trang bìa
  - Logo, tên báo cáo
  - Kỳ báo cáo, ngày tạo

[Trang 2] Tổng quan (Executive Summary)
  - KPI chính (4 cards)
  - Đoạn tóm tắt AI

[Trang 3] Xu hướng doanh thu
  - Line chart (export từ Plotly)
  - Nhận xét tự động

[Trang 4] Phân tích sản phẩm
  - Bar chart top sản phẩm
  - Bảng chi tiết top 10

[Trang 5] AI Insights
  - Insights chính
  - Cảnh báo
  - Đề xuất hành động

[Trang 6] Phụ lục
  - Raw data summary
  - Metadata
```

- [ ] Viết function `export_pdf(metrics, charts, insights)` — dùng ReportLab
- [ ] Hỗ trợ font tiếng Việt trong PDF (embed font NotoSans)
- [ ] Viết function `export_markdown(metrics, insights)` — Markdown report
- [ ] Test PDF render đúng trên Windows + MacOS
- [ ] File PDF < 5MB

---

### ✅ Phase 3 — Definition of Done

- [ ] Dashboard chạy được bằng `streamlit run dashboard/streamlit_app.py` ✓
- [ ] Upload file → Generate report trong < 60 giây ✓
- [ ] 4 KPI cards hiển thị đúng ✓
- [ ] 3+ charts render đúng dữ liệu ✓
- [ ] AI insight hiển thị có cấu trúc rõ ràng ✓
- [ ] Xuất được PDF với tiếng Việt không bị lỗi font ✓

---

## 📌 PHASE 4 — Polish, Testing & Demo
**⏱️ Timeline: Day 22 – 28 (Tuần 4)**
**🎯 Mục tiêu:** Hoàn thiện, test toàn diện, chuẩn bị demo phỏng vấn.

### 4.1 Testing & Bug Fix (Day 22–24)

- [ ] **Unit Tests:** Chạy `pytest tests/` — coverage ≥ 70%
- [ ] **Integration Tests:**
  - [ ] Test với file E-commerce (Shopee style)
  - [ ] Test với file Marketing Ads (Facebook/Google)
  - [ ] Test với file SME weekly
- [ ] **Performance Test:** Đo thời gian với file 10k rows
- [ ] **Edge Cases:**
  - [ ] File Excel với multiple sheets
  - [ ] File có header ở row 2 (không phải row 1)
  - [ ] Revenue chứa ký tự "₫" hoặc dấu phẩy
  - [ ] Ngày dạng dd/mm/yyyy vs yyyy-mm-dd
- [ ] Fix tất cả bug critical
- [ ] Code review, clean up dead code

---

### 4.2 UX Polish (Day 25–26)

- [ ] Thêm tooltip giải thích các chỉ số (ROAS là gì, AOV là gì)
- [ ] Responsive layout trên màn hình nhỏ
- [ ] Dark mode (tùy chọn)
- [ ] Thêm progress bar khi generating report
- [ ] Hiển thị thời gian xử lý sau khi xong
- [ ] Thêm "Copy to Clipboard" cho AI insight
- [ ] Cải thiện error messages (tiếng Việt, thân thiện)
- [ ] Thêm favicon và page title

---

### 4.3 Documentation (Day 27)

- [ ] Cập nhật `README.md`:
  - [ ] Mô tả dự án + screenshot
  - [ ] Hướng dẫn cài đặt (3 bước đơn giản)
  - [ ] Hướng dẫn sử dụng
  - [ ] FAQ
- [ ] Viết docstring cho tất cả public functions
- [ ] Tạo `ARCHITECTURE.md` — mô tả kiến trúc hệ thống
- [ ] Tạo `DEMO.md` — script demo phỏng vấn

---

### 4.4 Demo Preparation (Day 28)

**Kịch bản demo phỏng vấn:**

```
[Bước 1] Giới thiệu bài toán (30 giây)
  "Doanh nghiệp mất 2-3 giờ làm báo cáo mỗi tuần.
   Tôi xây hệ thống giảm xuống còn < 1 phút."

[Bước 2] Demo live (2-3 phút)
  - Upload file dữ liệu bán hàng (ecommerce_sample.csv)
  - Click "Generate Report"
  - Chờ 20-30 giây
  - Chỉ vào KPI: "Doanh thu tháng này giảm 12.5%"
  - Chỉ vào chart: "Ngày 10/4 doanh thu giảm mạnh bất thường"
  - Đọc AI insight: "Sản phẩm Áo thun chiếm 60% doanh thu"
  - Download PDF

[Bước 3] Giải thích kiến trúc (1-2 phút)
  - Vẽ sơ đồ pipeline: Upload → Validate → Process → AI → Report
  - Nhấn mạnh: auto column mapping, AI insight tiếng Việt
```

- [ ] Chuẩn bị 3 file demo data (hấp dẫn, có story rõ ràng)
- [ ] Test demo flow 3 lần không có bug
- [ ] Chuẩn bị câu trả lời cho câu hỏi kỹ thuật:
  - [ ] "Tại sao dùng Streamlit mà không dùng FastAPI + React?"
  - [ ] "Xử lý dữ liệu lớn như thế nào?"
  - [ ] "Mở rộng multi-user thì làm gì?"
  - [ ] "Chi phí API OpenAI mỗi báo cáo là bao nhiêu?"
- [ ] Đẩy code lên GitHub, public repo

---

### ✅ Phase 4 — Definition of Done

- [ ] Không có bug critical khi demo ✓
- [ ] README đầy đủ với screenshot ✓
- [ ] Demo flow chạy mượt trong < 60 giây ✓
- [ ] Code pushed lên GitHub ✓

---

## 📐 Kiến trúc Hệ thống

```
                    ┌─────────────────────────────────────┐
                    │         Streamlit Dashboard          │
                    │  (Upload / Visualize / Download)    │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │        Data Validation Layer         │
                    │  (Schema check / Column mapping /    │
                    │   Missing value / Format normalize)  │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │        Data Processing Layer         │
                    │  (Pandas: Revenue / Growth /         │
                    │   Top products / Anomaly detect)    │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │       Business Metrics Layer         │
                    │  (Structured JSON payload)           │
                    └──────┬───────────────────────┬──────┘
                           │                       │
           ┌───────────────▼───┐         ┌─────────▼──────────────┐
           │  AI Insight Engine │         │   Visualization Layer   │
           │  (OpenAI GPT-4o)  │         │  (Plotly: line, bar,   │
           │  Insight/Warning/  │         │   pie, heatmap)        │
           │  Recommendation   │         └─────────┬──────────────┘
           └───────────────┬───┘                   │
                           └──────────┬────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │          Report Generator            │
                    │       (PDF / Markdown export)        │
                    └─────────────────────────────────────┘
```

---

## 📊 KPI Dự án

| Chỉ số | Baseline | Target | Đo bằng |
|---|---|---|---|
| Thời gian làm báo cáo | 2–3 giờ | < 1 phút | Stopwatch demo |
| Tỷ lệ tự động hóa | 0% | 80–90% | % bước thủ công |
| Phát hiện anomaly | Không có | 100% anomaly tìm thấy | Test với data có sẵn |
| Lỗi thủ công | Nhiều | ~0 | Manual review |
| Thời gian AI response | N/A | < 10 giây | Code timer |
| PDF export | N/A | < 5MB | File size check |

---

## 🚀 Hướng Mở Rộng (Future Roadmap)

### V2 — Short-term (1-2 tháng sau MVP)
- [ ] **Chat với dữ liệu** — Hỏi đáp tự nhiên qua chatbot (LangChain + RAG)
- [ ] **Lưu lịch sử báo cáo** — Database SQLite/PostgreSQL
- [ ] **Email alert** — Tự động gửi cảnh báo khi phát hiện anomaly

### V3 — Mid-term (3-6 tháng)
- [ ] **Multi-user** — Authentication, per-user data isolation
- [ ] **API endpoint** — FastAPI wrapper để tích hợp vào hệ thống khác
- [ ] **Scheduled reports** — Cron job tự động tạo báo cáo định kỳ
- [ ] **Connectors** — Kết nối trực tiếp Shopee API, Google Ads API

### V4 — Long-term
- [ ] **SaaS model** — Multi-tenant, subscription billing
- [ ] **Custom branding** — White-label cho đại lý
- [ ] **Mobile app** — React Native companion app

---

## 🛠️ Tech Stack Chi Tiết

| Layer | Công nghệ | Lý do chọn |
|---|---|---|
| Frontend/UI | Streamlit | Nhanh, đẹp, không cần JS |
| Data processing | Pandas, NumPy | Chuẩn công nghiệp |
| AI Engine | OpenAI GPT-4o-mini | Rẻ (~$0.01/báo cáo), tiếng Việt tốt |
| Visualization | Plotly | Interactive, đẹp, xuất ảnh dễ |
| PDF export | ReportLab | Hỗ trợ font Unicode/VN tốt |
| Testing | Pytest | Chuẩn Python |
| Version control | Git + GitHub | Chuẩn công nghiệp |

---

## 💼 CV Highlights (Sau khi xong dự án)

```
AI Business Insight Dashboard | Python, Streamlit, OpenAI, Pandas
• Xây dựng hệ thống AI tự động phân tích dữ liệu kinh doanh và tạo báo cáo
  thông minh, hỗ trợ E-commerce, Marketing Ads và SME tại Việt Nam
• Thiết kế pipeline 6 layers: Validation → Processing → Metrics → AI Insight
  → Visualization → PDF Report với xử lý edge case đầy đủ
• Tích hợp OpenAI GPT-4o-mini với prompt tiếng Việt, sinh insight/cảnh báo/
  đề xuất tự động, giảm thời gian làm báo cáo từ 2-3 giờ xuống < 1 phút (~95%)
• Implement auto column mapping (hỗ trợ tiếng Việt/Anh), anomaly detection
  bằng Z-score, xuất PDF đa trang với font Unicode
```

---

*📅 Tạo lúc: 2026-04-30 | Cập nhật lần cuối: 2026-04-30*
