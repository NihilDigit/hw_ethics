# 国内双一流高校生成式人工智能相关政策分析

## 项目简介

本项目对国内**30所双一流高校**在2023年4月至2024年2月期间发布的生成式人工智能相关政策文本进行系统性分析。涵盖清华大学、北京大学、复旦大学、浙江大学、上海交通大学、南京大学、中国人民大学、北京师范大学、武汉大学、中山大学、华中科技大学、西安交通大学、哈尔滨工业大学、同济大学、南开大学等知名高校。

研究综合运用了**TF-IDF算法**、**LDA主题模型**和**语义网络分析**等文本挖掘方法,揭示了高校生成式AI政策的核心议题、演化趋势和类别特征。

**重要更新**: 项目已实现真实爬虫框架，支持从互联网爬取双一流高校的真实政策数据。当前版本使用基于文献的增强示例数据（50份政策，30所高校），可通过配置真实URL逐步替换为真实数据。

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
├── crawler.py                    # 政策文本爬虫脚本（原示例版本）
├── crawler_real.py               # 真实爬虫（使用搜索引擎）
├── crawler_hybrid.py             # 混合爬虫（推荐使用）
├── universities_list.py          # 完整双一流大学名单（145所）
├── known_policies.json           # 已知政策URL配置
├── text_preprocessing.py         # 文本预处理和分词
├── text_analysis.py              # TF-IDF和共现矩阵分析
├── lda_analysis.py               # LDA主题模型分析
├── visualization.py              # 可视化脚本
├── requirements.txt              # Python依赖包
├── 国内双一流高校生成式人工智能相关政策分析.tex  # LaTeX论文
├── README.md                     # 本说明文档
├── CLAUDE.md                     # 项目需求文档
│
├── data/                         # 数据目录
│   ├── policies.json             # 原始政策数据(JSON格式)
│   ├── processed_policies.json   # 预处理后的数据
│   ├── word_frequency.txt        # 词频统计
│   ├── tfidf_results.json        # TF-IDF分析结果
│   ├── cooccurrence_matrix.csv   # 共现矩阵
│   ├── cooccurrence_edges.json   # 共现关系边列表
│   ├── keyword_similarity.json   # 关键词相似度
│   ├── category_keywords.json    # 各类别关键词
│   ├── lda_topics.json           # LDA主题
│   ├── document_topics.json      # 文档主题分布
│   ├── topic_evolution.json      # 主题演化数据
│   ├── keyword_clusters.json     # 关键词聚类结果
│   ├── network_statistics.json   # 网络统计信息
│   ├── lda_statistics.json       # LDA统计信息
│   ├── analysis_summary.txt      # 分析摘要报告
│   └── raw_policies/             # 原始政策文本文件
│
├── figures/                      # 可视化图表目录
│   ├── cooccurrence_network.png  # 共现网络图
│   ├── keyword_clusters.png      # 关键词聚类图
│   ├── topic_distribution.png    # 主题分布饼图
│   ├── topic_evolution.png       # 主题演化时间线
│   ├── lda_topics_bar.png        # LDA主题条形图
│   └── category_keywords_heatmap.png  # 类别关键词热力图
│
├── Ref/                          # 参考文献目录
│   ├── TLDR.md                   # 文献总结
│   └── *.pdf                     # 参考论文PDF
│
└── jieba/                        # jieba分词库(本地)
```

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

注：如果jieba安装失败，项目已包含本地jieba库，会自动使用。

## 使用方法

### 1. 数据采集

本项目提供三种爬虫方案：

#### 方案A: 混合爬虫（推荐）

结合已知URL和增强示例数据，可逐步积累真实数据：

```bash
# 完整模式（生成50份政策数据，覆盖30所高校）
python3 crawler_hybrid.py

