import streamlit as st
import pandas as pd
from app.validator import validate_pipeline
from app.metrics import build_metrics_payload, format_currency_vnd
from app.visualizer import plot_revenue_trend, plot_top_products, plot_product_pie
from app.ai_engine import generate_insight
from app.reporter import generate_pdf_report
import os

# Cấu hình trang
st.set_page_config(
    page_title="AI Business Insight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS cho giao diện Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    /* Glassmorphism cho Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .metric-label {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 5px;
    }
    
    /* Gradient Sidebar */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
    }
    
    /* Header AI */
    .ai-header {
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1693/1693746.png", width=80)
    st.title("Phân Tích Kinh Doanh")
    uploaded_file = st.file_uploader("Tải lên file báo cáo (CSV/Excel)", type=["csv", "xlsx"])
    
    st.markdown("---")
    st.info("Hệ thống sử dụng Gemini 2.0 Flash để phân tích chuyên sâu.")
    
    if st.button("Reset Dữ Liệu"):
        st.rerun()

# Nội dung chính
st.title("🚀 AI Business Insight Dashboard")
st.markdown("Chuyển đổi dữ liệu thô thành chiến lược kinh doanh thông minh.")

if uploaded_file is not None:
    try:
        # 1. Xử lý dữ liệu
        with st.spinner("Đang xử lý dữ liệu..."):
            # Lưu tạm file
            temp_path = f"data/temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            df = validate_pipeline(temp_path)
            metrics = build_metrics_payload(df)
            
            # Xóa file tạm
            os.remove(temp_path)

        # 2. Hiển thị Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>Tổng Doanh Thu</div><div class='metric-value'>{format_currency_vnd(metrics['summary']['total_revenue'])}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>Số Đơn Hàng</div><div class='metric-value'>{metrics['summary']['total_orders']}</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>Giá Trị Trung Bình</div><div class='metric-value'>{format_currency_vnd(metrics['summary']['avg_order_value'])}</div></div>""", unsafe_allow_html=True)
        with col4:
            growth_color = "green" if metrics['summary']['revenue_growth_percent'] >= 0 else "red"
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>Tăng Trưởng</div><div class='metric-value' style='color:{growth_color}'>{metrics['summary']['revenue_growth_percent']}%</div></div>""", unsafe_allow_html=True)

        st.markdown("---")

        # 3. Biểu đồ & AI Insight
        tab1, tab2 = st.tabs(["📊 Phân Tích Xu Hướng", "🧠 Nhận Xét Từ AI"])

        with tab1:
            c1, c2 = st.columns([2, 1])
            with c1:
                # Lấy anomalies để vẽ
                daily_rev = df.groupby('date')['revenue'].sum().reset_index()
                from app.processor import detect_anomalies
                anomalies = detect_anomalies(df)
                st.plotly_chart(plot_revenue_trend(daily_rev, anomalies), use_container_width=True)
            with c2:
                top_products_data = pd.DataFrame(metrics['top_products'])
                if not top_products_data.empty:
                    top_products_data = top_products_data.rename(columns={'name': 'product'})
                    fig_pie = plot_product_pie(top_products_data)
                    if fig_pie:
                        st.plotly_chart(fig_pie, use_container_width=True)

            if not pd.DataFrame(metrics['top_products']).empty:
                fig_bar = plot_top_products(pd.DataFrame(metrics['top_products']).rename(columns={'name': 'product'}))
                if fig_bar:
                    st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            st.markdown("<div class='ai-header'>🤖 AI Consultant Insight</div>", unsafe_allow_html=True)
            
            with st.spinner("Gemini đang suy nghĩ..."):
                ai_report = generate_insight(metrics)
                
                st.subheader("📝 Tóm tắt")
                st.write(ai_report['summary'])
                
                c_insight, c_warn = st.columns(2)
                with c_insight:
                    st.success("💡 Điểm sáng")
                    for item in ai_report['insights']:
                        st.write(f"- {item}")
                
                with c_warn:
                    st.warning("⚠️ Lưu ý & Rủi ro")
                    for item in ai_report['warnings']:
                        st.write(f"- {item}")
                
                st.subheader("🎯 Đề xuất hành động")
                for item in ai_report['recommendations']:
                    st.info(item)
                
                # Nút xuất PDF
                st.markdown("---")
                pdf_filename = f"report_{uploaded_file.name.split('.')[0]}.pdf"
                pdf_path = f"output/reports/{pdf_filename}"
                
                os.makedirs("output/reports", exist_ok=True)
                
                if st.button("📄 Tạo Báo Cáo PDF"):
                    with st.spinner("Đang khởi tạo PDF..."):
                        generate_pdf_report(metrics, ai_report, pdf_path)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Tải xuống Báo Cáo PDF",
                                data=f,
                                file_name=pdf_filename,
                                mime="application/pdf"
                            )

    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi xử lý dữ liệu: {e}")
else:
    # Màn hình chờ
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-804.jpg", width=400)
    st.info("Vui lòng tải lên file dữ liệu ở thanh bên trái để bắt đầu phân tích.")
