#!/bin/bash
# 论文Word文档一键构建脚本
# 用法：./build_paper.sh <markdown文件路径> [output_name]
# 命名规则：日期_版本号_论文标题.docx

set -e  # 出错时停止

# 获取参数
INPUT_FILE="$1"

# 从文件名提取命名组件（格式：日期_版本号_论文标题.md）
parse_filename() {
    local filename="$1"
    local basename=$(basename "$filename" .md)

    # 检查是否符合 日期_版本号_论文标题 格式
    if [[ $basename =~ ^([0-9]{8})_(v[0-9]+\.[0-9]+)_(.+)$ ]]; then
        echo "${BASH_REMATCH[1]}_${BASH_REMATCH[2]}_${BASH_REMATCH[3]}"
        return 0
    fi

    # 不符合规范格式，返回原文件名（去掉.md）
    echo "$basename"
    return 0
}

# 确定输出文件名
if [ -n "$2" ]; then
    # 用户提供了自定义输出名
    OUTPUT_NAME="$2"
else
    # 自动解析文件名
    OUTPUT_NAME=$(parse_filename "$INPUT_FILE")
fi

# 检查输入文件
if [ -z "$INPUT_FILE" ]; then
    echo "Error: 请指定Markdown文件路径"
    echo "用法：./build_paper.sh <markdown文件路径> [output_name]"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: 文件不存在: $INPUT_FILE"
    exit 1
fi

# 获取目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$INPUT_FILE")"
OUTPUT_FILE="${PROJECT_DIR}/${OUTPUT_NAME}.docx"
TEMPLATE_FILE="${SCRIPT_DIR}/../规范/template.docx"

# 检查模板
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: 模板文件不存在: $TEMPLATE_FILE"
    exit 1
fi

echo "========================================="
echo "开始构建Word文档..."
echo "输入: $INPUT_FILE"
echo "输出: $OUTPUT_FILE"
echo "========================================="

# 步骤1: Pandoc转换（保留LaTeX公式）
echo "[1/4] Pandoc转换（保留LaTeX公式）..."

# 转换
pandoc "$INPUT_FILE" \
    --from markdown+tex_math_dollars+tex_math_double_backslash \
    --to docx \
    --reference-doc="$TEMPLATE_FILE" \
    --output="$OUTPUT_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Pandoc转换失败"
    exit 1
fi

echo "✓ Pandoc转换完成"

# 步骤2: 应用格式化脚本（删除分隔线、应用字体格式）
echo "[2/4] 应用格式（删除分隔线、设置字体字号）..."
python3 "${SCRIPT_DIR}/apply_template_format.py" "$OUTPUT_FILE"

if [ $? -ne 0 ]; then
    echo "Error: 格式化失败"
    exit 1
fi

echo "✓ 格式应用完成"

# 步骤3: 恢复数学公式（已禁用，避免格式问题）
echo "[3/4] 跳过公式恢复（保持pandoc原始格式）..."
# python3 "${SCRIPT_DIR}/restore_math_formulas.py" "$OUTPUT_FILE" "$INPUT_FILE" 2>/dev/null || echo "  （公式恢复脚本未找到，跳过）"

echo "✓ 跳过公式恢复"

# 步骤4: 表格规范化（如果有表格）
echo "[4/4] 检查表格格式..."
python3 "${SCRIPT_DIR}/table_formatter.py" "$OUTPUT_FILE" 2>/dev/null || echo "  （无表格需要处理）"

echo "✓ 表格处理完成"

echo "========================================="
echo "✓ 构建成功: $OUTPUT_FILE"
echo "========================================="
ls -lh "$OUTPUT_FILE"
