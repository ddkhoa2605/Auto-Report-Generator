from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def generate_pdf_report(metrics_payload, ai_insights, output_path):
    """Tạo báo cáo PDF chuyên nghiệp từ dữ liệu và nhận xét AI."""
    
    # Cấu hình tài liệu
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Tạo style tùy chỉnh (sử dụng font mặc định có hỗ trợ Unicode trên Windows nếu cần)
    # Lưu ý: Trong môi trường production thực tế, nên tải font .ttf cụ thể.
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.hexColor("#1E3A8A"),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.hexColor("#D97706"),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = styles['BodyText']
    body_style.fontSize = 12
    body_style.leading = 14

    elements = []

    # 1. Tiêu đề
    elements.append(Paragraph("BÁO CÁO PHÂN TÍCH KINH DOANH AI", title_style))
    elements.append(Paragraph(f"Khoảng thời gian: {metrics_payload['summary']['period']}", body_style))
    elements.append(Spacer(1, 20))

    # 2. Bảng chỉ số chính
    elements.append(Paragraph("1. Chỉ số hiệu suất chính (KPIs)", section_style))
    data = [
        ["Chỉ số", "Giá trị"],
        ["Tổng doanh thu", f"{metrics_payload['summary']['total_revenue']:,.0f} VNĐ"],
        ["Tổng đơn hàng", str(metrics_payload['summary']['total_orders'])],
        ["Giá trị trung bình đơn", f"{metrics_payload['summary']['avg_order_value']:,.0f} VNĐ"],
        ["Tăng trưởng doanh thu", f"{metrics_payload['summary']['revenue_growth_percent']}%"]
    ]
    
    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.hexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    # 3. Phân tích từ AI
    elements.append(Paragraph("2. Phân tích chuyên sâu từ AI", section_style))
    elements.append(Paragraph("<b>Tóm tắt:</b>", body_style))
    elements.append(Paragraph(ai_insights.get('summary', 'N/A'), body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Điểm sáng & Cảnh báo:</b>", body_style))
    for insight in ai_insights.get('insights', []):
        elements.append(Paragraph(f"• {insight}", body_style))
    for warn in ai_insights.get('warnings', []):
        elements.append(Paragraph(f"• [Cảnh báo] {warn}", body_style))
    
    elements.append(Spacer(1, 20))

    # 4. Đề xuất
    elements.append(Paragraph("3. Chiến lược & Đề xuất", section_style))
    for rec in ai_insights.get('recommendations', []):
        elements.append(Paragraph(f"- {rec}", body_style))

    # Xây dựng PDF
    doc.build(elements)
    return output_path
