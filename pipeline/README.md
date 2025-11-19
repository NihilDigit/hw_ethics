# 国内双一流高校生成式人工智能政策分析 - 数据处理流水线

本文件夹包含完整的数据处理流水线，从爬取原始政策文本到生成最终分析报告的全部代码。

## 📋 流程概览

整个数据处理流程分为4个阶段：

```
1_crawler (爬虫)
    ↓
2_cleaning (数据清洗)
    ↓
3_analysis (数据分析)
    ↓
4_report (报告生成)
```

## 📁 目录结构

```
pipeline/
├── 1_crawler/              # 阶段1：爬虫
│   ├── universities_list.py        # 146所双一流大学名单
│   ├── crawler_real.py             # 第一轮爬虫（主要）
│   └── crawler_retry_failed.py     # 第二轮重试爬虫
├── 2_cleaning/             # 阶段2：数据清洗
│   ├── data_cleaner_v2.py          # V2数据清洗脚本
│   └── post_clean_manual.py        # 手动微调清洗
├── 3_analysis/             # 阶段3：数据分析
│   ├── text_preprocessing.py       # 文本预处理（分词、停用词）
│   ├── lda_analysis.py             # LDA主题模型分析
│   ├── text_analysis.py            # TF-IDF和共现网络分析
│   └── visualization.py            # 数据可视化
├── 4_report/               # 阶段4：报告生成
│   ├── generate_summary_report.py  # 生成汇总报告
│   ├── build_report.py             # 构建LaTeX内容
│   └── build_report.sh             # 一键编译PDF
├── requirements.txt        # Python依赖
├── README.md               # 本文档
└── run_pipeline.sh         # 一键运行完整流程
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装Python依赖
pip install -r requirements.txt

# 确保在项目根目录下有以下目录
mkdir -p data figures fonts
```

### 2. 使用现有数据运行分析（推荐）

如果你已经有爬取和清洗后的数据（`data/policies_cleaned_final.json`），可以直接运行分析：

```bash
# 从项目根目录运行
cd /home/user/hw_ethics

# 运行完整分析流程（跳过爬虫和清洗）
python3 pipeline/3_analysis/text_preprocessing.py
python3 pipeline/3_analysis/lda_analysis.py
python3 pipeline/3_analysis/text_analysis.py
python3 pipeline/3_analysis/visualization.py
python3 pipeline/4_report/generate_summary_report.py
./pipeline/4_report/build_report.sh
```

### 3. 从头运行完整流程

⚠️ **警告**：爬虫过程需要2-3小时，不建议重新运行除非必要。

```bash
# 从项目根目录运行
cd /home/user/hw_ethics

# 运行一键脚本
./pipeline/run_pipeline.sh
```

## 📊 数据流详解

### 阶段1：爬虫（1_crawler）

**目标**：从互联网爬取双一流高校的生成式AI政策文本

**脚本**：
- `universities_list.py` - 定义146所双一流大学列表
- `crawler_real.py` - 第一轮爬取，使用百度搜索
- `crawler_retry_failed.py` - 第二轮重试失败的大学

**输入**：无
**输出**：
- `data/policies.json` - 原始政策数据（115份文档，77所大学）
- `data/raw_policies/` - 原始文本文件
- `crawler.log` - 爬取日志

**运行方式**：
```bash
cd /home/user/hw_ethics
python3 pipeline/1_crawler/crawler_real.py
python3 pipeline/1_crawler/crawler_retry_failed.py
```

**关键参数**：
- 搜索关键词：生成式人工智能、ChatGPT、AI工具等
- 延迟时间：2秒/请求（避免被封）
- 搜索引擎：百度（site:.edu.cn限定）

### 阶段2：数据清洗（2_cleaning）

**目标**：删除网站框架噪声，保留政策实质内容

**脚本**：
- `data_cleaner_v2.py` - 主要清洗脚本
- `post_clean_manual.py` - 手动微调

**输入**：
- `data/policies.json` - 原始数据（100KB）

**输出**：
- `data/policies_cleaned.json` - V2清洗结果
- `data/policies_cleaned_final.json` - **最终清洗数据**（81KB）
- `data/policies_cleaned_report.txt` - 清洗报告

**运行方式**：
```bash
cd /home/user/hw_ethics
python3 pipeline/2_cleaning/data_cleaner_v2.py
python3 pipeline/2_cleaning/post_clean_manual.py
```

**清洗效果**：
- 删除噪声：~27%（约19KB）
- 删除内容：导航菜单、面包屑、版权信息、操作按钮、URL、友情链接等
- 保留内容：政策标题、正文、通知内容等实质性信息

### 阶段3：数据分析（3_analysis）

**目标**：对清洗后的政策文本进行文本分析和可视化

**脚本执行顺序**：
1. `text_preprocessing.py` - 文本预处理
2. `lda_analysis.py` - LDA主题模型
3. `text_analysis.py` - TF-IDF和共现网络
4. `visualization.py` - 生成图表

**输入**：
- `data/policies_cleaned_final.json` - 清洗后数据

