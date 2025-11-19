# 国内双一流高校生成式人工智能相关政策分析

## 项目简介

本项目通过网络爬虫收集了国内**15所双一流高校**发布的生成式人工智能相关政策文本，共计**17份政策**。涵盖清华大学、上海交通大学、西安交通大学、中国人民大学、华东师范大学、江南大学、东北大学、中国科学技术大学、中国农业大学、西安电子科技大学、华北电力大学、上海科技大学、南京医科大学、北京外国语大学、大连理工大学。

研究综合运用了**TF-IDF算法**、**LDA主题模型**和**语义网络分析**等文本挖掘方法,揭示了高校生成式AI政策的核心议题、演化趋势和类别特征。

## 主要研究发现

1. **政策关注重点**: 教学管理类政策占比最高(52.9%)，反映高校重点关注AI在教学中的应用

2. **核心议题**:
   - AI教学应用与课程建设
   - 学术规范与AIGC使用
   - 师生AI素养培养与平台建设
   - 教学改革项目推进

3. **关键词共现关系**:
   - "项目-申报"、"论文-AIGC"、"教学改革-项目"为核心共现对
   - 反映高校通过项目推动AI教学创新
   - 强调学术诚信与规范使用

4. **LDA主题分析**: 识别出5个主题，包括教学监管探索、服务与应用、课程项目建设、平台素养培育、课程教学赋能

## 项目结构

```
hw_ethics/
├── README.md                           # 本说明文档
├── PIPELINE.md                         # 数据处理流水线概览
├── CLAUDE.md                           # 项目需求文档
├── requirements.txt                    # Python依赖包
├── 国内双一流高校生成式人工智能相关政策分析.tex  # LaTeX论文
├── 国内双一流高校生成式人工智能相关政策分析.pdf  # 论文PDF
│
├── pipeline/                           # 完整数据处理流水线
│   ├── README.md                       # 详细技术文档
│   ├── QUICKSTART.md                   # 快速开始指南
│   ├── run_pipeline.sh                 # 一键运行脚本
│   ├── requirements.txt                # 依赖清单
│   ├── 1_crawler/                      # 阶段1: 数据爬取
│   │   ├── crawler_real.py             # 真实爬虫（使用搜索引擎）
│   │   ├── crawler_retry_failed.py     # 失败重试脚本
│   │   └── universities_list.py        # 147所双一流高校名单
│   ├── 2_cleaning/                     # 阶段2: 数据清洗
│   │   ├── data_cleaner_v2.py          # 数据清洗脚本
│   │   └── post_clean_manual.py        # 手动清洗脚本
│   ├── 3_analysis/                     # 阶段3: 数据分析
│   │   ├── text_preprocessing.py       # 文本预处理和分词
│   │   ├── lda_analysis.py             # LDA主题模型分析
│   │   ├── text_analysis.py            # TF-IDF和共现分析
│   │   └── visualization.py            # 可视化图表生成
│   └── 4_report/                       # 阶段4: 报告生成
│       ├── generate_summary_report.py  # 汇总报告生成
│       ├── build_report.py             # 论文构建脚本
│       └── build_report.sh             # 论文构建Shell脚本
│
├── scripts/                            # 实用工具脚本
│   ├── README.md                       # 工具说明文档
│   ├── check_data_quality.py           # 数据质量检查
│   └── rebuild_policies.py             # 从原始文件重建数据
│
├── data/                               # 数据目录
│   ├── policies.json                   # 原始政策数据(115份)
│   ├── policies_cleaned_final.json     # 清洗后数据(17份，所有分析基础)
│   ├── processed_policies.json         # 预处理后的数据
│   ├── word_frequency.txt              # 词频统计
│   ├── tfidf_results.json              # TF-IDF分析结果
│   ├── cooccurrence_matrix.csv         # 共现矩阵
│   ├── cooccurrence_edges.json         # 共现关系边列表
│   ├── keyword_similarity.json         # 关键词相似度
│   ├── category_keywords.json          # 各类别关键词
│   ├── lda_topics.json                 # LDA主题
│   ├── document_topics.json            # 文档主题分布
│   ├── topic_evolution.json            # 主题演化数据
│   ├── keyword_clusters.json           # 关键词聚类结果
│   ├── network_statistics.json         # 网络统计信息
│   ├── lda_statistics.json             # LDA统计信息
│   ├── analysis_summary.md             # 分析汇总报告
│   └── raw_policies/                   # 原始政策文本文件
│
├── figures/                            # 可视化图表目录（300 DPI高分辨率）
│   ├── cooccurrence_network.png        # 共现网络图
│   ├── keyword_clusters.png            # 关键词聚类图
│   ├── topic_distribution.png          # 主题分布饼图
│   ├── topic_evolution.png             # 主题演化时间线
│   ├── lda_topics_bar.png              # LDA主题条形图
│   └── category_keywords_heatmap.png   # 类别关键词热力图
│
├── Ref/                                # 参考文献目录
│   ├── TLDR.md                         # 文献总结（必读）
│   └── *.pdf                           # 参考论文PDF
│
├── ElegantPaper/                       # LaTeX论文模板
├── fonts/                              # 中文字体文件
└── jieba/                              # jieba分词库(本地)
```

