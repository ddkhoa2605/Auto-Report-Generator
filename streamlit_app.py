import streamlit as st
import pandas as pd
from app.validator import validate_pipeline
from app.metrics import build_metrics_payload, format_currency_vnd
from app.visualizer import plot_revenue_trend, plot_top_products, plot_product_pie
from app.ai_engine import generate_insight
from app.reporter import generate_pdf_report
import os

# ─── Cấu hình trang ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Doanh Nghiệp ─────────────────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    :root {
        --bg:          #F4F5F7;
        --surface:     #FFFFFF;
        --border:      #E2E4E9;
        --text-primary: #0D1117;
        --text-muted:  #6B7280;
        --accent:      #1B4FD8;
        --accent-light:#EEF2FF;
        --positive:    #16A34A;
        --negative:    #DC2626;
        --mono:        'DM Mono', monospace;
    }

    html, body, [class*="css"], .stApp, .main {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebarNav"] { display: none; }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 0 20px;
    }
    .sidebar-logo-mark {
        width: 32px; height: 32px;
        background: var(--accent);
        border-radius: 6px;
        display: inline-block;
    }
    .sidebar-logo-text {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.3px;
    }
    .sidebar-section {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 20px 0 8px;
    }

    /* ── Page Header ── */
    .page-header {
        padding: 8px 0 24px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 28px;
    }
    .page-title {
        font-size: 22px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.4px;
        margin: 0;
    }
    .page-subtitle {
        font-size: 14px;
        color: var(--text-muted);
        margin: 4px 0 0;
    }

    /* ── KPI Cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 20px 22px;
        min-height: 125px; /* Ép các thẻ luôn bằng nhau */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 14px; /* Tăng từ 12px -> 14px */
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 28px; /* Tăng từ 26px -> 28px */
        font-weight: 700;
        color: var(--text-primary);
        font-family: var(--mono);
        letter-spacing: -0.5px;
        line-height: 1.2; /* Thu gọn khoảng cách khi rớt dòng */
        white-space: nowrap; /* Cấm rớt dòng ngẫu nhiên */
    }
    .kpi-value.positive { color: var(--positive); }
    .kpi-value.negative { color: var(--negative); }

    /* ── Section Headers ── */
    .section-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.2px;
        margin: 0 0 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }

    /* ── AI Panel ── */
    .ai-insight-label {
        display: inline-block;
        background: var(--accent-light);
        color: var(--accent);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 4px;
        margin-bottom: 14px;
    }
    .insight-block {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    .insight-block-title {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 10px;
    }
    .insight-block.highlight { border-left: 3px solid var(--accent); }
    .insight-block.warn      { border-left: 3px solid #F59E0B; }

    /* ── Divider ── */
    hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

    /* ── Buttons ── */
    .stButton > button {
        background-color: var(--accent);
        color: #fff;
        border: none;
        border-radius: 7px;
        font-size: 13px;
        font-weight: 500;
        padding: 8px 18px;
        letter-spacing: 0.01em;
        transition: opacity 0.15s;
    }
    .stButton > button:hover { opacity: 0.88; }

    /* ── Tab styling ── */
    [data-baseweb="tab-list"] {
        border-bottom: 1px solid var(--border);
        gap: 0;
    }
    [data-baseweb="tab"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        padding: 10px 18px !important;
        border-bottom: 2px solid transparent !important;
    }
    [aria-selected="true"][data-baseweb="tab"] {
        color: var(--accent) !important;
        border-bottom-color: var(--accent) !important;
    }
    </style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            <span class="sidebar-logo-mark"></span>
            <span class="sidebar-logo-text">BI Dashboard</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Nguồn dữ liệu</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Tải lên báo cáo",
        type=["csv", "xlsx"],
        label_visibility="collapsed",
        help="Hỗ trợ định dạng CSV và Excel (.xlsx)"
    )

    st.markdown('<div class="sidebar-section">Hành động</div>', unsafe_allow_html=True)
    if st.button("Làm mới", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("Phân tích được hỗ trợ bởi Coze AI · Dữ liệu không được lưu trữ.")


# ─── Tiêu đề trang ────────────────────────────────────────────────────────────
st.markdown("""
    <div class="page-header">
        <div class="page-title">Phân Tích Kinh Doanh</div>
        <div class="page-subtitle">Tổng quan hiệu suất doanh thu và phân tích chiến lược</div>
    </div>
""", unsafe_allow_html=True)


# ─── Nội dung chính ───────────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        with st.spinner("Đang xử lý dữ liệu..."):
            temp_path = f"data/temp_{uploaded_file.name}"
            os.makedirs("data", exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            df = validate_pipeline(temp_path)
            metrics = build_metrics_payload(df)
            os.remove(temp_path)

        # ── KPI Cards ─────────────────────────────────────────────────────────
        growth_rate = metrics.get('growth_and_trend', {}).get('revenue_growth_rate', 0)
        growth_class = "positive" if growth_rate >= 0 else "negative"
        growth_sign  = "+" if growth_rate >= 0 else ""

        col1, col2, col3, col4 = st.columns(4)
        kpi_items = [
            (col1, "Tổng Doanh Thu",    format_currency_vnd(metrics['summary']['total_revenue']), ""),
            (col2, "Số Đơn Hàng",        f"{metrics['summary']['total_orders']:,}",                ""),
            (col3, "Giá Trị Trung Bình", format_currency_vnd(metrics['summary']['avg_order_value']), ""),
            (col4, "Tăng Trưởng",        f"{growth_sign}{growth_rate}%",                            growth_class),
        ]
        for col, label, value, cls in kpi_items:
            with col:
                st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value {cls}">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Tabs ──────────────────────────────────────────────────────────────
        tab1, tab2 = st.tabs(["Xu Hướng & Phân Phối", "Phân Tích AI"])

        # Tab 1 — Biểu đồ
        with tab1:
            st.markdown('<div class="section-title">Doanh thu theo thời gian</div>', unsafe_allow_html=True)
            c1, c2 = st.columns([2, 1])
            with c1:
                daily_rev = df.groupby('date')['revenue'].sum().reset_index()
                from app.processor import detect_anomalies
                anomalies = detect_anomalies(df)
                st.plotly_chart(plot_revenue_trend(daily_rev, anomalies), use_container_width=True)
            with c2:
                top_products_data = pd.DataFrame(metrics.get('distribution', {}).get('top_products', []))
                if not top_products_data.empty:
                    top_products_data = top_products_data.rename(columns={'name': 'product'})
                    fig_pie = plot_product_pie(top_products_data)
                    if fig_pie:
                        st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown('<div class="section-title">Sản phẩm hàng đầu</div>', unsafe_allow_html=True)
            top_df = pd.DataFrame(metrics.get('distribution', {}).get('top_products', []))
            if not top_df.empty:
                fig_bar = plot_top_products(top_df.rename(columns={'name': 'product'}))
                if fig_bar:
                    st.plotly_chart(fig_bar, use_container_width=True)

        # Tab 2 — AI Insight
        with tab2:
            st.markdown('<span class="ai-insight-label">AI Consultant</span>', unsafe_allow_html=True)

            with st.spinner("Đang phân tích..."):
                ai_report = generate_insight(metrics)

            st.markdown('<div class="section-title">Tóm tắt</div>', unsafe_allow_html=True)
            st.markdown(f"""<div class="insight-block">{ai_report['summary']}</div>""", unsafe_allow_html=True)

            c_insight, c_warn = st.columns(2)
            with c_insight:
                items_html = "".join(f"<p style='margin:6px 0;font-size:14px;'>— {item}</p>" for item in ai_report['insights'])
                st.markdown(f"""
                    <div class="insight-block highlight">
                        <div class="insight-block-title">Điểm tích cực</div>
                        {items_html}
                    </div>
                """, unsafe_allow_html=True)
            with c_warn:
                items_html = "".join(f"<p style='margin:6px 0;font-size:14px;'>— {item}</p>" for item in ai_report['warnings'])
                st.markdown(f"""
                    <div class="insight-block warn">
                        <div class="insight-block-title">Lưu ý & Rủi ro</div>
                        {items_html}
                    </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-title" style="margin-top:20px;">Khuyến nghị hành động</div>', unsafe_allow_html=True)
            for i, item in enumerate(ai_report['recommendations'], 1):
                st.markdown(f"""
                    <div class="insight-block" style="display:flex;gap:14px;align-items:flex-start;">
                        <span style="font-family:var(--mono);font-size:12px;color:var(--accent);font-weight:600;padding-top:2px;min-width:20px;">{i:02d}</span>
                        <span style="font-size:14px;">{item}</span>
                    </div>
                """, unsafe_allow_html=True)

            # Xuất PDF
            st.markdown("<hr>", unsafe_allow_html=True)
            pdf_filename = f"report_{uploaded_file.name.rsplit('.', 1)[0]}.pdf"
            pdf_path     = f"output/reports/{pdf_filename}"
            os.makedirs("output/reports", exist_ok=True)

            if st.button("Tạo báo cáo PDF"):
                with st.spinner("Đang tạo PDF..."):
                    generate_pdf_report(metrics, ai_report, pdf_path)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Tải xuống báo cáo",
                            data=f,
                            file_name=pdf_filename,
                            mime="application/pdf",
                        )

    except Exception as e:
        st.error(f"Lỗi xử lý dữ liệu: {e}")

else:
    # ── Trạng thái rỗng ───────────────────────────────────────────────────────
    st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 80px 20px;
            border: 1px dashed #D1D5DB;
            border-radius: 12px;
            background: #fff;
            text-align: center;
        ">
            <div style="
                width: 48px; height: 48px;
                background: #EEF2FF;
                border-radius: 10px;
                display: flex; align-items: center; justify-content: center;
                margin-bottom: 18px;
                font-size: 22px;
            ">&#128202;</div>
            <div style="font-size:16px;font-weight:600;color:#0D1117;margin-bottom:8px;">
                Chưa có dữ liệu
            </div>
            <div style="font-size:14px;color:#6B7280;max-width:340px;line-height:1.6;">
                Tải lên file CSV hoặc Excel từ thanh bên trái để bắt đầu phân tích.
                Hệ thống sẽ tự động tính toán các chỉ số và tạo báo cáo AI.
            </div>
        </div>
    """, unsafe_allow_html=True)
