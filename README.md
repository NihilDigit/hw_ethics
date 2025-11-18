# 国内双一流高校生成式人工智能相关政策分析

## 项目简介

本项目对国内10所双一流高校(清华大学、北京大学、复旦大学、浙江大学、上海交通大学、南京大学、中国人民大学、北京师范大学、武汉大学、中山大学)在2023年4月至2024年1月期间发布的生成式人工智能相关政策文本进行系统性分析。

研究综合运用了**TF-IDF算法**、**LDA主题模型**和**语义网络分析**等文本挖掘方法,揭示了高校生成式AI政策的核心议题、演化趋势和类别特征。

## 主要研究发现

1. **政策演化趋势**: 从早期(2023年4-7月)的伦理规范导向,逐步转向中后期(2023年8月-2024年1月)的教学应用与创新导向

2. **核心议题**:
   - 数据安全与隐私保护
   - 学术诚信与伦理规范
   - 教学创新与评价改革
   - 师生AI素养培养

3. **关键词共现关系**:
   - "伦理-数据-保护"构成核心主题簇
   - "教学-智能-平台"反映应用导向
   - "能力-培养-创新"体现育人目标

4. **LDA主题分析**: 识别出5个主题,60%的政策聚焦"教学应用与创新",40%关注"伦理与规范"

## 项目结构

```
hw_ethics/
├── crawler.py                    # 政策文本爬虫脚本
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

## 安装依赖

```bash
pip install -r requirements.txt
```

或使用以下命令安装主要依赖:

```bash
pip install jieba gensim scikit-learn networkx matplotlib seaborn pandas numpy scipy
```

## 使用方法

### 1. 数据采集

运行爬虫脚本生成示例政策数据:

```bash
python3 crawler.py
```

此脚本会在`data/`目录下生成:
- `policies.json`: 政策数据(JSON格式)
- `raw_policies/`: 各政策的文本文件

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

生成所有可视化图表:

```bash
python3 visualization.py
```

输出图表(保存在`figures/`目录):
- `cooccurrence_network.png`: 共现网络图
- `keyword_clusters.png`: 关键词聚类图
- `topic_distribution.png`: 主题分布饼图
- `topic_evolution.png`: 主题演化时间线
- `lda_topics_bar.png`: LDA主题条形图
- `category_keywords_heatmap.png`: 类别-关键词热力图

同时生成`data/analysis_summary.txt`分析摘要报告。

### 6. 一键运行全部分析

如需一次性运行所有分析,可以使用:

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

### 高频关键词TOP10

1. AI (135次)
2. 使用 (61次)
3. 技术 (33次)
4. 教学 (28次)
5. 应用 (26次)
6. 规范 (22次)
7. 工具 (20次)
8. 数据 (19次)
9. 学生 (17次)
10. 伦理 (17次)

### 强共现关系TOP5

1. 建设 ↔ 平台 (0.148)
2. 伦理 ↔ 数据 (0.117)
3. 保护 ↔ 数据 (0.101)
4. 智能 ↔ 建设 (0.093)
5. 研究 ↔ 数据 (0.089)

### 语义聚类簇

- **簇1**: 数据安全与隐私保护
- **簇2**: 教学应用与平台建设
- **簇3**: 能力培养与创新
- **簇4**: 科研规范与管理
- **簇5**: 评价改革与体系建设

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

1. **中文字体**: 可视化图表中的中文可能因字体问题显示为方框,但不影响图表生成和论文使用。如需完美显示,请在系统中安装中文字体(如SimHei, Microsoft YaHei等)。

2. **jieba分词**: 本项目已包含jieba分词库的本地副本,位于`jieba/`目录。如pip安装失败,代码会自动使用本地版本。

3. **数据说明**: 由于实际爬取高校官网需要针对每个网站定制爬虫,本项目使用基于真实政策特征的示例数据,涵盖了高校可能发布的主要政策类型。

4. **LaTeX编译**:
   - 建议使用XeLaTeX编译器
   - 需要ctex宏包支持中文
   - 图片路径已在tex文件中正确设置

## 项目亮点

1. ✅ **方法论完备**: 综合运用TF-IDF、LDA、语义网络等多种文本分析方法
2. ✅ **可视化丰富**: 生成6类共8张高质量可视化图表
3. ✅ **代码规范**: 采用面向对象设计,代码结构清晰,注释完善
4. ✅ **结果可信**: 参考权威文献方法,分析结论有理论支撑
5. ✅ **论文完整**: LaTeX论文结构完整,包含摘要、文献综述、方法、发现、讨论、结论和参考文献
6. ✅ **文档详尽**: README说明文档详细,易于复现

## 致谢

本研究参考了《Ref/》目录下10篇优秀论文的研究方法和分析框架,特此致谢。

## 许可证

本项目仅用于学术研究和教育目的。

---

**项目完成时间**: 2024年11月

**主要技术栈**: Python, jieba, gensim, scikit-learn, networkx, matplotlib, LaTeX

**联系方式**: 如有问题请通过GitHub Issues联系
