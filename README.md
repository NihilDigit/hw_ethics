# 国内双一流高校生成式人工智能相关政策分析

## 项目简介

本项目对国内**30所双一流高校**在2023年4月至2024年2月期间发布的生成式人工智能相关政策文本进行系统性分析。涵盖清华大学、北京大学、复旦大学、浙江大学、上海交通大学、南京大学、中国人民大学、北京师范大学、武汉大学、中山大学、华中科技大学、西安交通大学、哈尔滨工业大学、同济大学、南开大学等知名高校。

研究综合运用了**TF-IDF算法**、**LDA主题模型**和**语义网络分析**等文本挖掘方法,揭示了高校生成式AI政策的核心议题、演化趋势和类别特征。

## 主要研究发现

1. **政策演化趋势**: 从早期(2023年4-7月)的伦理规范导向,逐步转向中后期(2023年8月-2024年2月)的教学应用与创新导向

2. **核心议题**:
   - 数据安全与隐私保护
   - 学术诚信与伦理规范
   - 教学创新与评价改革
   - 师生AI素养培养

3. **关键词共现关系**:
   - "数据-智能-能力"构成核心主题簇
   - "教学-评价-体系"反映应用导向
   - "原则-伦理-规范"体现伦理关注

4. **LDA主题分析**: 识别出5个主题,所有政策聚焦"教学应用与创新"主题

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
│   │   └── universities_list.py        # 145所双一流高校名单
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

- **原始数据**: 115份政策文档
- **清洗后数据**: 17份高质量政策
- **覆盖高校**: 30所双一流高校
- **时间跨度**: 2023年4月-2024年2月
- **政策类别**: 教学管理、伦理规范、发展规划等

### 高频关键词TOP10

1. 人工智能 (185次)
2. 学生 (132次)
3. 技术 (98次)
4. 能力 (87次)
5. 教学 (76次)
6. 数据 (71次)
7. 应用 (69次)
8. 评价 (64次)
9. 工具 (58次)
10. 智能 (52次)

### 强共现关系TOP5

1. 数据 ↔ 智能 (高权重)
2. 能力 ↔ 评价 (高权重)
3. 教学 ↔ 体系 (高权重)
4. 原则 ↔ 伦理 (高权重)
5. 研究 ↔ 科研 (高权重)

### 语义聚类簇

通过K-means聚类识别出主要语义簇：
- **簇1**: 数据安全与智能应用
- **簇2**: 教学评价与体系建设
- **簇3**: 能力培养与研究创新
- **簇4**: 伦理规范与原则坚持

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
1. 共现网络图 - 现代化布局，节点大小基于度中心性，颜色基于介数中心性
2. 关键词聚类图 - PCA降维+K-means，展示解释方差比例
3. 主题分布饼图 - 带阴影和爆炸效果
4. 主题演化时间线 - 彩色主题标记，带图例
5. LDA主题条形图 - 多子图布局，概率标注
6. 类别-关键词热力图 - 现代配色方案

## 双一流高校覆盖

项目包含完整的**145所双一流大学名单**（见 `pipeline/1_crawler/universities_list.py`），包含：
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

## 更新日志

### v2.1 (2024-11-19) - 项目结构清理
- 🗑️ 清理31个无用文件，减少约8000行代码
- 📁 创建 scripts/ 目录整理实用工具
- 📝 完善文档结构，突出 pipeline/ 主流程
- ✨ 项目结构更清晰，易于维护和使用

### v2.0 (2024-11) - 现代化图表与报告优化
- ✨ 使用现代化matplotlib样式重写可视化代码
- ✨ 图表采用出版级质量，300 DPI高分辨率
- ✨ LaTeX报告优化，图表嵌入正文而非附录
- ✨ 添加详细的图表说明和标注
- ✨ 改进图表配色方案，使用专业学术配色
- 📝 完善pipeline文档，添加QUICKSTART和README

### v1.0 (2024-11) - 数据流水线整理
- 🔧 整理完整数据处理流水线到独立目录
- 📚 添加pipeline详细文档
- 🐛 修复数据清洗脚本
- ✅ 完成真实爬虫框架

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
8. ✅ **全面覆盖**: 包含145所双一流大学完整名单，可扩展性强
9. ✅ **清洁流水线**: 整理完整的数据处理流水线，结构清晰，易于维护

## 致谢

本研究参考了《Ref/》目录下10篇优秀论文的研究方法和分析框架,特此致谢。

## 许可证

本项目仅用于学术研究和教育目的。

---

**项目完成时间**: 2024年11月

**主要技术栈**: Python, jieba, gensim, scikit-learn, networkx, matplotlib, beautifulsoup4, requests, LaTeX

**联系方式**: 如有问题请通过GitHub Issues联系
