#!/usr/bin/env python3
"""
修复Word文档中的LaTeX数学公式
将丢失的LaTeX公式从原文恢复并尝试转换为Word格式
"""

import sys
import re
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

def add_omath_paragraph(paragraph, latex_formula):
    """添加OMath公式到段落"""
    # 创建OMath元素
    oMathPara = OxmlElement('m:oMathPara')
    oMath = OxmlElement('m:oMath')

    # 简单的LaTeX到Word OMML转换（基础实现）
    # 处理简单的上标和下标
    formula_text = latex_formula

    # 替换常见的LaTeX符号为Word OMML格式
    # 这是一个简化版本，完整的实现需要解析LaTeX

    # 创建r元素
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Cambria Math')
    rFonts.set(qn('w:hAnsi'), 'Cambria Math')
    rFonts.set(qn('w:eastAsia'), 'Cambria Math')
    rPr.append(rFonts)

    # 设置字体大小
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '24')
    rPr.append(sz)

    t = OxmlElement('w:t')
    t.text = formula_text
    r.append(t)
    r.append(rPr)

    oMath.append(r)
    oMathPara.append(oMath)

    # 插入到段落
    paragraph._element.append(oMathPara)

def extract_and_restore_formulas(md_file, docx_file):
    """从markdown文件提取公式并恢复到docx"""
    import os

    if not os.path.exists(md_file):
        print(f"Warning: Markdown file not found: {md_file}")
        return False

    # 读取markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取所有公式（块级和行内）
    block_formulas = re.findall(r'\$\$([^$]+)\$\$', md_content)
    inline_formulas = re.findall(r'\$([^$]+)\$', md_content)

    all_formulas = block_formulas + inline_formulas

    if not all_formulas:
        print("No formulas found in markdown file")
        return False

    print(f"Found {len(all_formulas)} formulas in markdown")
    print("Restoring formulas to document...")

    # 打开docx文件
    doc = Document(docx_file)

    # 尝试恢复公式
    formula_index = 0
    for para in doc.paragraphs:
        text = para.text.strip()

        # 检查是否应该有公式
        if formula_index < len(all_formulas):
            # 查找可能包含公式的段落
            if 'BartikIV' in text or 'LU_' in text or 'log(' in text or 'beta' in text.lower():
                formula = all_formulas[formula_index]

                # 清理公式文本
                formula = formula.replace('\\_', '_').strip()

                # 添加公式段落
                if formula_index < len(block_formulas):
                    # 块级公式：创建新段落
                    new_para = doc.add_paragraph()
                    add_omath_paragraph(new_para, formula)
                else:
                    # 行内公式：在当前段落末尾添加
                    add_omath_paragraph(para, formula)

                formula_index += 1

    doc.save(docx_file)
    print(f"Restored {formula_index} formulas")
    return True

def convert_latex_to_text(latex):
    """将LaTeX公式转换为可读的文本格式"""
    # 简单的LaTeX到文本转换
    conversions = {
        r'\Delta': 'Δ',
        r'\log': 'log',
        r'\beta': 'β',
        r'\sum': 'Σ',
        r'\times': '×',
        r'\frac': '/'
    }

    text = latex
    for latex_cmd, symbol in conversions.items():
        text = text.replace(latex_cmd, symbol)

    # 处理上标和下标
    text = re.sub(r'_\{([^}]+)\}', r'_{\1}', text)
    text = re.sub(r'\^\{([^}]+)\}', r'^{\1}', text)

    return text

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_math_formulas.py <docx_file> [markdown_file]")
        sys.exit(1)

    docx_file = sys.argv[1]
    md_file = sys.argv[2] if len(sys.argv) > 2 else None

    if md_file:
        # 从markdown恢复公式
        extract_and_restore_formulas(md_file, docx_file)
    else:
        print("Warning: No markdown file provided. Cannot restore formulas.")
        print("Please provide the original markdown file as second argument.")

if __name__ == "__main__":
    main()