## 快速开始

### 方式一：使用 pipeline（推荐）

完整的数据处理流水线已整理到 `pipeline/` 目录，包含详细文档和一键运行脚本。

```bash
# 1. 安装依赖
pip install -r pipeline/requirements.txt

# 2. 快速复现分析结果（推荐）
cd pipeline
bash run_pipeline.sh --quick

# 或分步运行
python3 3_analysis/text_preprocessing.py
python3 3_analysis/lda_analysis.py
python3 3_analysis/text_analysis.py
python3 3_analysis/visualization.py
python3 4_report/generate_summary_report.py
```

**详细说明请查看**：
- `pipeline/QUICKSTART.md` - 快速开始指南
- `pipeline/README.md` - 完整技术文档
- `PIPELINE.md` - 流水线概览

### 方式二：重新爬取数据（可选）

如果需要重新爬取政策数据：

```bash
cd pipeline/1_crawler

# 爬取所有双一流高校（需要较长时间）
python3 crawler_real.py

# 或限制数量进行测试
python3 crawler_real.py --max 5 --delay 3
```

**注意**：
- 已有完整的爬取数据，不建议重新爬取（需2-3小时）
- 爬虫依赖网络环境和搜索引擎可用性
- 建议直接使用已有数据进行分析

## 运行环境

- Python 3.11+
- 主要依赖包:
  - jieba (中文分词)
  - gensim (LDA主题模型)
  - scikit-learn (机器学习)
  - networkx (网络分析)
  - matplotlib, seaborn (可视化)
  - pandas, numpy (数据处理)
  - beautifulsoup4, requests (网络爬虫)

## 安装依赖

```bash
pip install -r requirements.txt
```

或使用以下命令安装主要依赖:

```bash
pip install beautifulsoup4 requests numpy pandas scikit-learn gensim networkx matplotlib seaborn scipy
```

**注**：如果jieba安装失败，项目已包含本地jieba库，会自动使用。

## 论文编译

LaTeX论文源文件为`国内双一流高校生成式人工智能相关政策分析.tex`。

### 使用 pipeline 编译（推荐）

```bash
cd pipeline/4_report
bash build_report.sh
```

### 手动编译

```bash
xelatex 国内双一流高校生成式人工智能相关政策分析.tex
xelatex 国内双一流高校生成式人工智能相关政策分析.tex  # 第二次编译以生成目录和引用
```

推荐使用XeLaTeX编译器以支持中文。

## 实用工具

`scripts/` 目录包含一些辅助工具脚本：

### 数据质量检查
```bash
python3 scripts/check_data_quality.py
```
检查原始数据质量，识别需要清洗的内容（URL、邮箱、可疑词等）。

### 从原始文件重建数据
```bash
python3 scripts/rebuild_policies.py
```
从 `data/raw_policies/` 目录重建 `policies.json` 文件。

详细说明请查看 `scripts/README.md`。

## 主要研究成果

### 数据规模

- **原始爬取**: 115份政策文档（来自147所双一流高校）
- **清洗筛选后**: 17份真实政策
- **覆盖高校**: 15所双一流高校
- **时间跨度**: 2017年至2025年
- **政策类别**: 教学管理(9份)、伦理规范(4份)、综合管理(2份)、教师指导(1份)、科研管理(1份)

### 高频关键词TOP10

1. 人工智能 (219次)
2. AI (100次)
3. 技术 (97次)
4. 使用 (89次)
5. 教育 (87次)
6. 服务 (84次)
7. 教学 (81次)
8. 学生 (64次)
9. 课程 (62次)
10. 生成式人工智能 (58次)

### 强共现关系TOP5

1. 项目 ↔ 申报 (0.95权重)
2. 论文 ↔ AIGC (0.92权重)
3. 我们 ↔ 服务 (0.88权重)
4. 教学改革 ↔ 项目 (0.73权重)
5. 项目 ↔ 附件 (0.58权重)

### 主题分析（LDA主题模型）

识别出5个核心主题：
- **主题0: 教学监管探索** - 关注AI在教学中的应用与监管
- **主题1: 服务与应用** - 聚焦AIGC工具的实际应用与规范
- **主题2: 课程项目建设** - 强调课程建设和教学改革项目
- **主题3: 平台素养培育** - 关注智能平台与师生AI素养
- **主题4: 课程教学赋能** - 强调AI赋能教学质量提升

