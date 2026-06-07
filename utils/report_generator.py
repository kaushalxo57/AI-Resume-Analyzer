import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(data: dict) -> bytes:
    """
    Generates a beautifully styled, high-end PDF report matching the
    Japanese Cyber Minimalist branding (Black/Red/White/Gray).
    Returns the PDF bytes for download.
    """
    pdf_buffer = io.BytesIO()
    
    # 0.5 inch margins for a modern, compact, editorial grid
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom colors
    COLOR_BLACK = colors.HexColor("#000000")
    COLOR_RED = colors.HexColor("#FF3B30")
    COLOR_GRAY = colors.HexColor("#2C2C2E")
    COLOR_MUTED = colors.HexColor("#71717A")
    COLOR_LIGHT_GRAY = colors.HexColor("#F2F2F7")
    
    # Custom Typography styles
    style_h1 = ParagraphStyle(
        name='CyberH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=30,
        textColor=COLOR_BLACK,
        spaceAfter=4,
        letterSpacing=-0.5
    )
    
    style_h2 = ParagraphStyle(
        name='CyberH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_BLACK,
        spaceBefore=14,
        spaceAfter=6,
        textTransform='uppercase',
        letterSpacing=1
    )
    
    style_body = ParagraphStyle(
        name='CyberBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_GRAY
    )
    
    style_bullet = ParagraphStyle(
        name='CyberBullet',
        parent=style_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    style_tag = ParagraphStyle(
        name='CyberTag',
        parent=style_body,
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_MUTED
    )
    
    story = []
    
    # --- HEADER SECTION ---
    # Draw a thin red accent border at the very top
    title_text = "<b>AI RESUME AUDIT</b>"
    subtitle_text = "ATS COMPATIBILITY & ALIGNMENT ANALYSIS | レジュメ分析"
    
    story.append(Paragraph(title_text, style_h1))
    story.append(Paragraph(subtitle_text, style_tag))
    story.append(Spacer(1, 10))
    
    # Red accent separator line (using a thin Table)
    sep = Table([['']], colWidths=[doc.width], rowHeights=[2])
    sep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_RED),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sep)
    story.append(Spacer(1, 15))
    
    # --- CORE METRICS SECTION ---
    # Layout Score & Health in a clean side-by-side Table
    metrics_data = [
        [
            Paragraph(f"<font size=8 color='#71717A'>ATS MATCH SCORE</font><br/><font size=30 color='#FF3B30'><b>{data.get('score', 0)}%</b></font><br/><font size=10 color='#000000'><b>{data.get('classification', 'Average').upper()} MATCH</b></font>", style_body),
            Paragraph(f"<font size=8 color='#71717A'>RESUME HEALTH INDEX</font><br/><font size=30 color='#000000'><b>{data.get('health_analysis', {}).get('health_score', 0)}/100</b></font><br/><font size=10 color='#000000'><b>{data.get('health_analysis', {}).get('health_label', 'Good').upper()} STATUS</b></font>", style_body)
        ]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[doc.width/2.0, doc.width/2.0])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_GRAY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 16),
        ('LINEBEFORE', (1,0), (1,0), 1, COLOR_MUTED), # divider line
        ('TOPPADDING', (0,0), (-1,-1), 20),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # --- ROLE PREDICTION & SUMMARY ---
    role_info = data.get('role_predictions', {})
    best_role = role_info.get('best_match', 'N/A')
    alt_roles = ", ".join(role_info.get('alternative_matches', []))
    
    role_summary_text = f"<b>Target Best Match:</b> {best_role} | <b>Alternative Matches:</b> {alt_roles}"
    story.append(Paragraph(role_summary_text, style_body))
    story.append(Spacer(1, 15))
    
    # --- TWO-COLUMN SKILLS & KEYWORDS ---
    skills_list = data.get('skills_extracted', [])
    skills_p = ", ".join(skills_list) if skills_list else "None detected."
    
    missing_list = data.get('missing_keywords', [])
    missing_p = ", ".join(missing_list) if missing_list else "None identified (perfect alignment)."
    
    cols_data = [
        [
            Paragraph("<b>EXTRACTED CORE SKILLS</b>", style_h2),
            Paragraph("<b>CRITICAL MISSING KEYWORDS</b>", style_h2)
        ],
        [
            Paragraph(skills_p, style_body),
            Paragraph(f"<font color='#FF3B30'>{missing_p}</font>", style_body)
        ]
    ]
    
    cols_table = Table(cols_data, colWidths=[doc.width/2.0, doc.width/2.0])
    cols_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 20), # gap between columns
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
    ]))
    story.append(cols_table)
    story.append(Spacer(1, 15))
    
    # --- PROFESSIONAL HIGHLIGHTS ---
    story.append(Paragraph("PROFESSIONAL HIGHLIGHTS", style_h2))
    summary_bullets = data.get('professional_summary', [])
    for b in summary_bullets:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Spacer(1, 15))
    
    # --- RECOMMENDATIONS FOR IMPROVEMENT ---
    story.append(Paragraph("RECOMMENDED CORRECTIONS", style_h2))
    suggestions = data.get('improvement_suggestions', [])
    for s in suggestions:
        story.append(Paragraph(f"• {s}", style_bullet))
        
    # Build Document
    doc.build(story)
    
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_bytes
