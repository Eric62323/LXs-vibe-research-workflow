#!/usr/bin/env python3
"""
应用模板格式到Word文档
确保字体、字号、行距、缩进等符合学术规范
"""

import sys
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

MATH_NS = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}

def set_run_font(run, font_name='Times New Roman', east_asia_font='宋体', size_pt=12, bold=False):
    """设置run的字体"""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)  # 黑色
    # 设置中文字体
    if run._element.rPr is None:
        run._element.get_or_add_rPr()
    if run._element.rPr.rFonts is None:
        run._element.rPr.get_or_add_rFonts()
    run._element.rPr.rFonts.set(qn('w:eastAsia'), east_asia_font)
    run._element.rPr.rFonts.set(qn('w:ascii'), font_name)
    run._element.rPr.rFonts.set(qn('w:hAnsi'), font_name)

def set_paragraph_format(paragraph, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                         first_line_indent=None, line_spacing=Pt(20),
                         space_before=Pt(0), space_after=Pt(0),
                         line_spacing_rule=None):
    """设置段落格式"""
    paragraph.alignment = alignment
    if first_line_indent:
        paragraph.paragraph_format.first_line_indent = first_line_indent
    paragraph.paragraph_format.line_spacing = line_spacing
    if line_spacing_rule:
        paragraph.paragraph_format.line_spacing_rule = line_spacing_rule
    paragraph.paragraph_format.space_before = space_before
    paragraph.paragraph_format.space_after = space_after

def is_horizontal_line(para):
    """检测段落是否为水平分隔线（Markdown --- 转换而来）"""
    if paragraph_has_math(para):
        return False
    text = para.text.strip()
    # 检查文本是否为水平线字符
    if text in ['---', '___', '***', '—', '–', '-']:
        return True
    # 检查是否只包含连字符或下划线或星号
    if text and all(c in '-_=*—–' for c in text):
        return True
    # 检查段落是否有底部边框（可能是水平线样式）
    pPr = para._p.get_or_add_pPr()
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is not None:
        # 检查是否有底部边框
        bottom = pBdr.find(qn('w:bottom'))
        if bottom is not None:
            return True
    return False


def remove_horizontal_lines(doc):
    """删除文档中的所有水平分隔线段落"""
    paragraphs_to_remove = []
    for para in doc.paragraphs:
        if is_horizontal_line(para):
            paragraphs_to_remove.append(para)

    # 删除标记的段落
    for para in paragraphs_to_remove:
        p = para._p
        p.getparent().remove(p)

    if paragraphs_to_remove:
        print(f"Removed {len(paragraphs_to_remove)} horizontal line(s)")


def paragraph_has_math(paragraph):
    """检测段落是否包含OMML数学公式"""
    try:
        return bool(paragraph._p.xpath('.//m:oMath | .//m:oMathPara', namespaces=MATH_NS))
    except Exception:
        return False


def format_document(input_path, output_path=None):
    """格式化文档"""
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        return False

    if output_path is None:
        output_path = input_path

    try:
        doc = Document(input_path)
    except Exception as e:
        print(f"Error opening file: {e}")
        return False

    print(f"Formatting: {input_path}")

    # 首先删除水平分隔线
    remove_horizontal_lines(doc)

    # 遍历所有段落
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        has_math = paragraph_has_math(para)

        # 判断段落类型并应用相应格式
        if text.startswith('【') or text.startswith('摘要：') or text.startswith('关键词：'):
            # 摘要和关键词：宋体/Times New Roman，小四，1.5倍行距
            if not has_math:
                for run in para.runs:
                    set_run_font(run, 'Times New Roman', '宋体', 12)
            set_paragraph_format(para, WD_ALIGN_PARAGRAPH.LEFT, Inches(0.4), 1.5)

        elif text.startswith('## ') or text.startswith('一、') or text.startswith('二、') or text.startswith('三、') or text.startswith('四、') or text.startswith('五、') or text.startswith('六、'):
            # 一级标题：黑体，三号（16pt），居中，加粗
            if not has_math:
                for run in para.runs:
                    set_run_font(run, 'Times New Roman', '黑体', 16, bold=True)
            set_paragraph_format(para, WD_ALIGN_PARAGRAPH.CENTER, None, 1.5, Pt(12), Pt(12))

        elif text.startswith('### ') or text.startswith('###') or (len(text) > 0 and text[0].isdigit() and '、' in text[:5]):
            # 二级标题：黑体，四号（14pt），左对齐，加粗
            if not has_math:
                for run in para.runs:
                    set_run_font(run, 'Times New Roman', '黑体', 14, bold=True)
            set_paragraph_format(para, WD_ALIGN_PARAGRAPH.LEFT, None, 1.5, Pt(6), Pt(6))

        elif text.startswith('#### ') or text.startswith('**') and text.endswith('**'):
            # 三级标题/加粗文本：黑体，小四（12pt），左对齐，加粗
            if not has_math:
                for run in para.runs:
                    set_run_font(run, 'Times New Roman', '黑体', 12, bold=True)
            set_paragraph_format(para, WD_ALIGN_PARAGRAPH.LEFT, None, 1.5, Pt(3), Pt(3))

        else:
            # 正文：宋体/Times New Roman，小四（12pt），首行缩进2字符，20磅固定行距
            if not has_math:
                for run in para.runs:
                    set_run_font(run, 'Times New Roman', '宋体', 12)
            set_paragraph_format(para, WD_ALIGN_PARAGRAPH.LEFT, Inches(0.4), Pt(20), Pt(0), Pt(0), WD_LINE_SPACING.EXACTLY)

    # 保存文档
    doc.save(output_path)
    print(f"Saved to: {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file
        format_document(input_file, output_file)
    else:
        print("Usage: python apply_template_format.py <input.docx> [output.docx]")
