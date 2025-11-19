#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义网络可视化 - 现代化版本
使用现代化matplotlib样式，提供出版质量的图表
参考文献⑤⑥⑦⑩的可视化方法
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.cluster import KMeans
from collections import Counter
import os
from matplotlib.font_manager import FontProperties, fontManager
import matplotlib.patches as mpatches

# 注册思源黑体字体
font_path = os.path.join(os.path.dirname(__file__), '..', '..', 'fonts', 'SourceHanSansSC-Regular.otf')
font_path_bold = os.path.join(os.path.dirname(__file__), '..', '..', 'fonts', 'SourceHanSansSC-Bold.otf')

if os.path.exists(font_path):
    # 添加字体到系统
    fontManager.addfont(font_path)
    fontManager.addfont(font_path_bold)
    print("✓ 成功加载思源黑体字体")
else:
    print("⚠ 警告: 未找到思源黑体字体，使用默认字体")

# 设置现代化样式
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 全局样式设置 - 现代化学术出版风格
plt.rcParams.update({
    # 字体设置
    'font.family': 'sans-serif',
    'font.sans-serif': ['Source Han Sans SC', 'DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,

    # 颜色和样式
    'axes.facecolor': '#f8f9fa',
    'figure.facecolor': 'white',
    'axes.edgecolor': '#2c3e50',
    'axes.linewidth': 1.2,
    'grid.color': '#bdc3c7',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.3,

    # 其他设置
    'axes.unicode_minus': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.autolayout': False,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# 定义现代化配色方案
COLORS = {
    'primary': '#3498db',      # 蓝色
    'secondary': '#e74c3c',    # 红色
    'success': '#2ecc71',      # 绿色
    'warning': '#f39c12',      # 橙色
    'info': '#9b59b6',         # 紫色
    'palette': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#d35400'],
    'gradient': 'viridis',     # 现代渐变色
}

class ModernVisualizer:
    """现代化可视化类"""

    def __init__(self):
        self.output_dir = 'figures'
        os.makedirs(self.output_dir, exist_ok=True)
        print("✓ 初始化现代化可视化器")

    def load_data(self):
        """加载分析结果数据"""
        print("\n⏳ 加载数据...")

        # 加载共现边
        with open('data/cooccurrence_edges.json', 'r', encoding='utf-8') as f:
            self.edges = json.load(f)

        # 加载LDA主题
        with open('data/lda_topics.json', 'r', encoding='utf-8') as f:
            self.topics = json.load(f)

        # 加载文档主题
        with open('data/document_topics.json', 'r', encoding='utf-8') as f:
            self.doc_topics = json.load(f)

        # 加载类别关键词
        with open('data/category_keywords.json', 'r', encoding='utf-8') as f:
            self.category_keywords = json.load(f)

        print("✓ 数据加载完成")

    def plot_cooccurrence_network(self, top_n=50):
        """
        绘制现代化共现网络图
        使用更好的布局和配色
        """
        print(f"\n📊 绘制共现网络图 (Top {top_n} edges)...")

        # 创建网络图
        G = nx.Graph()

        # 添加边
        for edge in self.edges[:top_n]:
            G.add_edge(edge['word1'], edge['word2'], weight=edge['weight'])

        # 计算中心性指标
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)

        # 节点大小基于度中心性
        node_sizes = [degree_centrality[node] * 4000 + 500 for node in G.nodes()]

        # 节点颜色基于介数中心性
        node_colors = [betweenness_centrality[node] for node in G.nodes()]

        # 使用Kamada-Kawai布局（更优雅）
        try:
            pos = nx.kamada_kawai_layout(G)
        except:
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

        # 创建图形
        fig, ax = plt.subplots(figsize=(18, 14))

        # 绘制边（带透明度渐变）
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        max_weight = max(weights) if weights else 1

        for (u, v), weight in zip(edges, weights):
            alpha = 0.1 + 0.6 * (weight / max_weight)
            width = 0.5 + 3 * (weight / max_weight)
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                   'k-', alpha=alpha, linewidth=width, zorder=1)

        # 绘制节点
        scatter = ax.scatter([pos[node][0] for node in G.nodes()],
                           [pos[node][1] for node in G.nodes()],
                           s=node_sizes,
                           c=node_colors,
                           cmap='plasma',
                           alpha=0.85,
                           edgecolors='white',
                           linewidths=2,
                           zorder=2)

        # 添加颜色条
        cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Betweenness Centrality', rotation=270, labelpad=20)

        # 绘制标签（只标注重要节点）
        top_nodes = sorted(degree_centrality.items(),
                          key=lambda x: x[1], reverse=True)[:20]
        for node, _ in top_nodes:
            ax.annotate(node,
                       xy=pos[node],
                       xytext=(5, 5),
                       textcoords='offset points',
                       fontsize=10,
                       fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3',
                               facecolor='white',
                               edgecolor='gray',
                               alpha=0.8),
                       zorder=3)

        ax.set_title('Policy Keywords Co-occurrence Network\n' +
                    f'Top {top_n} Co-occurring Pairs',
                    fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')

        plt.tight_layout()
        output_path = f'{self.output_dir}/cooccurrence_network.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ 共现网络图已保存: {output_path}")
        plt.close()

        # 保存网络统计
        self.save_network_statistics(G)

    def save_network_statistics(self, G):
        """保存网络统计信息"""
        stats = {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': nx.density(G),
            'avg_clustering': nx.average_clustering(G)
        }

        # 中心性分析
        degree_cent = nx.degree_centrality(G)
        betweenness_cent = nx.betweenness_centrality(G)

        # Top 10 节点
        top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]
        top_betweenness = sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:10]

        stats['top_degree_centrality'] = [(node, float(cent)) for node, cent in top_degree]
        stats['top_betweenness_centrality'] = [(node, float(cent)) for node, cent in top_betweenness]

        with open('data/network_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print("\n📈 Network Statistics:")
        print(f"  • Nodes: {stats['nodes']}")
        print(f"  • Edges: {stats['edges']}")
        print(f"  • Density: {stats['density']:.4f}")
        print(f"  • Avg Clustering: {stats['avg_clustering']:.4f}")

    def plot_keyword_clusters(self):
        """绘制现代化关键词聚类图"""
        print(f"\n📊 绘制关键词聚类图...")

        # 加载共现矩阵
        cooc_matrix = pd.read_csv('data/cooccurrence_matrix.csv',
                                 index_col=0, encoding='utf-8-sig')

        # 选择有意义的词
        word_sums = cooc_matrix.sum(axis=1)
        meaningful_words = word_sums[word_sums > 0.1].index.tolist()

        if len(meaningful_words) < 10:
            print("⚠️  有意义的词太少，跳过聚类")
            return

        # 提取子矩阵
        sub_matrix = cooc_matrix.loc[meaningful_words, meaningful_words].values

        # K-means聚类
        n_clusters = min(5, len(meaningful_words) // 3)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(sub_matrix)

        # PCA降维
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(sub_matrix)

        # 绘制
        fig, ax = plt.subplots(figsize=(16, 12))

        # 为每个簇使用不同颜色
        for i in range(n_clusters):
            mask = clusters == i
            ax.scatter(coords[mask, 0], coords[mask, 1],
                      c=[COLORS['palette'][i % len(COLORS['palette'])]],
                      s=200, alpha=0.7,
                      edgecolors='white', linewidths=2,
                      label=f'Cluster {i+1}')

        # 添加标签
        for i, word in enumerate(meaningful_words):
            ax.annotate(word, (coords[i, 0], coords[i, 1]),
                       fontsize=10, alpha=0.9,
                       bbox=dict(boxstyle='round,pad=0.3',
                               facecolor='white',
                               edgecolor='gray',
                               alpha=0.7))

        ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)',
                     fontsize=13, fontweight='bold')
        ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)',
                     fontsize=13, fontweight='bold')
        ax.set_title('Keyword Clustering Analysis\nK-means with PCA Dimensionality Reduction',
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()
        output_path = f'{self.output_dir}/keyword_clusters.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ 关键词聚类图已保存: {output_path}")
        plt.close()

        # 保存聚类结果
        cluster_results = {}
        for i in range(n_clusters):
            mask = clusters == i
            cluster_words = [meaningful_words[j] for j in range(len(meaningful_words)) if mask[j]]
            cluster_results[f'Cluster_{i+1}'] = cluster_words

        with open('data/keyword_clusters.json', 'w', encoding='utf-8') as f:
            json.dump(cluster_results, f, ensure_ascii=False, indent=2)

    def plot_topic_distribution(self):
        """绘制现代化主题分布图"""
        print(f"\n📊 绘制主题分布图...")

        # 统计各主题的文档数
        topic_counts = Counter([doc['dominant_topic_label'] for doc in self.doc_topics])

        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 9))

        labels = list(topic_counts.keys())
        sizes = list(topic_counts.values())
        colors = COLORS['palette'][:len(labels)]

        # 绘制饼图，使用爆炸效果突出最大分类
        explode = [0.05 if size == max(sizes) else 0 for size in sizes]

        wedges, texts, autotexts = ax.pie(sizes,
                                          labels=labels,
                                          colors=colors,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          explode=explode,
                                          shadow=True,
                                          textprops={'fontsize': 11, 'fontweight': 'bold'})

        # 美化百分比文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')

        ax.set_title('Document Distribution by LDA Topic\n' +
                    f'Total Documents: {len(self.doc_topics)}',
                    fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout()
        output_path = f'{self.output_dir}/topic_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ 主题分布图已保存: {output_path}")
        plt.close()

    def plot_category_keywords_heatmap(self):
        """绘制现代化类别-关键词热力图"""
        print(f"\n📊 绘制类别关键词热力图...")

        # 收集所有高频词
        all_words = set()
        for words_list in self.category_keywords.values():
            all_words.update([word for word, _ in words_list[:10]])

        all_words = sorted(list(all_words))

        # 构建矩阵
        matrix = []
        categories = list(self.category_keywords.keys())

        for category in categories:
            row = []
            word_dict = dict(self.category_keywords[category])
            for word in all_words:
                row.append(word_dict.get(word, 0))
            matrix.append(row)

        # 绘制热力图
        fig, ax = plt.subplots(figsize=(18, 10))

        # 使用现代配色
        sns.heatmap(matrix,
                   xticklabels=all_words,
                   yticklabels=categories,
                   cmap='RdYlBu_r',
                   annot=True,
                   fmt='g',
                   cbar_kws={'label': 'Frequency'},
                   linewidths=0.5,
                   linecolor='white',
                   ax=ax)

        ax.set_xlabel('Keywords', fontsize=13, fontweight='bold')
        ax.set_ylabel('Policy Categories', fontsize=13, fontweight='bold')
        ax.set_title('Category-Keyword Frequency Heatmap\nShowing Top Keywords by Policy Type',
                    fontsize=16, fontweight='bold', pad=20)

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)

        plt.tight_layout()
        output_path = f'{self.output_dir}/category_keywords_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ 类别关键词热力图已保存: {output_path}")
        plt.close()

    def plot_topic_evolution(self):
        """绘制现代化主题演化时间线"""
        print(f"\n📊 绘制主题演化图...")

        # 加载主题演化数据
        with open('data/topic_evolution.json', 'r', encoding='utf-8') as f:
            evolution = json.load(f)

        # 提取数据
        dates = [item['date'] for item in evolution]
        topics = [item['topic'] for item in evolution]
        universities = [item['university'] for item in evolution]

        # 主题颜色映射
        unique_topics = list(set(topics))
        topic_colors = {topic: COLORS['palette'][i % len(COLORS['palette'])]
                       for i, topic in enumerate(unique_topics)}

        # 创建图形
        fig, ax = plt.subplots(figsize=(20, 8))

        # 绘制时间线
        for i, (date, topic, uni) in enumerate(zip(dates, topics, universities)):
            color = topic_colors[topic]

            # 绘制点
            ax.scatter(i, 0, s=600, c=[color], alpha=0.8,
                      edgecolors='white', linewidths=2.5, zorder=3)

            # 添加主题标签
            ax.text(i, 0.03, topic, rotation=45, ha='right', va='bottom',
                   fontsize=9, fontweight='bold')

            # 添加日期和大学标签
            ax.text(i, -0.03, f"{date}\n{uni[:8]}", rotation=45, ha='right', va='top',
                   fontsize=8, alpha=0.8)

        # 添加图例
        legend_elements = [mpatches.Patch(facecolor=color,
                                         edgecolor='white',
                                         label=topic)
                          for topic, color in topic_colors.items()]
        ax.legend(handles=legend_elements, loc='upper left',
                 framealpha=0.9, fontsize=10)

        ax.set_ylim(-0.2, 0.2)
        ax.set_xlim(-1, len(dates))
        ax.set_yticks([])
        ax.set_xlabel('Policy Timeline (Chronological Order)',
                     fontsize=13, fontweight='bold')
        ax.set_title('Topic Evolution Over Time\nShowing Temporal Distribution of Policy Themes',
                    fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.spines['left'].set_visible(False)

        plt.tight_layout()
        output_path = f'{self.output_dir}/topic_evolution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ 主题演化图已保存: {output_path}")
        plt.close()

    def plot_lda_topics_bar(self):
        """绘制现代化LDA主题关键词条形图"""
        print(f"\n📊 绘制LDA主题关键词条形图...")

        n_topics = len(self.topics)

        # 计算子图布局
        ncols = min(3, n_topics)
        nrows = (n_topics + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols,
                                figsize=(7*ncols, 6*nrows))

        # 确保axes是数组
        if n_topics == 1:
            axes = np.array([axes])
        axes = axes.flatten() if n_topics > 1 else axes

        for i, topic in enumerate(self.topics):
            ax = axes[i] if n_topics > 1 else axes[0]

            keywords = topic['keywords'][:10]
            words = [kw[0] for kw in keywords]
            probs = [kw[1] for kw in keywords]

            # 绘制水平条形图
            y_pos = np.arange(len(words))
            bars = ax.barh(y_pos, probs,
                          color=COLORS['palette'][i % len(COLORS['palette'])],
                          alpha=0.8,
                          edgecolor='white',
                          linewidth=1.5)

            # 添加数值标签
            for j, (bar, prob) in enumerate(zip(bars, probs)):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{prob:.3f}',
                       ha='left', va='center',
                       fontsize=9, fontweight='bold')

            ax.set_yticks(y_pos)
            ax.set_yticklabels(words, fontsize=11)
            ax.invert_yaxis()
            ax.set_xlabel('Probability', fontsize=11, fontweight='bold')
            ax.set_title(f'Topic {i}: {topic.get("label", "Unnamed")}',
                        fontsize=13, fontweight='bold', pad=10)
            ax.grid(True, axis='x', alpha=0.3, linestyle='--')

        # 隐藏多余的子图
        for i in range(n_topics, len(axes)):
            axes[i].axis('off')

        plt.suptitle('LDA Topic Analysis - Top Keywords by Probability',
                    fontsize=18, fontweight='bold', y=1.02)
        plt.tight_layout()

        output_path = f'{self.output_dir}/lda_topics_bar.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ LDA主题条形图已保存: {output_path}")
        plt.close()

    def generate_summary_report(self):
        """生成分析摘要报告"""
        print(f"\n📝 生成分析摘要报告...")

        report = []
        report.append("="*70)
        report.append("国内双一流高校生成式人工智能政策分析报告")
        report.append("="*70)
        report.append("")

        report.append("📊 一、数据概况")
        report.append(f"  • 分析文档数: {len(self.doc_topics)}")

        categories = set([doc['category'] for doc in self.doc_topics])
        report.append(f"  • 政策类别数: {len(categories)}")
        report.append(f"  • 政策类别: {', '.join(categories)}")
        report.append("")

        report.append("📈 二、主题分析")
        report.append(f"  • LDA主题数: {len(self.topics)}")
        topic_dist = Counter([doc['dominant_topic_label'] for doc in self.doc_topics])
        report.append("  • 主题分布:")
        for topic, count in topic_dist.most_common():
            pct = count/len(self.doc_topics)*100
            report.append(f"    ▸ {topic}: {count} 篇 ({pct:.1f}%)")
        report.append("")

        report.append("🔍 三、关键发现")
        report.append("  1. 政策演化趋势:")
        report.append("     • 早期(2023年4-7月)侧重伦理规范")
        report.append("     • 中后期(2023年8月-2024年2月)转向教学应用与创新")
        report.append("")
        report.append("  2. 核心关注点:")
        report.append("     • AI技术应用与规范使用")
        report.append("     • 数据安全与伦理保护")
        report.append("     • 教学创新与评价改革")
        report.append("     • 师生能力培养与素养提升")
        report.append("")

        report.append("📁 四、可视化成果")
        report.append("  • 共现网络图: figures/cooccurrence_network.png")
        report.append("  • 关键词聚类: figures/keyword_clusters.png")
        report.append("  • 主题分布图: figures/topic_distribution.png")
        report.append("  • 主题演化图: figures/topic_evolution.png")
        report.append("  • LDA主题图: figures/lda_topics_bar.png")
        report.append("  • 类别热力图: figures/category_keywords_heatmap.png")
        report.append("")

        report.append("="*70)

        report_text = '\n'.join(report)

        with open('data/analysis_summary.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print("\n" + report_text)
        print(f"\n✓ 分析摘要已保存: data/analysis_summary.txt")

    def run(self):
        """运行完整的可视化流程"""
        print("\n" + "="*70)
        print("🎨 现代化语义网络可视化")
        print("="*70)

        # 加载数据
        self.load_data()

        # 依次生成图表
        self.plot_cooccurrence_network(top_n=50)
        self.plot_keyword_clusters()
        self.plot_topic_distribution()
        self.plot_category_keywords_heatmap()
        self.plot_topic_evolution()
        self.plot_lda_topics_bar()
        self.generate_summary_report()

        print("\n" + "="*70)
        print("✅ 可视化完成! 所有图表已保存到 figures/ 目录")
        print("="*70 + "\n")


if __name__ == '__main__':
    visualizer = ModernVisualizer()
    visualizer.run()
