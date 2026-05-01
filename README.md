# 📊 AI Business Insight Dashboard

![Dashboard Overview](assets/dashboard_overview.png) *(Insert dashboard screenshot here)*

An enterprise-grade Business Intelligence (BI) dashboard powered by AI. This system ingests raw e-commerce sales data (CSV/Excel), sanitizes it, computes deep business metrics (AOV, Growth Rates, Anomaly Detection), and uses **Coze AI (Claude/GPT-4o)** to act as an automated business analyst, delivering actionable insights and generating PDF reports.

## ✨ Features

- **Automated Data Pipeline**: Robustly handles messy Excel/CSV files, cleaning `revenue` and `orders` data using RegEx.
- **Deep Metrics Calculation**: Computes Growth Rates (MoM), Average Order Value (AOV), Revenue per Order, and Z-Score based daily anomaly detection.
- **Enterprise SaaS UI**: A clean, responsive, and highly professional Dashboard built with Streamlit using custom CSS (Light Mode forced, DM Sans/Mono fonts).
- **AI Business Consultant**: Integrates with Coze API to parse numerical data and generate human-readable insights (Summaries, Highlights, Risks, and Priority-based Recommendations).
- **Smart Text Parser**: Fault-tolerant AI integration that can parse plain text into JSON structures if the AI model drops format constraints.
- **Automated PDF Reporting**: Generates localized (Vietnamese-supported) PDF reports using embedded Arial fonts.

## 📸 Screenshots

### 1. KPI & Trend Analysis
![KPI and Charts](assets/kpi_charts.png) *(Insert KPI and Chart screenshot here)*

### 2. AI Consultant Insights
![AI Insights](assets/ai_insights.png) *(Insert AI Consultant screenshot here)*

## 🛠️ Technology Stack

- **Frontend/UI**: Streamlit (with custom Enterprise CSS & Plotly for charts)
- **Data Processing**: Pandas, NumPy
- **AI Integration**: Coze API (`requests`), Custom Text-to-JSON Parser
- **PDF Generation**: ReportLab (Embedded System Arial Font)

## 📁 Project Structure

```text
📦 AI_Business_Dashboard
 ┣ 📂 app/
 ┃ ┣ 📜 ai_engine.py      # Coze API integration & Text Parser
 ┃ ┣ 📜 metrics.py        # Compiles deep metrics payload for AI
 ┃ ┣ 📜 processor.py      # Calculations (Z-Score, AOV, Growth)
 ┃ ┣ 📜 reporter.py       # PDF generation with Vietnamese support
 ┃ ┣ 📜 validator.py      # Data cleaning & sanitization pipeline
 ┃ ┗ 📜 visualizer.py     # Plotly chart generation
 ┣ 📂 .streamlit/
 ┃ ┗ 📜 config.toml       # Streamlit Light theme enforcement
 ┣ 📜 streamlit_app.py    # Main UI Dashboard
 ┣ 📜 requirements.txt    # Python dependencies
 ┣ 📜 .env                # Environment variables (API Keys)
 ┗ 📜 README.md
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ddkhoa2605/Report_generator.git
cd Report_generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory and configure your Coze API bot:
```env
COZE_API_KEY="your_personal_access_token_here"
COZE_BOT_ID="your_published_bot_id_here"
```

### 4. Run the Dashboard
```bash
streamlit run streamlit_app.py
```
*(The dashboard will automatically open at `http://localhost:8501`)*

## 🤖 Coze Bot Setup Guide
To make the AI work flawlessly, ensure your Coze bot uses the following System Prompt:
```text
Bạn là chuyên gia phân tích kinh doanh tại Việt Nam.
Dựa trên dữ liệu metrics được cung cấp dạng JSON, hãy:
- Viết 1 câu tóm tắt
- Phát hiện các điểm sáng (Insights)
- Chỉ ra rủi ro/vấn đề (Warnings)
- Đưa ra đề xuất hành động (Recommendations)
Không giải thích thêm.
```

## 📄 License
This project is for educational and portfolio demonstration purposes.

---
**Created by**: Khoa (ddkhoa2605)
