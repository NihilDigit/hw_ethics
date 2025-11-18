#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从raw_policies目录重建policies.json
"""

import os
import json
import re

def extract_info_from_file(filepath):
    """从txt文件中提取政策信息"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    policy = {}

    for line in lines:
        if line.startswith('高校: '):
            policy['university'] = line.replace('高校: ', '').strip()
        elif line.startswith('标题: '):
            policy['title'] = line.replace('标题: ', '').strip()
        elif line.startswith('日期: '):
            policy['date'] = line.replace('日期: ', '').strip()
        elif line.startswith('类别: '):
            policy['category'] = line.replace('类别: ', '').strip()
        elif line.startswith('适用对象: '):
            policy['target_role'] = line.replace('适用对象: ', '').strip()
        elif line.startswith('来源URL: '):
            policy['url'] = line.replace('来源URL: ', '').strip()
        elif line.startswith('内容:'):
            # 找到"内容:"后面的所有内容
            idx = content.find('内容:')
            policy['content'] = content[idx+3:].strip()
            break

    return policy if len(policy) > 5 else None

def main():
    raw_dir = 'data/raw_policies'
    policies = []

    # 读取所有txt文件
    for filename in sorted(os.listdir(raw_dir)):
        if filename.endswith('.txt'):
            filepath = os.path.join(raw_dir, filename)
            policy = extract_info_from_file(filepath)
            if policy:
                policies.append(policy)

    # 保存为JSON
    with open('data/policies.json', 'w', encoding='utf-8') as f:
        json.dump(policies, f, ensure_ascii=False, indent=2)

    print(f"成功重建 {len(policies)} 份政策数据")

    # 统计每个大学的政策数量
    uni_count = {}
    for p in policies:
        uni = p['university']
        uni_count[uni] = uni_count.get(uni, 0) + 1

    print(f"\n成功爬取的大学数量: {len(uni_count)}")
    print(f"总政策数量: {len(policies)}")

    # 更新final report
    failed_unis = []
    from universities_list import DOUBLE_FIRST_CLASS_UNIVERSITIES
    for uni in DOUBLE_FIRST_CLASS_UNIVERSITIES.keys():
        if uni not in uni_count:
            failed_unis.append(uni)

    final_report = {
        'total_universities': 146,
        'successful': len(uni_count),
        'failed': len(failed_unis),
        'total_policies': len(policies),
        'failed_list': failed_unis
    }

    with open('data/crawler_report_corrected.json', 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)

    print(f"\n最终统计: {len(uni_count)}/146 所大学成功爬取")
    print(f"失败: {len(failed_unis)} 所大学")

if __name__ == '__main__':
    main()
