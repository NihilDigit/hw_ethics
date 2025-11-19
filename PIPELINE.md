# 数据处理流水线说明

本文档说明如何使用 `pipeline/` 目录中整理好的数据处理流水线复现项目结果。

## 📌 重要说明

本项目的数据处理流程已经完整运行过一次，所有中间数据和最终结果都已保存。**推荐直接使用已有数据**，无需重新爬取。

## 🎯 快速复现分析结果

如果你想验证或复现数据分析结果：

```bash
# 1. 删除分析中间文件（保留清洗后的数据）
rm -f data/processed_policies.json
rm -f data/lda_*.json data/tfidf_*.json data/cooccurrence_*.json
rm -f data/keyword_*.json data/analysis_summary.md
rm -rf figures/

# 2. 重新运行分析流程
python3 pipeline/3_analysis/text_preprocessing.py
python3 pipeline/3_analysis/lda_analysis.py
python3 pipeline/3_analysis/text_analysis.py
python3 pipeline/3_analysis/visualization.py
python3 pipeline/4_report/generate_summary_report.py
```

**预计用时**: 2-3分钟

## 📂 pipeline目录结构

```
pipeline/
├── 1_crawler/              # 爬虫脚本（不建议重新运行）
├── 2_cleaning/             # 数据清洗脚本（不建议重新运行）
├── 3_analysis/             # 数据分析脚本（可重复运行）
├── 4_report/               # 报告生成脚本（可重复运行）
├── README.md               # 详细技术文档
├── QUICKSTART.md           # 快速开始指南
└── run_pipeline.sh         # 一键运行脚本
```

## 🔄 完整数据流

```
原始数据 (data/policies.json)
    ↓ [阶段1: 爬虫 - 已完成]
    ↓
清洗数据 (data/policies_cleaned_final.json)
    ↓ [阶段2: 清洗 - 已完成]
    ↓ ← 从这里开始复现 ←
    ↓
预处理数据 (data/processed_policies.json)
    ↓ [阶段3: 分析]
    ├→ LDA主题模型 → data/lda_topics.json
    ├→ TF-IDF分析 → data/tfidf_results.json
    ├→ 共现网络 → data/cooccurrence_edges.json
    └→ 可视化 → figures/*.png
    ↓ [阶段4: 报告]
    ├→ 汇总报告 → data/analysis_summary.md
    └→ LaTeX编译 → 国内双一流高校生成式人工智能相关政策分析.pdf
```

## 📊 数据文件说明

### 固化数据（不要修改）
- `data/policies.json` - 爬虫原始数据（115份文档）
- `data/policies_cleaned_final.json` - 清洗后数据（所有分析的基础）

### 可重新生成的数据
- `data/processed_policies.json` - 预处理数据
- `data/lda_topics.json` - LDA主题
- `data/tfidf_results.json` - TF-IDF结果
- `data/cooccurrence_edges.json` - 共现网络
- `data/keyword_similarity.json` - 关键词相似度
- `data/analysis_summary.md` - 汇总报告
- `figures/*.png` - 所有可视化图表

## 🛠️ 环境要求

### Python依赖
```bash
pip install -r pipeline/requirements.txt
```

主要依赖：
- jieba - 中文分词
- gensim - LDA主题模型
- scikit-learn - TF-IDF和聚类
- networkx - 网络分析
- matplotlib, seaborn - 可视化

### LaTeX（可选，用于PDF编译）
- xelatex 或 pdflatex
- 中文字体支持

## ✅ 验证复现成功

运行分析后，检查以下文件是否生成：

```bash
# 检查数据文件
ls -lh data/processed_policies.json
ls -lh data/lda_topics.json
ls -lh data/tfidf_results.json

# 检查可视化图表
ls -lh figures/

# 查看汇总报告
cat data/analysis_summary.md
```

预期结果：
- ✅ 17份政策文档预处理完成
- ✅ 识别出5个LDA主题
- ✅ 生成6张可视化图表
- ✅ 生成数据汇总报告

## 🔍 分析参数调整

如果需要调整分析参数：

### LDA主题数量
编辑 `pipeline/3_analysis/lda_analysis.py`:
```python
n_topics = 5  # 修改这里，默认为5
```

### TF-IDF关键词数量
编辑 `pipeline/3_analysis/text_analysis.py`:
```python
max_features = 100  # 修改这里，默认为100
```

### 可视化显示的关键词数量
编辑 `pipeline/3_analysis/visualization.py`:
```python
top_n = 20  # 修改这里，默认为20
```

## 📝 完整文档

- **技术文档**: `pipeline/README.md` - 详细的技术说明和API文档
- **快速指南**: `pipeline/QUICKSTART.md` - 快速开始指南
- **本文档**: `PIPELINE.md` - 概览和复现说明

## 🐛 常见问题

### Q: 为什么不建议重新爬取？
A: 爬虫需要2-3小时，且网站内容可能已变化，结果不可复现。

### Q: 分析结果为什么和之前不完全一样？
A: 某些算法（如LDA）有随机性，但设置了random_seed=42确保大致相同。

### Q: 可以只运行某一个分析脚本吗？
A: 可以，但需要按顺序运行：text_preprocessing → lda_analysis/text_analysis → visualization

### Q: 如何重新编译PDF？
A: 运行 `./pipeline/4_report/build_report.sh`

## 📄 引用

如果使用本数据处理流水线，请引用：

```
国内双一流高校生成式人工智能相关政策分析
数据处理流水线 v1.0
2024年
```

---

**最后更新**: 2024-11-19
**维护者**: 项目团队
