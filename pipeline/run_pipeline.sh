#!/bin/bash

###############################################################################
# 国内双一流高校生成式人工智能政策分析 - 完整数据处理流水线
#
# 本脚本按顺序执行所有数据处理步骤：
# 1. 爬虫（可选，默认跳过）
# 2. 数据清洗（可选，默认跳过）
# 3. 数据分析（必选）
# 4. 报告生成（必选）
###############################################################################

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录（pipeline/）
PIPELINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 项目根目录
ROOT_DIR="$(dirname "$PIPELINE_DIR")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}国内双一流高校生成式AI政策分析${NC}"
echo -e "${BLUE}完整数据处理流水线${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 切换到项目根目录
cd "$ROOT_DIR"
echo -e "${GREEN}[信息]${NC} 工作目录: $ROOT_DIR"
echo ""

###############################################################################
# 检查环境
###############################################################################

echo -e "${BLUE}[0/4]${NC} 检查环境..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误]${NC} 未找到 python3"
    exit 1
fi
echo -e "${GREEN}  ✓${NC} Python: $(python3 --version)"

# 检查依赖
echo -e "${YELLOW}[信息]${NC} 检查Python依赖..."
python3 -c "import numpy, pandas, matplotlib, seaborn, networkx, sklearn, gensim, jieba" 2>/dev/null || {
    echo -e "${YELLOW}[警告]${NC} 缺少部分Python依赖，正在安装..."
    pip install -q -r "$PIPELINE_DIR/requirements.txt"
    echo -e "${GREEN}  ✓${NC} 依赖安装完成"
}

# 检查必要目录
mkdir -p data figures fonts
echo -e "${GREEN}  ✓${NC} 目录结构正常"
echo ""

###############################################################################
# 阶段1：爬虫（可选）
###############################################################################

echo -e "${BLUE}[1/4]${NC} 阶段1：爬虫"

if [ -f "data/policies.json" ]; then
    echo -e "${GREEN}  ✓${NC} 检测到已有原始数据: data/policies.json"
    echo -e "${YELLOW}  ⊳${NC} 跳过爬虫阶段（如需重新爬取，请删除 data/policies.json）"
else
    echo -e "${YELLOW}  ⊳${NC} 未找到原始数据，开始爬虫..."
    echo -e "${YELLOW}  ⚠${NC}  警告: 爬虫过程需要2-3小时，且结果可能不同"

    read -p "是否继续爬虫？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}  →${NC} 第一轮爬虫（主要爬取）..."
        python3 "$PIPELINE_DIR/1_crawler/crawler_real.py"

        echo -e "${BLUE}  →${NC} 第二轮爬虫（重试失败的大学）..."
        python3 "$PIPELINE_DIR/1_crawler/crawler_retry_failed.py"

        echo -e "${GREEN}  ✓${NC} 爬虫完成"
    else
        echo -e "${RED}[错误]${NC} 缺少原始数据且未执行爬虫，无法继续"
        exit 1
    fi
fi
echo ""

###############################################################################
# 阶段2：数据清洗（可选）
###############################################################################

echo -e "${BLUE}[2/4]${NC} 阶段2：数据清洗"

if [ -f "data/policies_cleaned_final.json" ]; then
    echo -e "${GREEN}  ✓${NC} 检测到已有清洗数据: data/policies_cleaned_final.json"
    echo -e "${YELLOW}  ⊳${NC} 跳过数据清洗（如需重新清洗，请删除 data/policies_cleaned_final.json）"
else
    echo -e "${BLUE}  →${NC} 执行V2数据清洗..."
    python3 "$PIPELINE_DIR/2_cleaning/data_cleaner_v2.py"

    echo -e "${BLUE}  →${NC} 执行手动微调..."
    python3 "$PIPELINE_DIR/2_cleaning/post_clean_manual.py"

    echo -e "${GREEN}  ✓${NC} 数据清洗完成"
fi
echo ""

###############################################################################
# 阶段3：数据分析（必选）
###############################################################################

echo -e "${BLUE}[3/4]${NC} 阶段3：数据分析"

# 检查清洗数据是否存在
if [ ! -f "data/policies_cleaned_final.json" ]; then
    echo -e "${RED}[错误]${NC} 未找到清洗后的数据: data/policies_cleaned_final.json"
    exit 1
fi

# 文本预处理
echo -e "${BLUE}  →${NC} [1/4] 文本预处理（分词、关键词提取）..."
python3 "$PIPELINE_DIR/3_analysis/text_preprocessing.py"
echo -e "${GREEN}  ✓${NC} 预处理完成 → data/processed_policies.json"

