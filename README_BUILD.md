# 一键编译PDF工作流使用说明

本项目提供了一键编译PDF报告的自动化工作流，可以自动完成从数据分析到PDF生成的全过程。

## 快速开始

### 方式1: 使用Bash脚本（推荐用于Linux/macOS）

```bash
./build_report.sh
```

### 方式2: 使用Python脚本（跨平台）

```bash
python build_report.py
```

或者：

```bash
./build_report.py
```

## 工作流程

脚本会自动执行以下步骤：

1. **检查Python依赖** - 确保所有必需的Python库已安装
2. **文本预处理** - 如果需要，运行文本预处理脚本
3. **数据分析** - 依次运行：
   - LDA主题模型分析
   - TF-IDF和共现网络分析
   - 可视化图表生成
   - 数据汇总报告生成
4. **LaTeX编译** - 将LaTeX文档编译为PDF
5. **清理临时文件** - 删除LaTeX编译生成的临时文件

## 环境要求

### Python依赖

- Python 3.7+
- numpy
- pandas
- matplotlib
- seaborn
- networkx
- scikit-learn
- gensim
- jieba

脚本会自动检查并安装缺失的依赖。

### LaTeX环境

需要安装以下之一：
- XeLaTeX（推荐，支持中文）
- PDFLaTeX

#### Ubuntu/Debian安装：
```bash
sudo apt-get install texlive-xetex texlive-lang-chinese
```

#### macOS安装：
```bash
brew install --cask mactex
```

#### Windows安装：
下载并安装 [TeX Live](https://www.tug.org/texlive/) 或 [MiKTeX](https://miktex.org/)

## 输出文件

成功运行后，会生成以下文件：

- **PDF报告**: `国内双一流高校生成式人工智能相关政策分析.pdf`
- **图表文件**: `figures/` 目录
  - `cooccurrence_network.png` - 共现网络图
  - `keyword_clusters.png` - 关键词聚类图
  - `topic_distribution.png` - 主题分布图
  - `topic_evolution.png` - 主题演化图
  - `lda_topics_bar.png` - LDA主题条形图
  - `category_keywords_heatmap.png` - 类别关键词热力图
- **数据文件**: `data/` 目录
  - `analysis_summary.md` - Markdown格式的数据汇总报告
  - 各种JSON格式的分析结果

## 字体说明

本项目使用思源黑体（Source Han Sans SC）来正确显示图表中的中文字符。字体文件位于 `fonts/` 目录：

- `SourceHanSansSC-Regular.otf` - 常规字体
- `SourceHanSansSC-Bold.otf` - 粗体字体

这些字体会在运行可视化脚本时自动加载。

## 单独运行各个步骤

如果需要单独运行某个步骤，可以使用以下命令：

```bash
# 1. 文本预处理
python text_preprocessing.py

# 2. LDA主题模型分析
python lda_analysis.py

# 3. TF-IDF和共现网络分析
python text_analysis.py

# 4. 生成可视化图表
python visualization.py

# 5. 生成数据汇总报告
python generate_summary_report.py

# 6. 编译LaTeX为PDF
xelatex -interaction=nonstopmode 国内双一流高校生成式人工智能相关政策分析.tex
xelatex -interaction=nonstopmode 国内双一流高校生成式人工智能相关政策分析.tex
```

## 故障排除

### 问题1: Python依赖安装失败

```bash
# 手动安装依赖
pip install numpy pandas matplotlib seaborn networkx scikit-learn gensim jieba
```

### 问题2: LaTeX编译失败

- 检查是否安装了LaTeX环境
- 确保安装了中文支持包
- 查看LaTeX日志文件（.log）了解详细错误信息

### 问题3: 图表中文显示为方框

- 确保 `fonts/` 目录下有思源黑体字体文件
- 重新运行 `python visualization.py`

### 问题4: 权限错误

```bash
# 添加执行权限
chmod +x build_report.sh
chmod +x build_report.py
```

## 更新报告

当数据更新后，只需重新运行构建脚本即可自动更新所有分析和PDF：

```bash
./build_report.sh
```

脚本会自动：
1. 重新运行所有分析
2. 更新所有图表
3. 重新编译PDF

## 技术支持

如有问题，请查看：
- 项目README.md
- 各脚本的注释文档
- Python和LaTeX的错误日志

## 许可证

本项目的字体文件（思源黑体）采用 SIL Open Font License 1.1 许可证。