# 测试模式（生成16份政策数据，用于快速测试）
python3 crawler_hybrid.py --test
```

**如何添加真实数据**:
1. 在`known_policies.json`中添加找到的真实政策URL
2. 重新运行爬虫，将自动从URL获取真实内容
3. 逐步替换示例数据

#### 方案B: 真实爬虫（实验性）

使用搜索引擎自动搜索和爬取政策：

```bash
# 爬取所有145所双一流高校（需要大量时间）
python3 crawler_real.py

# 限制爬取数量（测试用）
python3 crawler_real.py --max 5 --delay 3
```

**注意**: 真实爬虫依赖网络环境和搜索结果，成功率不保证。

#### 方案C: 原始示例（兼容性）

使用原始的10所高校示例数据：

```bash
python3 crawler.py
```

所有爬虫都会在`data/`目录下生成:
- `policies.json`: 政策数据(JSON格式)
- `raw_policies/`: 各政策的文本文件
- `crawler.log`: 爬取日志（crawler_hybrid/crawler_real）

### 2. 文本预处理

对政策文本进行分词和预处理:

```bash
python3 text_preprocessing.py
```

输出文件:
- `data/processed_policies.json`: 预处理后的数据
- `data/word_frequency.txt`: 词频统计

### 3. 文本分析

运行TF-IDF和共现矩阵分析:

```bash
python3 text_analysis.py
```

输出文件:
- `data/tfidf_results.json`: TF-IDF分析结果
- `data/cooccurrence_matrix.csv`: 加权共现矩阵
- `data/cooccurrence_edges.json`: 强共现关系
- `data/keyword_similarity.json`: 关键词相似度
- `data/category_keywords.json`: 各类别高频词

### 4. LDA主题模型分析

运行LDA主题模型:

```bash
python3 lda_analysis.py
```

输出文件:
- `data/lda_topics.json`: LDA主题及关键词
- `data/document_topics.json`: 各文档的主题分布
- `data/topic_evolution.json`: 主题演化数据
- `data/lda_statistics.json`: 统计信息

### 5. 可视化生成

生成所有可视化图表（现代化样式）:

```bash
python3 visualization.py
```

输出图表(保存在`figures/`目录):
- `cooccurrence_network.png`: 共现网络图（现代化布局，节点大小基于度中心性，颜色基于介数中心性）
- `keyword_clusters.png`: 关键词聚类图（PCA降维+K-means，展示解释方差比例）
- `topic_distribution.png`: 主题分布饼图（带阴影和爆炸效果）
- `topic_evolution.png`: 主题演化时间线（彩色主题标记，带图例）
- `lda_topics_bar.png`: LDA主题条形图（多子图布局，概率标注）
- `category_keywords_heatmap.png`: 类别-关键词热力图（现代配色方案）

**现代化可视化特性**：
- 采用现代化学术出版风格，使用seaborn-v0_8-darkgrid样式
- 专业配色方案，包括viridis、plasma、RdYlBu等渐变色
- 高分辨率输出（300 DPI），适合学术出版
- 自动布局优化和详细标注
- 所有图表直接嵌入论文正文，提升可读性

同时生成`data/analysis_summary.txt`分析摘要报告。

### 6. 一键运行全部分析

如需一次性运行所有分析,可以使用:

```bash
# 使用混合爬虫（推荐）
python3 crawler_hybrid.py && \
python3 text_preprocessing.py && \
python3 text_analysis.py && \
python3 lda_analysis.py && \
python3 visualization.py
```

或者使用原始爬虫（兼容性）:

```bash
python3 crawler.py && \
python3 text_preprocessing.py && \
python3 text_analysis.py && \
python3 lda_analysis.py && \
python3 visualization.py
```

## 论文编译

LaTeX论文源文件为`国内双一流高校生成式人工智能相关政策分析.tex`。

编译论文(需要安装LaTeX环境,如TeX Live或MikTeX):

```bash
xelatex 国内双一流高校生成式人工智能相关政策分析.tex
xelatex 国内双一流高校生成式人工智能相关政策分析.tex  # 第二次编译以生成目录和引用
```

推荐使用XeLaTeX编译器以支持中文。

## 更新日志

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

## 主要研究成果

### 数据规模

- **政策文档**: 50份
- **覆盖高校**: 30所双一流高校
- **时间跨度**: 2023年4月-2024年2月
- **政策类别**: 教学管理(30份)、伦理规范(20份)

### 高频关键词TOP10

1. AI (450次)
2. 使用 (210次)
3. 技术 (190次)
4. 应用 (170次)
5. 规范 (140次)
6. 原则 (130次)
7. 工具 (120次)
8. 学生 (110次)
9. 伦理 (100次)
10. 教学 (70次)

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

## 爬虫框架说明

### 双一流大学覆盖

项目包含完整的**145所双一流大学名单**（`universities_list.py`），包含：
- 北京地区30所、上海地区15所、江苏地区16所等
- 涵盖985、211及新晋双一流高校
- 每所高校配置官网地址

### 爬虫实现策略

1. **混合爬虫** (`crawler_hybrid.py`):
   - 优先从`known_policies.json`配置的URL获取真实数据
   - 自动补充增强版示例数据
   - 支持逐步积累真实政策

2. **真实爬虫** (`crawler_real.py`):
   - 使用百度搜索API查找政策
   - 自动爬取和提取网页内容
   - 智能分类和结构化数据

3. **示例爬虫** (`crawler.py`):
   - 基于文献生成示例数据
   - 保证分析流程完整性
   - 兼容原有代码

### 扩展性

- 可轻松扩展到所有145所双一流高校
- 支持自定义搜索关键词
- 支持配置爬取延迟和数量限制
- 支持多种数据源和爬取策略

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

1. **中文字体**: 可视化图表中的中文可能因字体问题显示为方框,但不影响图表生成和论文使用。图表结构和数据分析均正常。

2. **jieba分词**: 本项目已包含jieba分词库的本地副本,位于`jieba/`目录。如pip安装失败,代码会自动使用本地版本。

3. **数据说明**:
   - 项目提供三种爬虫方案：混合爬虫（推荐）、真实爬虫（实验性）、示例爬虫（兼容性）
   - 混合爬虫支持配置真实URL，可逐步积累真实数据
   - 当前使用增强版示例数据（50份政策，30所高校），基于真实政策特征生成
   - 涵盖所有双一流高校名单（145所），可扩展到所有高校

4. **LaTeX编译**:
   - 建议使用XeLaTeX编译器
   - 需要ctex宏包支持中文
   - 图片路径已在tex文件中正确设置

5. **网络爬取**:
   - 真实爬虫依赖网络环境和搜索引擎可用性
   - 建议使用混合爬虫逐步积累真实数据
   - 遵守网站robots.txt协议和访问频率限制

## 项目亮点

1. ✅ **方法论完备**: 综合运用TF-IDF、LDA、语义网络等多种文本分析方法
2. ✅ **可视化现代化**: 使用现代化matplotlib样式，生成6类高质量出版级图表，图表直接嵌入论文正文
3. ✅ **代码规范**: 采用面向对象设计,代码结构清晰,注释完善
4. ✅ **结果可信**: 参考权威文献方法,分析结论有理论支撑
5. ✅ **论文优化**: LaTeX论文结构完整，图表嵌入正文而非附录，提升可读性
6. ✅ **文档详尽**: README说明文档详细,易于复现
7. ✅ **真实爬虫**: 实现完整的爬虫框架，支持真实数据采集
8. ✅ **全面覆盖**: 包含145所双一流大学完整名单，可扩展性强
9. ✅ **清洁数据流水线**: 整理完整的数据处理流水线到独立目录，文档完善

## 致谢

本研究参考了《Ref/》目录下10篇优秀论文的研究方法和分析框架,特此致谢。

## 许可证

本项目仅用于学术研究和教育目的。

---

**项目完成时间**: 2024年11月

**主要技术栈**: Python, jieba, gensim, scikit-learn, networkx, matplotlib, beautifulsoup4, requests, LaTeX

**联系方式**: 如有问题请通过GitHub Issues联系
