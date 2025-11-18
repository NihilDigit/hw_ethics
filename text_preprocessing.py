#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政策文本预处理和分类编码
包括:中文分词、停用词过滤、词频统计等
"""

import json
import jieba
import jieba.analyse
import re
from collections import Counter
import os

class TextPreprocessor:
    def __init__(self):
        # 中文停用词列表
        self.stopwords = set([
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '什么', '等', '及', '或', '与', '并', '为', '以', '对', '中',
            '而', '从', '由', '但', '被', '将', '其', '可', '等', '于', '之', '及', '应',
            '应当', '应该', '需要', '进行', '通过', '开展', '实施', '加强', '提高', '建立',
            '完善', '推进', '促进', '各', '有关', '相关', '主要', '重要', '基本', '全面',
            # 添加网络相关停用词
            'http', 'https', 'www', 'com', 'cn', 'edu', 'net', 'org', 'html', 'htm',
            'php', 'asp', 'jsp', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'
        ])

        # 添加自定义词典
        self.add_custom_words()

        # 政策分类编码
        self.policy_categories = {
            '教学管理': 1,
            '科研管理': 2,
            '伦理规范': 3,
            '技术管理': 4,
            '学生指导': 5,
            '教师指导': 6,
            '教学改革': 7,
            '发展规划': 8
        }

        # 适用对象编码
        self.target_roles = {
            '学生': 1,
            '教师': 2,
            '管理人员': 3,
            '科研人员': 4,
            '全体师生': 5
        }

    def add_custom_words(self):
        """添加领域专业词汇"""
        custom_words = [
            '生成式人工智能', '生成式', '人工智能', 'ChatGPT', '大语言模型',
            '深度学习', '机器学习', '自然语言处理', '算法', '数据安全',
            '学术诚信', '学术不端', '知识产权', '隐私保护', '伦理审查',
            '教学改革', '课程设计', '评价方式', '个性化教学', '混合式教学',
            '科研创新', '项目申报', '论文发表', '数据分析', '实验设计',
            '师资队伍', '能力培养', '素养教育', '批判性思维', '创新能力',
            '监督机制', '管理制度', '技术平台', '数据治理', '风险防控',
            '双一流', '高等教育', '教育质量', '人才培养', '协同育人'
        ]
        for word in custom_words:
            jieba.add_word(word)

    def load_policies(self, filepath='data/policies_cleaned_final.json'):
        """加载政策数据(使用清洗后的数据)"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def clean_text(self, text):
        """清理文本:去除URL、邮箱、数字、标点等"""
        # 去除URL
        text = re.sub(r'https?://[^\s]+', ' ', text)
        text = re.sub(r'www\.[^\s]+', ' ', text)

        # 去除邮箱地址
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ' ', text)

        # 去除文件路径和扩展名
        text = re.sub(r'\.(com|cn|edu|net|org|gov|html|htm|php|asp|jsp|pdf|doc|docx|xls|xlsx|ppt|pptx)\b', ' ', text, flags=re.IGNORECASE)

        # 去除数字（包括年份、日期等）
        text = re.sub(r'\d+', ' ', text)

        # 保留中文、英文字母
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z]', ' ', text)

        # 去除多余空格
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def segment_text(self, text):
        """中文分词"""
        # 清理文本
        clean_text = self.clean_text(text)
        # 分词
        words = jieba.cut(clean_text)
        # 过滤停用词和短词
        words = [w.strip() for w in words if w.strip() and len(w.strip()) > 1]
        words = [w for w in words if w not in self.stopwords]
        return words

    def extract_keywords(self, text, topK=20):
        """提取关键词(使用TF-IDF)"""
        keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
        return keywords

    def encode_category(self, category):
        """编码政策类别"""
        return self.policy_categories.get(category, 0)

    def encode_target_role(self, role_str):
        """编码适用对象"""
        roles = []
        for role, code in self.target_roles.items():
            if role in role_str:
                roles.append(code)
        return roles if roles else [0]

    def preprocess_policies(self, policies):
        """预处理所有政策文本"""
        processed_policies = []

        for policy in policies:
            # 分词
            words = self.segment_text(policy['content'])

            # 提取关键词
            keywords = self.extract_keywords(policy['content'], topK=30)

            # 编码
            category_code = self.encode_category(policy['category'])
            role_codes = self.encode_target_role(policy['target_role'])

            processed_policy = {
                'university': policy['university'],
                'title': policy['title'],
                'date': policy['date'],
                'category': policy['category'],
                'category_code': category_code,
                'target_role': policy['target_role'],
                'target_role_codes': role_codes,
                'content': policy['content'],
                'words': words,
                'word_count': len(words),
                'keywords': [(kw, float(weight)) for kw, weight in keywords]
            }

            processed_policies.append(processed_policy)

        return processed_policies

    def save_processed_data(self, processed_policies, filepath='data/processed_policies.json'):
        """保存预处理后的数据"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(processed_policies, f, ensure_ascii=False, indent=2)
        print(f"已保存预处理数据到: {filepath}")

    def generate_statistics(self, processed_policies):
        """生成统计信息"""
        print("\n=== 文本预处理统计 ===")
        print(f"总文档数: {len(processed_policies)}")

        # 词频统计
        all_words = []
        for p in processed_policies:
            all_words.extend(p['words'])

        word_freq = Counter(all_words)
        print(f"\n总词数: {len(all_words)}")
        print(f"独特词数: {len(word_freq)}")

        print(f"\n高频词TOP20:")
        for word, freq in word_freq.most_common(20):
            print(f"  {word}: {freq}")

        # 按类别统计
        print(f"\n按类别统计词数:")
        category_words = {}
        for p in processed_policies:
            cat = p['category']
            if cat not in category_words:
                category_words[cat] = []
            category_words[cat].extend(p['words'])

        for cat, words in category_words.items():
            print(f"  {cat}: {len(words)} 词")

        # 保存高频词
        with open('data/word_frequency.txt', 'w', encoding='utf-8') as f:
            f.write("词语\t频次\n")
            for word, freq in word_freq.most_common(100):
                f.write(f"{word}\t{freq}\n")
        print(f"\n已保存词频统计到: data/word_frequency.txt")

        return word_freq

    def run(self):
        """运行预处理流程"""
        print("开始文本预处理...")

        # 加载数据
        policies = self.load_policies()
        print(f"加载了 {len(policies)} 份政策文档")

        # 预处理
        processed_policies = self.preprocess_policies(policies)

        # 保存
        self.save_processed_data(processed_policies)

        # 统计
        word_freq = self.generate_statistics(processed_policies)

        print("\n预处理完成!")
        return processed_policies, word_freq


if __name__ == '__main__':
    preprocessor = TextPreprocessor()
    processed_policies, word_freq = preprocessor.run()
