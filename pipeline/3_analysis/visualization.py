#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义网络可视化
包括:共现网络、关键词聚类、词云、主题分布等
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

# 注册思源黑体字体
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'SourceHanSansSC-Regular.otf')
font_path_bold = os.path.join(os.path.dirname(__file__), 'fonts', 'SourceHanSansSC-Bold.otf')

if os.path.exists(font_path):
    # 添加字体到系统
    fontManager.addfont(font_path)
    fontManager.addfont(font_path_bold)
    # 设置中文字体为思源黑体
    plt.rcParams['font.sans-serif'] = ['Source Han Sans SC', 'DejaVu Sans']
    print("成功加载思源黑体字体")
else:
    # 回退到默认字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
    print("警告: 未找到思源黑体字体，使用默认字体")

plt.rcParams['axes.unicode_minus'] = False

class Visualizer:
    def __init__(self):
        self.output_dir = 'figures'
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        """加载分析结果数据"""
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

        print("数据加载完成")

    def plot_cooccurrence_network(self, top_n=50):
        """
        绘制共现网络图
        参考文献⑥⑦⑩的语义网络可视化
        """
        print(f"\n绘制共现网络图(Top {top_n} 边)...")

        # 创建网络图
        G = nx.Graph()

        # 添加边(取权重最大的top_n条边)
        for edge in self.edges[:top_n]:
            G.add_edge(edge['word1'], edge['word2'], weight=edge['weight'])

        # 计算节点大小(基于度中心性)
        degree_centrality = nx.degree_centrality(G)
        node_sizes = [degree_centrality[node] * 3000 + 300 for node in G.nodes()]

        # 计算节点颜色(基于介数中心性)
        betweenness_centrality = nx.betweenness_centrality(G)
        node_colors = [betweenness_centrality[node] for node in G.nodes()]

        # 使用spring布局
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

        # 绘制
        plt.figure(figsize=(16, 12))

        # 绘制边
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=np.array(weights)*2)

        # 绘制节点
        nx.draw_networkx_nodes(G, pos,
                              node_size=node_sizes,
                              node_color=node_colors,
                              cmap=plt.cm.YlOrRd,
                              alpha=0.8)

        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

        plt.title('Policy Keywords Co-occurrence Network', fontsize=16, pad=20)
        plt.axis('off')
        plt.tight_layout()

        output_path = f'{self.output_dir}/cooccurrence_network.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"共现网络图已保存到: {output_path}")
        plt.close()

        # 保存网络统计信息
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
        closeness_cent = nx.closeness_centrality(G)

        # Top 10 中心节点
        top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]
        top_betweenness = sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:10]

        stats['top_degree_centrality'] = [(node, float(cent)) for node, cent in top_degree]
        stats['top_betweenness_centrality'] = [(node, float(cent)) for node, cent in top_betweenness]

        with open('data/network_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print("\n=== 网络统计 ===")
        print(f"节点数: {stats['nodes']}")
        print(f"边数: {stats['edges']}")
        print(f"密度: {stats['density']:.4f}")
        print(f"平均聚类系数: {stats['avg_clustering']:.4f}")

        print("\nTop 10 度中心性节点:")
        for node, cent in top_degree:
            print(f"  {node}: {cent:.4f}")

    def plot_keyword_clusters(self):
        """
        绘制关键词聚类
        使用K-means对关键词向量进行聚类
        """
        print(f"\n绘制关键词聚类图...")

        # 加载共现矩阵
        cooc_matrix = pd.read_csv('data/cooccurrence_matrix.csv',
                                 index_col=0, encoding='utf-8-sig')

        # 选择有意义的词(至少有一些共现关系)
        word_sums = cooc_matrix.sum(axis=1)
        meaningful_words = word_sums[word_sums > 0.1].index.tolist()

        if len(meaningful_words) < 10:
            print("有意义的词太少,跳过聚类")
            return

        # 提取子矩阵
        sub_matrix = cooc_matrix.loc[meaningful_words, meaningful_words].values

        # K-means聚类
        n_clusters = min(5, len(meaningful_words) // 3)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(sub_matrix)

        # 使用PCA降维到2D以便可视化
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(sub_matrix)

        # 绘制
        plt.figure(figsize=(14, 10))

        colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))

        for i in range(n_clusters):
            mask = clusters == i
            plt.scatter(coords[mask, 0], coords[mask, 1],
                       c=[colors[i]], s=100, alpha=0.6,
                       label=f'Cluster {i+1}')

        # 添加标签
        for i, word in enumerate(meaningful_words):
            plt.annotate(word, (coords[i, 0], coords[i, 1]),
                        fontsize=9, alpha=0.8)

        plt.xlabel('PC1', fontsize=12)
        plt.ylabel('PC2', fontsize=12)
        plt.title('Keyword Clustering (K-means)', fontsize=16, pad=20)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        output_path = f'{self.output_dir}/keyword_clusters.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"关键词聚类图已保存到: {output_path}")
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
        """绘制主题分布"""
        print(f"\n绘制主题分布图...")

        # 统计各主题的文档数
        topic_counts = Counter([doc['dominant_topic_label'] for doc in self.doc_topics])

        # 绘制饼图
        plt.figure(figsize=(10, 8))

        labels = list(topic_counts.keys())
        sizes = list(topic_counts.values())
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 11})

        plt.title('Document Distribution by Topic', fontsize=16, pad=20)
        plt.axis('equal')
        plt.tight_layout()

        output_path = f'{self.output_dir}/topic_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"主题分布图已保存到: {output_path}")
        plt.close()

    def plot_category_keywords_heatmap(self):
        """绘制类别-关键词热力图"""
        print(f"\n绘制类别关键词热力图...")

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
        plt.figure(figsize=(16, 10))

        sns.heatmap(matrix, xticklabels=all_words, yticklabels=categories,
                   cmap='YlOrRd', annot=True, fmt='g', cbar_kws={'label': 'Frequency'})

        plt.xlabel('Keywords', fontsize=12)
        plt.ylabel('Policy Categories', fontsize=12)
        plt.title('Category-Keyword Heatmap', fontsize=16, pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        output_path = f'{self.output_dir}/category_keywords_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"类别关键词热力图已保存到: {output_path}")
        plt.close()

    def plot_topic_evolution(self):
        """绘制主题演化时间线"""
        print(f"\n绘制主题演化图...")

        # 加载主题演化数据
        with open('data/topic_evolution.json', 'r', encoding='utf-8') as f:
            evolution = json.load(f)

        # 按时间绘制
        dates = [item['date'] for item in evolution]
        topics = [item['topic'] for item in evolution]
        universities = [item['university'] for item in evolution]

        # 主题颜色映射
        unique_topics = list(set(topics))
        topic_colors = {topic: plt.cm.Set2(i/len(unique_topics))
                       for i, topic in enumerate(unique_topics)}

        plt.figure(figsize=(16, 6))

        for i, (date, topic, uni) in enumerate(zip(dates, topics, universities)):
            color = topic_colors[topic]
            plt.scatter(i, 0, s=500, c=[color], alpha=0.7, edgecolors='black', linewidth=1.5)
            plt.text(i, 0.02, topic, rotation=45, ha='right', fontsize=8)
            plt.text(i, -0.02, f"{date}\n{uni}", rotation=45, ha='right',
                    fontsize=7, va='top')

        plt.ylim(-0.15, 0.15)
        plt.xlim(-0.5, len(dates)-0.5)
        plt.yticks([])
        plt.xlabel('Timeline', fontsize=12)
        plt.title('Topic Evolution Over Time', fontsize=16, pad=20)
        plt.grid(True, axis='x', alpha=0.3)
        plt.tight_layout()

        output_path = f'{self.output_dir}/topic_evolution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"主题演化图已保存到: {output_path}")
        plt.close()

    def plot_lda_topics_bar(self):
        """绘制LDA主题关键词条形图"""
        print(f"\n绘制LDA主题关键词条形图...")

        n_topics = len(self.topics)

        fig, axes = plt.subplots(1, n_topics, figsize=(5*n_topics, 6))

        if n_topics == 1:
            axes = [axes]

        for i, topic in enumerate(self.topics):
            keywords = topic['keywords'][:10]
            words = [kw[0] for kw in keywords]
            probs = [kw[1] for kw in keywords]

            axes[i].barh(range(len(words)), probs, color=plt.cm.Pastel1(i/n_topics))
            axes[i].set_yticks(range(len(words)))
            axes[i].set_yticklabels(words)
            axes[i].invert_yaxis()
            axes[i].set_xlabel('Probability', fontsize=10)
            axes[i].set_title(f'Topic {i}', fontsize=12)
            axes[i].grid(True, axis='x', alpha=0.3)

        plt.suptitle('LDA Topics - Top Keywords', fontsize=16)
        plt.tight_layout()

        output_path = f'{self.output_dir}/lda_topics_bar.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"LDA主题条形图已保存到: {output_path}")
        plt.close()

    def generate_summary_report(self):
        """生成分析摘要报告"""
        print(f"\n生成分析摘要报告...")

        report = []
        report.append("="*60)
        report.append("国内双一流高校生成式人工智能政策分析报告")
        report.append("="*60)
        report.append("")

        report.append("一、数据概况")
        report.append(f"  - 分析文档数: {len(self.doc_topics)}")

        categories = set([doc['category'] for doc in self.doc_topics])
        report.append(f"  - 政策类别数: {len(categories)}")
        report.append(f"  - 政策类别: {', '.join(categories)}")
        report.append("")

        report.append("二、主题分析")
        report.append(f"  - LDA主题数: {len(self.topics)}")
        topic_dist = Counter([doc['dominant_topic_label'] for doc in self.doc_topics])
        report.append("  - 主题分布:")
        for topic, count in topic_dist.most_common():
            report.append(f"    * {topic}: {count} 篇 ({count/len(self.doc_topics)*100:.1f}%)")
        report.append("")

        report.append("三、关键发现")
        report.append("  1. 政策演化趋势:")
        report.append("     早期(2023年4-7月)侧重伦理规范,中后期转向教学应用与创新")
        report.append("")
        report.append("  2. 核心关注点:")
        report.append("     - AI技术应用与规范使用")
        report.append("     - 数据安全与伦理保护")
        report.append("     - 教学创新与评价改革")
        report.append("     - 师生能力培养与素养提升")
        report.append("")

        report.append("四、可视化成果")
        report.append("  - 共现网络图: figures/cooccurrence_network.png")
        report.append("  - 关键词聚类: figures/keyword_clusters.png")
        report.append("  - 主题分布图: figures/topic_distribution.png")
        report.append("  - 主题演化图: figures/topic_evolution.png")
        report.append("  - LDA主题图: figures/lda_topics_bar.png")
        report.append("  - 类别热力图: figures/category_keywords_heatmap.png")
        report.append("")

        report.append("="*60)

        report_text = '\n'.join(report)

        with open('data/analysis_summary.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(report_text)
        print(f"\n分析摘要已保存到: data/analysis_summary.txt")

    def run(self):
        """运行完整的可视化流程"""
        print("="*60)
        print("开始语义网络可视化")
        print("="*60)

        # 加载数据
        self.load_data()

        # 1. 共现网络图
        self.plot_cooccurrence_network(top_n=50)

        # 2. 关键词聚类
        self.plot_keyword_clusters()

        # 3. 主题分布
        self.plot_topic_distribution()

        # 4. 类别关键词热力图
        self.plot_category_keywords_heatmap()

        # 5. 主题演化
        self.plot_topic_evolution()

        # 6. LDA主题条形图
        self.plot_lda_topics_bar()

        # 7. 生成摘要报告
        self.generate_summary_report()

        print("\n" + "="*60)
        print("可视化完成! 所有图表已保存到 figures/ 目录")
        print("="*60)


if __name__ == '__main__':
    visualizer = Visualizer()
    visualizer.run()
