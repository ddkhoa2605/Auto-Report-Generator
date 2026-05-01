from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import urllib.request

def _ensure_font_exists():
    """Sử dụng trực tiếp font Arial có sẵn trên Windows để hỗ trợ Tiếng Việt."""
    regular_path = r"C:\Windows\Fonts\arial.ttf"
    bold_path = r"C:\Windows\Fonts\arialbd.ttf"
    
    if not os.path.exists(regular_path) or not os.path.exists(bold_path):
        print("CẢNH BÁO: Không tìm thấy font Arial trong hệ thống. Tiếng Việt có thể bị lỗi.")
        return
        
    # Đăng ký font với ReportLab
    pdfmetrics.registerFont(TTFont('Arial', regular_path))
    pdfmetrics.registerFont(TTFont('Arial-Bold', bold_path))
    
    # Đăng ký Family để hỗ trợ thẻ <b>
    pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold')

def generate_pdf_report(metrics_payload, ai_insights, output_path):
    """Tạo báo cáo PDF chuyên nghiệp với font tiếng Việt."""
    
    _ensure_font_exists()
    
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Tạo style tùy chỉnh sử dụng font Arial
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Arial-Bold',
        fontSize=24,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontName='Arial-Bold',
        fontSize=18,
        textColor=colors.HexColor("#D97706"),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontName='Arial',
        fontSize=12,
        leading=18 # Tăng khoảng cách dòng cho dễ đọc
    )

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
        ["Tăng trưởng doanh thu", f"{metrics_payload['growth_and_trend']['revenue_growth_rate']}%"]
    ]
    
    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'), # Dùng font Bold cho Header
        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),      # Dùng font thường cho nội dung
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    # 3. Phân tích từ AI
    elements.append(Paragraph("2. Phân tích chuyên sâu từ AI", section_style))
    elements.append(Paragraph("<b>Tóm tắt:</b>", body_style))
    elements.append(Paragraph(str(ai_insights.get('summary', 'N/A')), body_style))
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