**输出**：
- `data/processed_policies.json` - 预处理数据（分词、关键词）
- `data/lda_topics.json` - LDA主题模型结果
- `data/tfidf_results.json` - TF-IDF分析结果
- `data/cooccurrence_edges.json` - 词语共现网络
- `data/keyword_similarity.json` - 关键词相似度矩阵
- `figures/*.png` - 可视化图表

**运行方式**：
```bash
cd /home/user/hw_ethics
python3 pipeline/3_analysis/text_preprocessing.py
python3 pipeline/3_analysis/lda_analysis.py
python3 pipeline/3_analysis/text_analysis.py
python3 pipeline/3_analysis/visualization.py
```

**分析方法**：
- **中文分词**：jieba分词
- **关键词提取**：TF-IDF算法
- **主题建模**：LDA（Latent Dirichlet Allocation）
- **共现网络**：基于关键词共现构建语义网络
- **聚类分析**：基于关键词相似度的层次聚类

### 阶段4：报告生成（4_report）

**目标**：生成数据汇总报告和最终PDF论文

**脚本**：
- `generate_summary_report.py` - 生成Markdown汇总报告
- `build_report.sh` - 编译LaTeX为PDF

**输入**：
- 所有分析结果（data/目录）
- LaTeX模板（根目录的.tex文件）

**输出**：
- `data/analysis_summary.md` - 数据汇总报告
- `国内双一流高校生成式人工智能相关政策分析.pdf` - 最终论文PDF

**运行方式**：
```bash
cd /home/user/hw_ethics
python3 pipeline/4_report/generate_summary_report.py
./pipeline/4_report/build_report.sh
```

## 📈 数据文件说明

### 原始数据
- `data/policies.json` - 爬虫采集的原始数据（含噪声，100KB）
- `data/raw_policies/*.txt` - 原始txt文件（未使用）

### 清洗数据
- `data/policies_cleaned_final.json` - **最终清洗数据**（推荐使用，81KB）

### 分析数据
- `data/processed_policies.json` - 预处理后的数据（分词、关键词等）
- `data/lda_topics.json` - LDA主题模型结果
- `data/tfidf_results.json` - TF-IDF分析结果
- `data/cooccurrence_edges.json` - 词语共现网络
- `data/keyword_similarity.json` - 关键词相似度矩阵

### 报告数据
- `data/analysis_summary.md` - 数据汇总报告

## 🔧 重要说明

### 数据复现性

1. **固化数据**：`data/policies_cleaned_final.json` 是固化的最终数据，所有后续分析都基于此文件
2. **不建议重新爬取**：爬虫过程耗时长且结果可能不同，建议使用已有数据
3. **可重新分析**：阶段3和阶段4可以重复运行，结果是确定性的

### 脚本依赖关系

```
universities_list.py (独立模块)
    ↓
crawler_real.py → data/policies.json
    ↓
crawler_retry_failed.py → data/policies.json (更新)
    ↓
data_cleaner_v2.py → data/policies_cleaned.json
    ↓
post_clean_manual.py → data/policies_cleaned_final.json
    ↓
text_preprocessing.py → data/processed_policies.json
    ↓
┌───────────┬──────────────┬─────────────┐
│           │              │             │
lda_analysis.py  text_analysis.py  visualization.py
│           │              │             │
└───────────┴──────────────┴─────────────┘
    ↓           ↓              ↓
各种分析数据文件 + figures/
    ↓
generate_summary_report.py → data/analysis_summary.md
    ↓
build_report.sh → 国内双一流高校生成式人工智能相关政策分析.pdf
```

### 运行环境要求

- **Python**：3.8+
- **LaTeX**：xelatex 或 pdflatex（用于PDF编译）
- **字体**：需要中文字体支持（见 `fonts/` 目录）
- **内存**：建议4GB以上
- **磁盘**：约500MB（包括依赖和数据）

## 📝 参数配置

### LDA主题模型参数（lda_analysis.py）
```python
n_topics = 5          # 主题数量
passes = 20           # 迭代轮数
iterations = 100      # 每轮迭代次数
```

### TF-IDF参数（text_analysis.py）
```python
max_features = 100    # 最大关键词数
min_df = 2           # 最小文档频率
max_df = 0.7         # 最大文档频率
```

### 可视化参数（visualization.py）
```python
top_n_keywords = 20   # 显示的关键词数量
network_threshold = 3 # 共现网络最小边权重
```

## 🐛 常见问题

### Q1: 爬虫失败/被封怎么办？
**A**: 增加延迟时间（delay参数），或使用代理IP。不建议频繁重新爬取。

### Q2: 数据清洗后内容太少？
**A**: 检查清洗规则是否过于严格，可调整 `data_cleaner_v2.py` 中的噪声关键词列表。

### Q3: LDA主题不清晰？
**A**: 调整主题数量（n_topics）或增加迭代次数（passes）。

### Q4: PDF编译失败？
**A**: 检查是否安装了LaTeX（xelatex），以及中文字体是否正确安装。

### Q5: 如何验证结果可复现？
**A**: 删除 `data/processed_policies.json` 和 `figures/` 下的文件，然后重新运行阶段3和4。

## 📚 参考文献

详见项目根目录的 `Ref/TLDR.md` 文件。

## 📄 许可证

本项目仅用于学术研究目的。
