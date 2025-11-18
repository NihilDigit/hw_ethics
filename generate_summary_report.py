#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成数据汇总报告
"""

import json
from collections import defaultdict
from datetime import datetime

def generate_analysis_summary():
    """生成完整的数据分析汇总报告"""

    # 读取数据文件
    with open('data/processed_policies.json', 'r', encoding='utf-8') as f:
        policies = json.load(f)

    with open('data/lda_topics.json', 'r', encoding='utf-8') as f:
        lda_topics = json.load(f)

    with open('data/cooccurrence_edges.json', 'r', encoding='utf-8') as f:
        cooccurrence = json.load(f)

    with open('data/category_keywords.json', 'r', encoding='utf-8') as f:
        category_keywords = json.load(f)

    # 读取高频词
    word_freq = []
    with open('data/word_frequency.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # 跳过标题行
        for line in lines[:50]:  # 只取前50个
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    word_freq.append((parts[0], int(parts[1])))

    # 生成Markdown报告
    report = []

    # 标题和元信息
    report.append("# 国内双一流高校生成式AI政策数据分析汇总报告\n")
    report.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
    report.append(f"**数据来源**: 17个真实政策文件，来自15所双一流高校\n")
    report.append("\n---\n")

    # 第1部分：政策文档列表
    report.append("\n## 一、政策文档列表\n")
    report.append(f"\n共收集 **{len(policies)}** 个政策文件，涵盖 **{len(set(p['university'] for p in policies))}** 所双一流高校。\n")

    # 按大学分组
    policies_by_uni = defaultdict(list)
    for policy in policies:
        policies_by_uni[policy['university']].append(policy)

    # 统计各类别数量
    category_counts = defaultdict(int)
    for policy in policies:
        category_counts[policy['category']] += 1

    report.append("\n### 1.1 政策分类统计\n")
    report.append("\n| 类别 | 文件数量 |\n")
    report.append("|------|----------|\n")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {category} | {count} |\n")

    report.append("\n### 1.2 各高校政策详情\n")
    for university in sorted(policies_by_uni.keys()):
        report.append(f"\n#### {university}\n")
        for policy in policies_by_uni[university]:
            report.append(f"\n- **标题**: {policy['title']}\n")
            report.append(f"  - **日期**: {policy['date']}\n")
            report.append(f"  - **分类**: {policy['category']}\n")
            report.append(f"  - **目标角色**: {policy.get('target_role', '未指定')}\n")
            report.append(f"  - **字数**: {policy.get('word_count', 0)}\n")

    # 第2部分：高频词统计
    report.append("\n---\n")
    report.append("\n## 二、高频词统计分析\n")
    report.append("\n### 2.1 Top 50 高频词汇\n")
    report.append("\n以下是所有政策文本中出现频次最高的50个词汇：\n")
    report.append("\n| 排名 | 词语 | 频次 |\n")
    report.append("|------|------|------|\n")
    for idx, (word, freq) in enumerate(word_freq, 1):
        report.append(f"| {idx} | {word} | {freq} |\n")

    # Top 10 词汇分析
    report.append("\n### 2.2 核心词汇分析\n")
    report.append("\n**Top 10 核心词汇**:\n")
    for idx, (word, freq) in enumerate(word_freq[:10], 1):
        report.append(f"{idx}. **{word}** ({freq}次)\n")

    report.append("\n从高频词可以看出，政策文本主要关注：\n")
    report.append("- **技术关键词**: 人工智能、AI、生成式人工智能、AIGC、技术\n")
    report.append("- **教育关键词**: 教学、教育、课程、学生、教师\n")
    report.append("- **管理关键词**: 服务、平台、项目、管理、规范\n")

    # 第3部分：LDA主题模型
    report.append("\n---\n")
    report.append("\n## 三、LDA主题模型分析\n")
    report.append(f"\n通过LDA主题模型分析，识别出 **{len(lda_topics)}** 个主要主题：\n")

    for topic in lda_topics:
        topic_id = topic['topic_id']
        keywords = topic['keywords'][:10]  # 取前10个关键词

        report.append(f"\n### 3.{topic_id + 1} 主题 {topic_id}\n")
        report.append("\n| 关键词 | 权重 |\n")
        report.append("|--------|------|\n")
        for word, weight in keywords:
            report.append(f"| {word} | {weight:.4f} |\n")

        # 主题解读
        top_words = [w for w, _ in keywords[:5]]
        report.append(f"\n**主题特征**: {', '.join(top_words)}\n")

    # 主题总结
    report.append("\n### 3.6 主题总结\n")
    report.append("\n基于LDA主题模型分析，可以识别出以下主要主题方向：\n")
    report.append("- **主题0**: 服务与应用 - 关注AI服务的使用和监管\n")
    report.append("- **主题1**: 学术规范 - 强调学术素养和使用规范\n")
    report.append("- **主题2**: 课程项目 - 聚焦课程建设和项目申报\n")
    report.append("- **主题3**: 教学探索 - 探索AI在教学中的应用\n")
    report.append("- **主题4**: 平台资源 - 提供AI工具平台和资源导航\n")

    # 第4部分：共现关系分析
    report.append("\n---\n")
    report.append("\n## 四、词汇共现关系分析\n")
    report.append("\n### 4.1 Top 20 共现词对\n")
    report.append("\n以下是权重最高的20对共现词汇：\n")
    report.append("\n| 排名 | 词语1 | 词语2 | 共现权重 |\n")
    report.append("|------|-------|-------|----------|\n")

    for idx, edge in enumerate(cooccurrence[:20], 1):
        report.append(f"| {idx} | {edge['word1']} | {edge['word2']} | {edge['weight']:.4f} |\n")

    # 共现关系分析
    report.append("\n### 4.2 共现关系解读\n")
    report.append("\n**关键共现模式**:\n")
    report.append("\n1. **学术诚信相关**: 论文-AIGC、学位-AIGC、学术-AIGC\n")
    report.append("   - 反映高校对AI工具在学术写作中使用的关注\n")
    report.append("\n2. **项目管理相关**: 申报-项目、教学改革-项目、通知-项目\n")
    report.append("   - 显示高校通过项目推动AI在教学中的应用\n")
    report.append("\n3. **培训支持相关**: 培训-讲座、系列-培训、举办-培训\n")
    report.append("   - 说明高校重视师生AI素养培训\n")
    report.append("\n4. **平台服务相关**: https-com、平台-导航、助手-com\n")
    report.append("   - 体现高校提供AI工具平台和资源导航服务\n")

    # 第5部分：类别关键词分析
    report.append("\n---\n")
    report.append("\n## 五、按类别的关键词分析\n")
    report.append("\n根据政策文件的分类，提取各类别的核心关键词（Top 15）：\n")

    category_order = ["教学管理", "伦理规范", "科研管理", "综合管理", "教师指导"]

    for category in category_order:
        if category in category_keywords:
            keywords = category_keywords[category][:15]

            report.append(f"\n### 5.{category_order.index(category) + 1} {category}\n")
            report.append("\n| 排名 | 关键词 | 频次 |\n")
            report.append("|------|--------|------|\n")

            for idx, (word, freq) in enumerate(keywords, 1):
                report.append(f"| {idx} | {word} | {freq} |\n")

            # 类别特征总结
            top_5_words = [w for w, _ in keywords[:5]]
            report.append(f"\n**核心特征**: {', '.join(top_5_words)}\n")

    # 第6部分：总体分析结论
    report.append("\n---\n")
    report.append("\n## 六、总体分析结论\n")

    report.append("\n### 6.1 政策关注重点\n")
    report.append("\n通过对17个政策文件的综合分析，可以看出国内双一流高校在生成式AI政策方面主要关注：\n")
    report.append("\n1. **教学应用** (教学管理类文件最多)\n")
    report.append("   - AI工具在课程教学中的应用\n")
    report.append("   - 教学改革项目的申报与建设\n")
    report.append("   - 教学平台和资源的提供\n")

    report.append("\n2. **学术规范** (伦理规范类关注度高)\n")
    report.append("   - AIGC在论文写作中的使用规范\n")
    report.append("   - 学术诚信和学术不端问题\n")
    report.append("   - 学位论文的AI使用指导\n")

    report.append("\n3. **能力培养** (培训讲座频繁出现)\n")
    report.append("   - 师生AI素养提升\n")
    report.append("   - 定期举办培训和讲座\n")
    report.append("   - 提供学习资源和案例分享\n")

    report.append("\n4. **服务支持** (平台建设受重视)\n")
    report.append("   - AI工具平台和助手服务\n")
    report.append("   - 资源导航和专题网站\n")
    report.append("   - 技术支持和咨询服务\n")

    report.append("\n### 6.2 政策发展趋势\n")
    report.append("\n- **规范先行**: 多所高校制定了AI使用规范和学术指南\n")
    report.append("- **应用推广**: 通过项目资助鼓励AI在教学中的创新应用\n")
    report.append("- **能力建设**: 重视师生AI素养的系统培养\n")
    report.append("- **平台赋能**: 建设校级AI平台，提供统一服务\n")
    report.append("- **风险管控**: 关注AI使用的监管和安全问题\n")

    report.append("\n### 6.3 数据统计概览\n")
    report.append("\n| 统计项 | 数值 |\n")
    report.append("|--------|------|\n")
    report.append(f"| 政策文件总数 | {len(policies)} |\n")
    report.append(f"| 涵盖高校数量 | {len(policies_by_uni)} |\n")
    report.append(f"| 识别主题数量 | {len(lda_topics)} |\n")
    report.append(f"| 高频词汇数量 | {len(word_freq)} |\n")
    report.append(f"| 共现关系数量 | {len(cooccurrence)} |\n")
    report.append(f"| 政策类别数量 | {len(category_keywords)} |\n")

    # 附录
    report.append("\n---\n")
    report.append("\n## 附录：数据文件说明\n")
    report.append("\n本报告基于以下数据文件生成：\n")
    report.append("\n- `data/processed_policies.json`: 处理后的政策文件信息\n")
    report.append("- `data/word_frequency.txt`: 词频统计结果\n")
    report.append("- `data/lda_topics.json`: LDA主题模型分析结果\n")
    report.append("- `data/cooccurrence_edges.json`: 词汇共现关系数据\n")
    report.append("- `data/category_keywords.json`: 分类关键词统计\n")

    report.append("\n---\n")
    report.append("\n*报告生成完毕*\n")

    # 保存报告
    with open('data/analysis_summary.md', 'w', encoding='utf-8') as f:
        f.write(''.join(report))

    print("✓ 数据汇总报告已生成: data/analysis_summary.md")
    print(f"✓ 报告总长度: {len(''.join(report))} 字符")

if __name__ == '__main__':
    generate_analysis_summary()
