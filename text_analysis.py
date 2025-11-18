#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本分析:TF-IDF、关键词提取、共现矩阵、加权共词分析
参考文献②的方法:基于TF-IDF的加权共词分析
"""

import json
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from itertools import combinations
import os

class TextAnalyzer:
    def __init__(self):
        self.processed_policies = []
        self.tfidf_matrix = None
        self.vocab = []
        self.cooccurrence_matrix = None

    def load_processed_data(self, filepath='data/processed_policies.json'):
        """加载预处理后的数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.processed_policies = json.load(f)
        print(f"加载了 {len(self.processed_policies)} 份预处理文档")

    def compute_tf(self, words):
        """计算词频TF"""
        tf = Counter(words)
        total = len(words)
        return {word: count/total for word, count in tf.items()}

    def compute_idf(self, all_documents):
        """计算逆文档频率IDF"""
        n_docs = len(all_documents)
        # 统计每个词出现在多少个文档中
        doc_freq = defaultdict(int)

        for doc_words in all_documents:
            unique_words = set(doc_words)
            for word in unique_words:
                doc_freq[word] += 1

        # 计算IDF: log(N / df)
        idf = {word: np.log(n_docs / (df + 1)) for word, df in doc_freq.items()}
        return idf

    def compute_tfidf(self):
        """计算TF-IDF矩阵"""
        print("\n计算TF-IDF矩阵...")

        # 收集所有文档的词
        all_documents = [p['words'] for p in self.processed_policies]

        # 计算IDF
        idf = self.compute_idf(all_documents)

        # 构建词汇表(选择出现频率适中的词)
        word_freq = Counter()
        for words in all_documents:
            word_freq.update(words)

        # 过滤:至少出现在2个文档中,最多不超过8个文档
        self.vocab = [word for word, freq in word_freq.items()
                      if 2 <= len([d for d in all_documents if word in d]) <= 8]

        print(f"词汇表大小: {len(self.vocab)}")

        # 计算TF-IDF矩阵
        tfidf_matrix = []
        for doc_words in all_documents:
            tf = self.compute_tf(doc_words)
            tfidf_vec = [tf.get(word, 0) * idf.get(word, 0) for word in self.vocab]
            tfidf_matrix.append(tfidf_vec)

        self.tfidf_matrix = np.array(tfidf_matrix)

        # 保存TF-IDF结果
        self.save_tfidf_results()

        return self.tfidf_matrix

    def save_tfidf_results(self):
        """保存TF-IDF分析结果"""
        # 为每个文档找出最重要的词
        results = []

        for i, policy in enumerate(self.processed_policies):
            tfidf_scores = self.tfidf_matrix[i]
            # 获取top 10的词
            top_indices = np.argsort(tfidf_scores)[-10:][::-1]
            top_words = [(self.vocab[idx], float(tfidf_scores[idx]))
                        for idx in top_indices if tfidf_scores[idx] > 0]

            results.append({
                'university': policy['university'],
                'category': policy['category'],
                'top_tfidf_words': top_words
            })

        with open('data/tfidf_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("TF-IDF结果已保存到: data/tfidf_results.json")

    def compute_cooccurrence_matrix(self, window_size=5, use_tfidf_weight=True):
        """
        计算加权共现矩阵
        参考文献②:使用TF-IDF权重 + 政策效力等级加权
        window_size: 共现窗口大小(词距离)
        """
        print(f"\n计算共现矩阵(窗口大小={window_size})...")

        # 使用vocab中的词构建共现矩阵
        if not self.vocab:
            print("请先运行compute_tfidf()")
            return None

        word_to_idx = {word: i for i, word in enumerate(self.vocab)}
        n_vocab = len(self.vocab)

        # 初始化共现矩阵
        cooc_matrix = np.zeros((n_vocab, n_vocab))

        # 政策类别权重(模拟政策效力等级)
        category_weights = {
            '发展规划': 1.5,  # 高层次规划,权重最高
            '教学管理': 1.3,
            '科研管理': 1.3,
            '伦理规范': 1.2,
            '技术管理': 1.0,
            '教学改革': 1.0,
            '教师指导': 0.8,
            '学生指导': 0.8
        }

        for policy in self.processed_policies:
            words = policy['words']
            category = policy['category']
            weight = category_weights.get(category, 1.0)

            # 计算该文档的TF-IDF权重
            if use_tfidf_weight and self.tfidf_matrix is not None:
                doc_idx = self.processed_policies.index(policy)
                tfidf_weights = {self.vocab[i]: self.tfidf_matrix[doc_idx][i]
                               for i in range(len(self.vocab))}
            else:
                tfidf_weights = {word: 1.0 for word in self.vocab}

            # 滑动窗口计算共现
            for i in range(len(words)):
                if words[i] not in word_to_idx:
                    continue

                word1_idx = word_to_idx[words[i]]
                word1_tfidf = tfidf_weights.get(words[i], 0)

                # 窗口内的其他词
                for j in range(max(0, i-window_size), min(len(words), i+window_size+1)):
                    if i == j or words[j] not in word_to_idx:
                        continue

                    word2_idx = word_to_idx[words[j]]
                    word2_tfidf = tfidf_weights.get(words[j], 0)

                    # 加权:类别权重 * TF-IDF权重
                    cooc_weight = weight * (word1_tfidf + word2_tfidf) / 2

                    cooc_matrix[word1_idx][word2_idx] += cooc_weight

        # 对称化
        self.cooccurrence_matrix = (cooc_matrix + cooc_matrix.T) / 2

        # 保存共现矩阵
        self.save_cooccurrence_matrix()

        return self.cooccurrence_matrix

    def save_cooccurrence_matrix(self):
        """保存共现矩阵"""
        # 保存为CSV
        df = pd.DataFrame(self.cooccurrence_matrix,
                         index=self.vocab,
                         columns=self.vocab)
        df.to_csv('data/cooccurrence_matrix.csv', encoding='utf-8-sig')

        # 提取强共现关系(top edges)
        edges = []
        n = len(self.vocab)

        for i in range(n):
            for j in range(i+1, n):
                if self.cooccurrence_matrix[i][j] > 0:
                    edges.append({
                        'word1': self.vocab[i],
                        'word2': self.vocab[j],
                        'weight': float(self.cooccurrence_matrix[i][j])
                    })

        # 按权重排序
        edges = sorted(edges, key=lambda x: x['weight'], reverse=True)

        # 保存top 100 edges
        with open('data/cooccurrence_edges.json', 'w', encoding='utf-8') as f:
            json.dump(edges[:100], f, ensure_ascii=False, indent=2)

        print(f"共现矩阵已保存到: data/cooccurrence_matrix.csv")
        print(f"Top 100 共现关系已保存到: data/cooccurrence_edges.json")
        print(f"强共现关系示例(Top 10):")
        for edge in edges[:10]:
            print(f"  {edge['word1']} <-> {edge['word2']}: {edge['weight']:.3f}")

    def compute_keyword_similarity(self, top_k=30):
        """
        基于共现关系计算关键词相似度
        使用余弦相似度
        """
        print(f"\n计算关键词相似度...")

        if self.cooccurrence_matrix is None:
            print("请先运行compute_cooccurrence_matrix()")
            return None

        # 计算余弦相似度
        # 规范化:每个词向量 / 其L2范数
        norms = np.linalg.norm(self.cooccurrence_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1  # 避免除零

        normalized_matrix = self.cooccurrence_matrix / norms
        similarity_matrix = np.dot(normalized_matrix, normalized_matrix.T)

        # 找出每个词最相似的词
        similarities = []

        for i, word in enumerate(self.vocab):
            sim_scores = similarity_matrix[i]
            # 排除自己
            sim_scores[i] = -1

            top_indices = np.argsort(sim_scores)[-top_k:][::-1]
            similar_words = [(self.vocab[idx], float(sim_scores[idx]))
                           for idx in top_indices if sim_scores[idx] > 0]

            if similar_words:
                similarities.append({
                    'word': word,
                    'similar_words': similar_words[:10]  # 只保存top 10
                })

        # 保存结果
        with open('data/keyword_similarity.json', 'w', encoding='utf-8') as f:
            json.dump(similarities, f, ensure_ascii=False, indent=2)

        print(f"关键词相似度已保存到: data/keyword_similarity.json")
        print(f"\n示例 - '教学'的相似词:")
        for item in similarities:
            if item['word'] == '教学':
                for sim_word, score in item['similar_words'][:5]:
                    print(f"  {sim_word}: {score:.3f}")
                break

    def analyze_by_category(self):
        """按政策类别分析关键词"""
        print("\n=== 按类别分析关键词 ===")

        category_words = defaultdict(list)

        for policy in self.processed_policies:
            category = policy['category']
            category_words[category].extend(policy['words'])

        results = {}

        for category, words in category_words.items():
            word_freq = Counter(words)
            top_words = word_freq.most_common(15)
            results[category] = [(word, freq) for word, freq in top_words]

            print(f"\n{category}:")
            for word, freq in top_words[:10]:
                print(f"  {word}: {freq}")

        # 保存
        with open('data/category_keywords.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return results

    def run(self):
        """运行完整的文本分析流程"""
        print("="*50)
        print("开始文本分析")
        print("="*50)

        # 加载数据
        self.load_processed_data()

        # 1. TF-IDF分析
        self.compute_tfidf()

        # 2. 加权共现矩阵
        self.compute_cooccurrence_matrix(window_size=5, use_tfidf_weight=True)

        # 3. 关键词相似度
        self.compute_keyword_similarity()

        # 4. 按类别分析
        self.analyze_by_category()

        print("\n" + "="*50)
        print("文本分析完成!")
        print("="*50)


if __name__ == '__main__':
    analyzer = TextAnalyzer()
    analyzer.run()
