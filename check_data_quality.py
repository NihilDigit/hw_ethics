#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查原始数据质量，识别需要清洗的内容
"""

import json
import re
from collections import Counter

def check_data_quality():
    # 加载原始数据
    with open('data/policies.json', 'r', encoding='utf-8') as f:
        policies = json.load(f)

    print(f"总政策数: {len(policies)}")

    # 检查URL
    url_pattern = r'https?://[^\s]+|www\.[^\s]+'
    urls_found = []
    policies_with_urls = 0

    for policy in policies:
        urls_in_content = re.findall(url_pattern, policy['content'])
        if urls_in_content:
            policies_with_urls += 1
            urls_found.extend(urls_in_content)

    print(f"\n包含URL的政策数: {policies_with_urls}")
    print(f"发现的URL总数: {len(urls_found)}")
    print("URL示例:")
    for url in list(set(urls_found))[:20]:
        print(f"  {url[:80]}")

    # 检查其他需要清洗的内容
    # 1. 邮箱地址
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = []
    for policy in policies:
        emails.extend(re.findall(email_pattern, policy['content']))
    print(f"\n发现的邮箱地址数: {len(emails)}")
    print("邮箱示例:")
    for email in list(set(emails))[:10]:
        print(f"  {email}")

    # 2. 数字和特殊字符
    number_pattern = r'\d+'
    all_numbers = []
    for policy in policies[:10]:
        all_numbers.extend(re.findall(number_pattern, policy['content']))
    print(f"\n前10份政策中的数字总数: {len(all_numbers)}")

    # 3. 检查已处理数据中的问题
    print("\n\n=== 检查已处理数据 ===")
    with open('data/processed_policies.json', 'r', encoding='utf-8') as f:
        processed = json.load(f)

    # 收集所有分词结果
    all_words = []
    for p in processed:
        all_words.extend(p['words'])

    word_freq = Counter(all_words)

    # 检查可疑的词
    print("\n可疑的高频词（可能需要添加到停用词）:")
    suspicious_words = []
    for word, freq in word_freq.most_common(100):
        # 检查是否包含数字、特殊字符等
        if any(char.isdigit() for char in word):
            suspicious_words.append((word, freq))
        elif len(word) == 1:
            suspicious_words.append((word, freq))
        elif word in ['http', 'https', 'com', 'cn', 'edu', 'www', 'html', 'php']:
            suspicious_words.append((word, freq))

    for word, freq in suspicious_words[:30]:
        print(f"  {word}: {freq}")

    # 检查关键词中的问题
    print("\n\n=== 检查TF-IDF关键词 ===")
    with open('data/tfidf_results.json', 'r', encoding='utf-8') as f:
        tfidf_results = json.load(f)

    all_keywords = set()
    for result in tfidf_results:
        for keyword, score in result['top_tfidf_words']:
            all_keywords.add(keyword)

    print(f"TF-IDF关键词总数: {len(all_keywords)}")

    # 检查可疑的关键词
    suspicious_keywords = []
    for keyword in all_keywords:
        if any(char.isdigit() for char in keyword):
            suspicious_keywords.append(keyword)
        elif keyword.lower() in ['http', 'https', 'com', 'cn', 'edu', 'www', 'html', 'php', 'htm']:
            suspicious_keywords.append(keyword)
        elif len(keyword) == 1:
            suspicious_keywords.append(keyword)

    print(f"\n可疑的关键词数: {len(suspicious_keywords)}")
    print("可疑关键词示例:")
    for kw in suspicious_keywords[:30]:
        print(f"  {kw}")

if __name__ == '__main__':
    check_data_quality()