## 核心方法说明

### 1. TF-IDF加权共词分析

参考魏澜等(2023)的方法:
- 使用TF-IDF算法计算词语权重
- 根据政策类别赋予文档权重(发展规划1.5,教学管理1.3,学生指导0.8等)
- 构建加权共现矩阵,窗口大小为5

### 2. LDA主题模型

参考楚东晓等(2022)的方法:
- 使用gensim库的LdaModel
- 主题数K=5
- 迭代次数100次
- 自动推断alpha参数

### 3. 语义网络分析

参考巴志超等(2022)和穆卫军等(2023)的方法:
- 基于共现矩阵构建无向加权网络
- 计算度中心性、介数中心性等指标
- 使用K-means聚类识别语义簇

## 可视化特性

**现代化学术出版风格**：
- 采用现代化学术出版风格，使用seaborn-v0_8-darkgrid样式
- 专业配色方案，包括viridis、plasma、RdYlBu等渐变色
- 高分辨率输出（300 DPI），适合学术出版
- 自动布局优化和详细标注
- 所有图表直接嵌入论文正文，提升可读性

**生成的6类图表**：
1. **共现网络图** (`cooccurrence_network.png`) - 显示关键词共现关系，节点大小基于度中心性，颜色基于介数中心性
2. **关键词聚类图** (`keyword_clusters.png`) - PCA降维+K-means聚类，展示语义簇分布
3. **主题分布饼图** (`topic_distribution.png`) - 显示17份政策的主题分布情况
4. **主题演化时间线** (`topic_evolution.png`) - 展示政策主题的时间演化趋势
5. **LDA主题条形图** (`lda_topics_bar.png`) - 5个主题的关键词概率分布
6. **类别-关键词热力图** (`category_keywords_heatmap.png`) - 不同政策类别的关键词分布热力图

## 双一流高校覆盖

项目包含完整的**147所双一流大学名单**（见 `pipeline/1_crawler/universities_list.py`），包含：
- 北京地区30所、上海地区15所、江苏地区16所等
- 涵盖985、211及新晋双一流高校
- 每所高校配置官网地址

## 参考文献

本研究参考了以下10篇文献(详见`Ref/TLDR.md`和论文参考文献部分):

1. 颜志萍 - 人工智能安全的公众认知研究
2. 魏澜 - 职业教育学生实习政策演变研究(加权共词分析)
3. 易璐 - 稀土产业政策演进研究(共词和语义网络分析)
4. 许世建 - 企业参与职业教育办学的政府注意力演化
5. 陈翔 - 基于动态语义网络的主题演化路径识别
6. 巴志超 - 基于关键词语义网络的领域主题演化分析
7. 刘滢 - "人类命运共同体"的国际社交媒体呈现
8. 俞立平 - 政策工具视角下科技创新质量政策演化
9. 楚东晓 - 基于LDA和语义网络的产品感知价值维度研究
10. 穆卫军 - 高等学历继续教育政策文本的语义网络分析

## 注意事项

1. **推荐工作流**: 使用 `pipeline/` 目录中的脚本和文档进行分析和复现

2. **数据说明**: 项目已包含完整的数据处理结果，建议直接使用，无需重新爬取

3. **中文字体**: 可视化图表已优化中文字体支持，如遇问题请检查系统字体配置

4. **LaTeX编译**: 建议使用XeLaTeX编译器，需要ctex宏包支持中文

5. **网络爬取**: 真实爬虫依赖网络环境和搜索引擎可用性，遵守网站robots.txt协议

## 项目亮点

1. ✅ **方法论完备**: 综合运用TF-IDF、LDA、语义网络等多种文本分析方法
2. ✅ **可视化现代化**: 使用现代化matplotlib样式，生成6类高质量出版级图表
3. ✅ **代码规范**: 采用面向对象设计,代码结构清晰,注释完善
4. ✅ **结果可信**: 参考权威文献方法,分析结论有理论支撑
5. ✅ **论文优化**: LaTeX论文结构完整，图表嵌入正文而非附录
6. ✅ **文档详尽**: 完善的文档体系，包含快速开始、技术文档、工具说明
7. ✅ **真实爬虫**: 实现完整的爬虫框架，支持真实数据采集
8. ✅ **全面覆盖**: 包含147所双一流大学完整名单，可扩展性强
9. ✅ **清洁流水线**: 整理完整的数据处理流水线，结构清晰，易于维护

## 致谢

本研究参考了《Ref/》目录下10篇优秀论文的研究方法和分析框架,特此致谢。

## 许可证

本项目仅用于学术研究和教育目的。

**主要技术栈**: Python, jieba, gensim, scikit-learn, networkx, matplotlib, beautifulsoup4, requests, LaTeX

**联系方式**: 如有问题请通过GitHub Issues联系
