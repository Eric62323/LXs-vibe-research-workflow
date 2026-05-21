#!/usr/bin/env python3
"""
学术论文Word文档格式化工具
功能：设置正文、标题的字体字号，调整段落格式
"""

import sys
import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_run_font(run, font_name='Times New Roman', east_asia_font='宋体', size_pt=12):
    """设置run的字体"""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    # 设置中文字体
    if run._element.rPr is None:
        run._element.get_or_add_rPr()
    if run._element.rPr.rFonts is None:
        run._element.rPr.get_or_add_rFonts()
    run._element.rPr.rFonts.set(qn('w:eastAsia'), east_asia_font)

def format_paragraph(paragraph, style_name='Normal'):
    """格式化段落"""
    # 根据段落样式应用不同格式
    if style_name.startswith('Heading 1') or '标题 1' in style_name:
        # 一级标题：黑体，16pt（三号），居中
        for run in paragraph.runs:
            set_run_font(run, 'Times New Roman', '黑体', 16)
            run.bold = True
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(24)
        paragraph.paragraph_format.space_after = Pt(18)
        paragraph.paragraph_format.line_spacing = 1.5

    elif style_name.startswith('Heading 2') or '标题 2' in style_name:
        # 二级标题：黑体，14pt（四号），左对齐
        for run in paragraph.runs:
            set_run_font(run, 'Times New Roman', '黑体', 14)
            run.bold = True
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = Pt(18)
        paragraph.paragraph_format.space_after = Pt(12)
        paragraph.paragraph_format.line_spacing = 1.5

    elif style_name.startswith('Heading 3') or '标题 3' in style_name:
        # 三级标题：黑体，12pt（小四），左对齐
        for run in paragraph.runs:
            set_run_font(run, 'Times New Roman', '黑体', 12)
            run.bold = True
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = Pt(12)
        paragraph.paragraph_format.space_after = Pt(6)
        paragraph.paragraph_format.line_spacing = 1.5

    else:
        # 正文：宋体/Times New Roman，12pt（小四）
        for run in paragraph.runs:
            set_run_font(run, 'Times New Roman', '宋体', 12)
        paragraph.paragraph_format.first_line_indent = Inches(0.4)  # 首行缩进2字符
        paragraph.paragraph_format.line_spacing = 1.5  # 1.5倍行距
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)

def format_docx(file_path):
    """格式化Word文档"""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"Error opening file: {e}")
        return False

    print(f"Formatting document: {file_path}...")

    # 格式化所有段落
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else 'Normal'
        format_paragraph(para, style_name)

    # 保存
    doc.save(file_path)
    print(f"Successfully formatted: {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        format_docx(sys.argv[1])
    else:
        print("Usage: python docx_formatter.py <docx_file_path>")
