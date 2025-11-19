#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LDA主题模型分析
参考文献⑨:基于LDA和语义网络的感知价值维度研究
用于识别政策文本的主题维度
"""

import json
import numpy as np
from collections import defaultdict
from gensim import corpora
from gensim.models import LdaModel
import warnings
warnings.filterwarnings('ignore')

class LDAAnalyzer:
    def __init__(self, n_topics=5):
        self.n_topics = n_topics
        self.processed_policies = []
        self.dictionary = None
        self.corpus = None
        self.lda_model = None
        self.topic_labels = []

    def load_processed_data(self, filepath='data/processed_policies.json'):
        """加载预处理后的数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.processed_policies = json.load(f)
        print(f"加载了 {len(self.processed_policies)} 份预处理文档")

    def prepare_corpus(self):
        """准备语料库"""
        print("\n准备语料库...")

        # 提取所有文档的词列表
        documents = [policy['words'] for policy in self.processed_policies]

        # 创建词典
        self.dictionary = corpora.Dictionary(documents)

        # 过滤极端词:至少出现在2个文档,最多不超过文档总数的70%
        self.dictionary.filter_extremes(no_below=2, no_above=0.7)

        print(f"词典大小: {len(self.dictionary)}")

        # 创建文档-词频矩阵(BOW格式)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in documents]

        print(f"语料库大小: {len(self.corpus)} 篇文档")

        return self.corpus

    def train_lda_model(self, passes=20, iterations=100):
        """训练LDA模型"""
        print(f"\n训练LDA模型(主题数={self.n_topics})...")

        self.lda_model = LdaModel(
            corpus=self.corpus,
            id2word=self.dictionary,
            num_topics=self.n_topics,
            random_state=42,
            passes=passes,
            iterations=iterations,
            alpha='auto',
            per_word_topics=True
        )

        print("LDA模型训练完成!")

        # 显示主题
        self.display_topics()

        return self.lda_model

    def display_topics(self, num_words=10):
        """显示主题及其关键词"""
        print(f"\n=== LDA主题分析结果 ===")

        topics = []

        for topic_id in range(self.n_topics):
            topic_words = self.lda_model.show_topic(topic_id, topn=num_words)
            topics.append({
                'topic_id': topic_id,
                'keywords': [(word, float(prob)) for word, prob in topic_words]
            })

            # 根据关键词为主题命名
            top_words = [word for word, _ in topic_words[:5]]
            topic_label = self.infer_topic_label(top_words)
            self.topic_labels.append(topic_label)

            print(f"\n主题 {topic_id}: {topic_label}")
            for word, prob in topic_words:
                print(f"  {word}: {prob:.4f}")

        # 保存主题
        with open('data/lda_topics.json', 'w', encoding='utf-8') as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)

        print(f"\nLDA主题已保存到: data/lda_topics.json")

        return topics

    def infer_topic_label(self, top_words):
        """根据高频词推断主题标签"""
        # 定义主题关键词模式
        patterns = {
            '教学应用与创新': ['教学', '学习', '课程', '学生', '教育', '培养', '能力'],
            '伦理与规范': ['伦理', '规范', '原则', '责任', '诚信', '透明', '保护'],
            '数据安全与隐私': ['数据', '安全', '隐私', '保护', '防止', '防范'],
            '技术管理与平台': ['技术', '平台', '管理', '建设', '系统', '支撑'],
            '科研应用': ['科研', '研究', '论文', '项目', '创新', '成果'],
            '政策与制度': ['政策', '制度', '规定', '办法', '要求', '机制'],
            'AI工具使用': ['AI', '工具', '使用', '应用', '辅助', '生成']
        }

        # 计算每个主题模式的匹配度
        scores = {}
        for label, keywords in patterns.items():
            score = sum(1 for word in top_words if word in keywords)
            scores[label] = score

        # 返回得分最高的标签
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return f"主题_{'+'.join(top_words[:2])}"

    def analyze_document_topics(self):
        """分析每个文档的主题分布"""
        print(f"\n分析文档主题分布...")

        doc_topics = []

        for i, policy in enumerate(self.processed_policies):
            # 获取文档的主题分布
            bow = self.corpus[i]
            topics = self.lda_model.get_document_topics(bow)

            # 找出主导主题
            if topics:
                dominant_topic = max(topics, key=lambda x: x[1])
                topic_id, topic_prob = dominant_topic
            else:
                topic_id, topic_prob = 0, 0.0

            doc_topics.append({
                'university': policy['university'],
                'category': policy['category'],
                'dominant_topic_id': int(topic_id),
                'dominant_topic_label': self.topic_labels[topic_id],
                'dominant_topic_prob': float(topic_prob),
                'all_topics': [(int(tid), float(prob)) for tid, prob in topics]
            })

        # 保存结果
        with open('data/document_topics.json', 'w', encoding='utf-8') as f:
            json.dump(doc_topics, f, ensure_ascii=False, indent=2)

        print(f"文档主题分布已保存到: data/document_topics.json")

        # 统计主题分布
        self.analyze_topic_distribution(doc_topics)

        return doc_topics

    def analyze_topic_distribution(self, doc_topics):
        """统计主题分布"""
        print(f"\n=== 主题分布统计 ===")

        # 按主题统计文档数
        topic_doc_count = defaultdict(int)
        for doc in doc_topics:
            topic_id = doc['dominant_topic_id']
            topic_doc_count[topic_id] += 1

        print(f"\n各主题的文档分布:")
        for topic_id in range(self.n_topics):
            label = self.topic_labels[topic_id]
            count = topic_doc_count[topic_id]
            print(f"  {label}: {count} 篇")

        # 按类别统计主题
        print(f"\n各类别政策的主题分布:")
        category_topics = defaultdict(lambda: defaultdict(int))

        for doc in doc_topics:
            category = doc['category']
            topic_label = doc['dominant_topic_label']
            category_topics[category][topic_label] += 1

        for category, topics in category_topics.items():
            print(f"\n{category}:")
            for topic_label, count in topics.items():
                print(f"  {topic_label}: {count}")

        # 保存统计结果
        stats = {
            'topic_document_count': {self.topic_labels[tid]: count
                                    for tid, count in topic_doc_count.items()},
            'category_topic_distribution': {cat: dict(topics)
                                          for cat, topics in category_topics.items()}
        }

        with open('data/lda_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    def find_topic_evolution(self):
        """分析主题演化(按时间顺序)"""
        print(f"\n=== 主题演化分析 ===")

        # 按日期排序文档
        sorted_policies = sorted(self.processed_policies, key=lambda x: x['date'])

        topic_timeline = []

        for i, policy in enumerate(sorted_policies):
            bow = self.dictionary.doc2bow(policy['words'])
            topics = self.lda_model.get_document_topics(bow)

            if topics:
                dominant_topic = max(topics, key=lambda x: x[1])
                topic_id, topic_prob = dominant_topic
                topic_label = self.topic_labels[topic_id]
            else:
                topic_id, topic_prob = 0, 0.0
                topic_label = self.topic_labels[0]

            topic_timeline.append({
                'date': policy['date'],
                'university': policy['university'],
                'topic': topic_label,
                'topic_id': int(topic_id)
            })

            print(f"{policy['date']} - {policy['university']}: {topic_label}")

        # 保存演化结果
        with open('data/topic_evolution.json', 'w', encoding='utf-8') as f:
            json.dump(topic_timeline, f, ensure_ascii=False, indent=2)

        return topic_timeline

    def run(self):
        """运行完整的LDA分析流程"""
        print("="*50)
        print("开始LDA主题模型分析")
        print("="*50)

        # 加载数据
        self.load_processed_data()

        # 准备语料库
        self.prepare_corpus()

        # 训练LDA模型
        self.train_lda_model()

        # 分析文档主题
        self.analyze_document_topics()

        # 主题演化
        self.find_topic_evolution()

        print("\n" + "="*50)
        print("LDA分析完成!")
        print("="*50)


if __name__ == '__main__':
    # 可以尝试不同的主题数
    analyzer = LDAAnalyzer(n_topics=5)
    analyzer.run()
