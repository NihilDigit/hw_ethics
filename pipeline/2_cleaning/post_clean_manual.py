#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动微调清洗后的数据
"""

import json
import re


def manual_clean():
    """手动清理残留噪声"""
    with open('data/policies_cleaned.json', 'r', encoding='utf-8') as f:
        policies = json.load(f)

    # 定义需要删除的残留模式
    remove_patterns = [
        r'^\d{8,11}\s*$',  # 纯电话号码行
        r'^(?:联系)?电话[：:].{0,100}$',
        r'^(?:课程|考试|毕业证补办及学历勘误|学生评教|Class直录播平台)[：:]\s*$',
        r'^二级教学单位\s*$',
        r'^教务通知\s*$',
        r'^.*?ICP备\d+号.*?$',
        r'^.*?公网安备\d+号.*?$',
        r'^.*?技术支持[：:].*$',
        r'^jwc\..*$',
        r'^.*?微教学\s*$',
        r'^信息网络技术中心\s*$',
        r'^【[^】]+】[^：]+：[^】]+$',  # 底部新闻标题
        r'^".*?"(?:系列之|专项行动|讲座|活动).*$',  # 系列活动标题
    ]

    for policy in policies:
        content = policy['content']
        lines = content.split('\n')
        cleaned_lines = []

        for line in lines:
            line_stripped = line.strip()

            if not line_stripped:
                continue

            # 检查是否匹配删除模式
            should_remove = False
            for pattern in remove_patterns:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    should_remove = True
                    break

            if not should_remove:
                cleaned_lines.append(line_stripped)

        # 更新内容
        policy['content'] = '\n'.join(cleaned_lines)
        policy['content_length'] = len(policy['content'])

    # 保存
    with open('data/policies_cleaned_final.json', 'w', encoding='utf-8') as f:
        json.dump(policies, f, ensure_ascii=False, indent=2)

    print("手动清理完成!")
    print(f"处理了 {len(policies)} 份文档")

    # 统计
    total_length = sum(p['content_length'] for p in policies)
    avg_length = total_length / len(policies)
    print(f"总字符数: {total_length}")
    print(f"平均长度: {avg_length:.0f} 字符/文档")


if __name__ == '__main__':
    manual_clean()
