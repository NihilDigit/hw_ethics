#!/bin/bash

# 一键编译PDF工作流脚本
# 此脚本会自动运行所有分析步骤并生成最终的PDF报告

set -e  # 遇到错误立即退出

echo "========================================"
echo "国内双一流高校生成式AI政策分析报告"
echo "一键编译PDF工作流"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 步骤1: 检查Python依赖
echo "[1/5] 检查Python依赖..."
python -c "import numpy, pandas, matplotlib, seaborn, networkx, sklearn, gensim" 2>/dev/null || {
    echo "正在安装Python依赖..."
    pip install -q numpy pandas matplotlib seaborn networkx scikit-learn gensim
}
echo "✓ Python依赖检查完成"
echo ""

# 步骤2: 运行文本预处理（如果需要）
if [ -f "data/processed_policies.json" ]; then
    echo "[2/5] 跳过文本预处理（数据已存在）"
else
    echo "[2/5] 运行文本预处理..."
    python text_preprocessing.py
    echo "✓ 文本预处理完成"
fi
echo ""

# 步骤3: 运行分析脚本
echo "[3/5] 运行数据分析..."
echo "  - LDA主题模型分析..."
python lda_analysis.py > /dev/null 2>&1
echo "  ✓ LDA分析完成"

echo "  - TF-IDF和共现网络分析..."
python text_analysis.py > /dev/null 2>&1
echo "  ✓ 文本分析完成"

echo "  - 生成可视化图表..."
python visualization.py > /dev/null 2>&1
echo "  ✓ 可视化完成"

echo "  - 生成数据汇总报告..."
python generate_summary_report.py > /dev/null 2>&1
echo "  ✓ 汇总报告完成"
echo ""

# 步骤4: 编译LaTeX为PDF
echo "[4/5] 编译LaTeX文档为PDF..."

# 检查LaTeX编译器
if command -v xelatex >/dev/null 2>&1; then
    LATEX_CMD="xelatex"
elif command -v pdflatex >/dev/null 2>&1; then
    LATEX_CMD="pdflatex"
else
    echo "错误: 未找到LaTeX编译器 (xelatex或pdflatex)"
    echo "请安装 texlive-xetex 或 texlive-latex-base"
    exit 1
fi

# LaTeX文件名
TEX_FILE="国内双一流高校生成式人工智能相关政策分析.tex"
PDF_FILE="${TEX_FILE%.tex}.pdf"

# 编译LaTeX（运行两次以确保交叉引用正确）
echo "  使用 $LATEX_CMD 编译..."
$LATEX_CMD -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1 || {
    echo "  第一次编译完成（可能有警告）"
}
$LATEX_CMD -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1 || {
    echo "  第二次编译完成（可能有警告）"
}

# 清理临时文件
rm -f *.aux *.log *.out *.toc *.bbl *.blg *.synctex.gz

if [ -f "$PDF_FILE" ]; then
    echo "✓ PDF编译成功: $PDF_FILE"
else
    echo "✗ PDF编译失败"
    exit 1
fi
echo ""

# 步骤5: 总结
echo "[5/5] 构建完成"
echo ""
echo "========================================"
echo "报告生成成功！"
echo "========================================"
echo ""
echo "生成的文件："
echo "  📄 PDF报告: $PDF_FILE"
echo "  📊 图表目录: figures/"
echo "  📈 数据文件: data/"
echo "  📝 汇总报告: data/analysis_summary.md"
echo ""
echo "快速查看："
echo "  - 查看PDF: xdg-open '$PDF_FILE' (Linux)"
echo "  - 查看PDF: open '$PDF_FILE' (macOS)"
echo "  - 查看图表: ls -lh figures/"
echo ""
