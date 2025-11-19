# 实用工具脚本

本目录包含一些实用的辅助工具脚本，用于特殊场景下的数据检查和处理。

## 脚本说明

### check_data_quality.py
**用途**: 检查数据质量，识别需要清洗的内容

**功能**:
- 检查原始数据中的 URL、邮箱地址等需要清洗的内容
- 检查已处理数据中的可疑词（包含数字、特殊字符等）
- 检查 TF-IDF 关键词中的问题

**使用场景**:
- 在数据清洗前评估数据质量
- 验证清洗效果
- 调试分词和关键词提取问题

**运行方式**:
```bash
cd /home/user/hw_ethics
python3 scripts/check_data_quality.py
```

### rebuild_policies.py
**用途**: 从 `data/raw_policies/` 目录重建 `data/policies.json`

**功能**:
- 从原始的文本文件（.txt）中提取政策信息
- 重新构建 policies.json 文件
- 生成统计报告

**使用场景**:
- 当 policies.json 文件损坏或丢失时
- 需要从原始文本文件重新生成数据时
- 更新爬虫统计报告时

**运行方式**:
```bash
cd /home/user/hw_ethics
python3 scripts/rebuild_policies.py
```

**注意事项**:
- 该脚本依赖 `data/raw_policies/` 目录中的原始文本文件
- 会覆盖现有的 `data/policies.json` 文件
- 会生成或更新 `data/crawler_report_corrected.json`

## 注意事项

这些脚本不在主数据处理流水线（`pipeline/`）中，仅用于特殊场景。

如需运行主要的数据处理流程，请参考：
- `pipeline/README.md` - 详细技术文档
- `pipeline/QUICKSTART.md` - 快速开始指南
- `PIPELINE.md` - 流水线概览
