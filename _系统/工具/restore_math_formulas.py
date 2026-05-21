#!/usr/bin/env python3
"""
恢复Word文档中的数学公式
从原始markdown文件提取LaTeX公式，并在Word文档中插入可编辑的文本版本
"""

import sys
import re
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

def insert_formula_text(paragraph, formula_text, is_display=False):
    """在段落中插入公式文本（使用Cambria Math字体）"""
    # 清理公式文本
    formula_text = formula_text.strip()
    # 移除$$标记
    formula_text = formula_text.replace('$$', '').strip()
    # 恢复转义的下划线
    formula_text = formula_text.replace('\\_', '_')
    # 移除多余的空白
    formula_text = ' '.join(formula_text.split())

    # 创建run - 只插入公式文本，不添加标记
    run = paragraph.add_run(formula_text)

    # 设置字体为Cambria Math（数学字体）
    run.font.name = 'Cambria Math'
    run.font.size = Pt(11)

    # 设置中文字体
    if run._element.rPr is None:
        run._element.get_or_add_rPr()
    if run._element.rPr.rFonts is None:
        run._element.rPr.get_or_add_rFonts()
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Cambria Math')
    run._element.rPr.rFonts.set(qn('w:ascii'), 'Cambria Math')
    run._element.rPr.rFonts.set(qn('w:hAnsi'), 'Cambria Math')

    # 斜体（数学公式通常用斜体）
    run.font.italic = True

    # 如果是显示公式，居中
    if is_display:
        paragraph.alignment = 3  # WD_ALIGN_PARAGRAPH.CENTER

def restore_formulas(md_file, docx_file):
    """从markdown文件恢复公式到Word文档"""
    import os

    if not os.path.exists(md_file):
        print(f"Warning: Markdown file not found: {md_file}")
        return False

    # 读取markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取公式
    # 块级公式: $$...$$
    block_formulas = re.findall(r'\$\$([^$]+?)\$\$', md_content, re.DOTALL)
    # 行内公式: $...$
    inline_formulas = re.findall(r'\$([^$]+?)\$', md_content)

    # 清理公式列表
    block_formulas = [f.strip() for f in block_formulas if f.strip()]
    inline_formulas = [f.strip() for f in inline_formulas if f.strip()]

    total_formulas = len(block_formulas) + len(inline_formulas)

    if total_formulas == 0:
        print("No formulas found in markdown file")
        return False

    print(f"Found {len(block_formulas)} display formulas and {len(inline_formulas)} inline formulas")

    # 打开docx文件
    doc = Document(docx_file)

    # 记录原始段落数
    original_para_count = len(doc.paragraphs)

    # 恢复块级公式
    block_idx = 0
    inline_idx = 0

    # 创建一个段落索引到公式的映射
    para_to_formula = {}

    # 分析markdown，找出每个公式应该在的位置
    lines = md_content.split('\n')
    current_para = 0
    i = 0
    processed_paras = set()  # 记录已处理的段落，避免重复

    while i < len(lines) and current_para < original_para_count:
        line = lines[i].strip()

        # 跳过空行
        if not line:
            i += 1
            continue

        # 检查是否是块级公式开始
        if line == '$$':
            # 找到公式结束
            formula_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != '$$':
                formula_lines.append(lines[i])
                i += 1

            formula = ' '.join(formula_lines).strip()
            if formula and block_idx < len(block_formulas):
                # 在当前段落位置之后插入公式段落
                if current_para not in processed_paras:
                    para_to_formula[current_para] = ('display', formula)
                    processed_paras.add(current_para)
                block_idx += 1
            i += 1
            current_para += 1
        else:
            # 普通文本，检查是否有行内公式
            # 只处理明确的行内公式标记
            if '$' in line and current_para not in processed_paras:
                # 计算这一行有多少个行内公式
                dollar_count = line.count('$')
                if dollar_count >= 2 and dollar_count % 2 == 0:  # 成对的$符号
                    # 有行内公式，记录但先不插入（避免复杂逻辑）
                    # 只处理最简单的情况：段落末尾的单个行内公式
                    pass

            current_para += 1
            i += 1

    # 现在在Word文档中插入公式
    inserted_count = 0
    # 从后往前插入，避免索引问题
    sorted_paras = sorted(para_to_formula.items(), key=lambda x: x[0], reverse=True)

    for para_idx, (formula_type, formula) in sorted_paras:
        if para_idx < len(doc.paragraphs):
            try:
                if formula_type == 'display':
                    # 在段落前插入新的公式段落
                    target_element = doc.paragraphs[para_idx]._element
                    parent = target_element.getparent()
                    index = parent.index(target_element)

                    new_p_element = OxmlElement('w:p')
                    parent.insert(index, new_p_element)
                    new_para = Paragraph(new_p_element, doc)
                    insert_formula_text(new_para, formula, is_display=True)
                else:
                    # 行内公式，在段落末尾插入
                    insert_formula_text(doc.paragraphs[para_idx], formula, is_display=False)
                inserted_count += 1
            except Exception as e:
                print(f"Warning: Failed to insert formula at position {para_idx}: {e}")

    doc.save(docx_file)
    print(f"Restored {inserted_count} formulas to document")
    return True

# 修正导入
from docx.text.paragraph import Paragraph

def main():
    if len(sys.argv) < 3:
        print("Usage: python restore_math_formulas.py <docx_file> <markdown_file>")
        sys.exit(1)

    docx_file = sys.argv[1]
    md_file = sys.argv[2]

    restore_formulas(md_file, docx_file)

if __name__ == "__main__":
    main()