# LDA主题模型
echo -e "${BLUE}  →${NC} [2/4] LDA主题模型分析..."
python3 "$PIPELINE_DIR/3_analysis/lda_analysis.py" > /dev/null 2>&1
echo -e "${GREEN}  ✓${NC} LDA分析完成 → data/lda_topics.json"

# TF-IDF和共现网络
echo -e "${BLUE}  →${NC} [3/4] TF-IDF和共现网络分析..."
python3 "$PIPELINE_DIR/3_analysis/text_analysis.py" > /dev/null 2>&1
echo -e "${GREEN}  ✓${NC} 文本分析完成 → data/tfidf_results.json, data/cooccurrence_edges.json"

# 可视化
echo -e "${BLUE}  →${NC} [4/4] 生成可视化图表..."
python3 "$PIPELINE_DIR/3_analysis/visualization.py" > /dev/null 2>&1
echo -e "${GREEN}  ✓${NC} 可视化完成 → figures/*.png"

echo -e "${GREEN}  ✓${NC} 数据分析阶段全部完成"
echo ""

###############################################################################
# 阶段4：报告生成（必选）
###############################################################################

echo -e "${BLUE}[4/4]${NC} 阶段4：报告生成"

# 生成汇总报告
echo -e "${BLUE}  →${NC} [1/2] 生成数据汇总报告..."
python3 "$PIPELINE_DIR/4_report/generate_summary_report.py" > /dev/null 2>&1
echo -e "${GREEN}  ✓${NC} 汇总报告完成 → data/analysis_summary.md"

# 编译LaTeX为PDF
echo -e "${BLUE}  →${NC} [2/2] 编译LaTeX文档为PDF..."

# 检查LaTeX编译器
if command -v xelatex >/dev/null 2>&1; then
    LATEX_CMD="xelatex"
elif command -v pdflatex >/dev/null 2>&1; then
    LATEX_CMD="pdflatex"
else
    echo -e "${RED}[错误]${NC} 未找到LaTeX编译器 (xelatex或pdflatex)"
    echo -e "${YELLOW}[提示]${NC} 跳过PDF编译，其他步骤已完成"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}流水线执行完成（除PDF编译外）${NC}"
    echo -e "${GREEN}========================================${NC}"
    exit 0
fi

TEX_FILE="国内双一流高校生成式人工智能相关政策分析.tex"
PDF_FILE="${TEX_FILE%.tex}.pdf"

# 编译LaTeX（运行两次以确保交叉引用正确）
$LATEX_CMD -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1 || true
$LATEX_CMD -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1 || true

# 清理临时文件
rm -f *.aux *.log *.out *.toc *.bbl *.blg *.synctex.gz 2>/dev/null || true

if [ -f "$PDF_FILE" ]; then
    echo -e "${GREEN}  ✓${NC} PDF编译成功 → $PDF_FILE"
else
    echo -e "${YELLOW}[警告]${NC} PDF编译失败（可能是字体问题）"
fi

echo ""

###############################################################################
# 完成总结
###############################################################################

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}流水线执行完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${BLUE}生成的文件：${NC}"
echo -e "  📊 ${YELLOW}数据文件${NC}"
echo "     - data/policies_cleaned_final.json   (清洗后数据)"
echo "     - data/processed_policies.json       (预处理数据)"
echo "     - data/lda_topics.json               (LDA主题)"
echo "     - data/tfidf_results.json            (TF-IDF结果)"
echo "     - data/cooccurrence_edges.json       (共现网络)"
echo ""
echo -e "  📈 ${YELLOW}可视化图表${NC}"
echo "     - figures/word_frequency.png         (词频分布)"
echo "     - figures/lda_topics.png             (主题分布)"
echo "     - figures/keyword_network.png        (关键词网络)"
echo "     - figures/category_distribution.png  (分类分布)"
echo ""
echo -e "  📄 ${YELLOW}报告${NC}"
echo "     - data/analysis_summary.md           (数据汇总)"
if [ -f "$PDF_FILE" ]; then
    echo "     - $PDF_FILE                          (最终论文)"
fi
echo ""

echo -e "${BLUE}下一步：${NC}"
echo "  1. 查看数据汇总: cat data/analysis_summary.md"
echo "  2. 查看图表: ls -lh figures/"
if [ -f "$PDF_FILE" ]; then
    echo "  3. 查看PDF: xdg-open '$PDF_FILE'"
fi
echo ""

echo -e "${GREEN}数据处理流水线执行完毕！${NC}"
