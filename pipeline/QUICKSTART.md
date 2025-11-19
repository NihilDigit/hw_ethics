# 快速开始指南

## 最简单的方式：使用现有数据

如果你只想复现分析结果和报告，**无需重新爬取和清洗数据**：

```bash
# 1. 进入项目根目录
cd /home/user/hw_ethics

# 2. 运行一键脚本（自动跳过爬虫和清洗）
./pipeline/run_pipeline.sh
```

脚本会自动：
- ✅ 检查环境和依赖
- ✅ 跳过爬虫（使用已有的 data/policies.json）
- ✅ 跳过清洗（使用已有的 data/policies_cleaned_final.json）
- ✅ 运行数据分析（文本预处理、LDA、TF-IDF、可视化）
- ✅ 生成报告（汇总报告 + PDF论文）

**预计用时**: 2-5分钟

## 手动运行各个阶段

如果你想分步骤运行：

### 阶段3：数据分析（从清洗后数据开始）

```bash
cd /home/user/hw_ethics

# 3.1 文本预处理
python3 pipeline/3_analysis/text_preprocessing.py

# 3.2 LDA主题模型
python3 pipeline/3_analysis/lda_analysis.py

# 3.3 TF-IDF和共现网络
python3 pipeline/3_analysis/text_analysis.py

# 3.4 可视化
python3 pipeline/3_analysis/visualization.py
```

### 阶段4：报告生成

```bash
cd /home/user/hw_ethics

# 4.1 生成汇总报告
python3 pipeline/4_report/generate_summary_report.py

# 4.2 编译PDF
./pipeline/4_report/build_report.sh
```

## 完整流程（从头开始）

⚠️ **警告**: 爬虫需要2-3小时，不建议重新运行！

```bash
# 1. 删除现有数据（谨慎操作！）
rm -f data/policies.json
rm -f data/policies_cleaned_final.json

# 2. 运行一键脚本，按提示选择是否爬取
./pipeline/run_pipeline.sh
```

## 验证结果

检查生成的文件：

```bash
# 查看分析数据
ls -lh data/*.json

# 查看可视化图表
ls -lh figures/

# 查看汇总报告
cat data/analysis_summary.md

# 查看PDF（如果生成成功）
ls -lh *.pdf
```

## 常见问题

**Q: 如何重新生成分析结果？**

删除分析中间文件，然后重新运行：
```bash
rm -f data/processed_policies.json
rm -rf figures/
./pipeline/run_pipeline.sh
```

**Q: PDF编译失败怎么办？**

检查LaTeX是否安装：
```bash
xelatex --version
```

如果未安装，可以只运行分析部分，跳过PDF编译。

**Q: 如何调整LDA主题数量？**

编辑 `pipeline/3_analysis/lda_analysis.py`，修改 `n_topics` 参数。

## 目录结构

```
pipeline/
├── 1_crawler/      # 爬虫脚本
├── 2_cleaning/     # 数据清洗
├── 3_analysis/     # 数据分析（←推荐从这里开始）
├── 4_report/       # 报告生成
├── README.md       # 详细文档
├── QUICKSTART.md   # 本文档
└── run_pipeline.sh # 一键运行脚本
```

## 更多信息

详细文档见 [README.md](README.md)
