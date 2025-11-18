#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版数据清洗脚本 - 彻底清除所有噪声
"""

import json
import re


class PolicyDataCleanerFinal:
    def __init__(self):
        """初始化"""
        # 底部新闻链接模式
        self.bottom_news_patterns = [
            r'^【.*?】.*?(?:大学|学院|研究院|中心).*?[:：].*$',  # 【来源】标题
            r'^.*?(?:大学|学院)：.*$',  # 学校：标题
            r'^\d{4}[./]\d{1,2}[./]\d{1,2}$',  # 日期
        ]

        # 联系信息模式
        self.contact_patterns = [
            r'^(?:联系)?(?:电话|邮编|地址)[：:].{0,100}$',
            r'^\d{5,11}$',  # 纯数字(电话/邮编)
            r'^ICP备\d+号$',
            r'^.*?公网安备\d+号$',
            r'^技术支持[：:].*$',
        ]

        # 需要删除的完整行
        self.noise_full_lines = {
            '教务通知', '教学通知', '最新动态', '要闻推荐', '通知公告',
            '二级教学单位', '中外大学', '教育站点导航', '快速导航',
            '友情链接', '相关链接', '教学新闻', '媒体报道',
            'Class直录播平台', 'XD.智课', '教务管理系统', '教学日历',
            '本科教育教学节', '陕ICP备05016463号', '教学研究',
            '教学资源', '规章制度', '常用下载', '合作交流', '卓越计划',
            '教学意见信箱', '信息网络技术中心', '西电微教学',
        }

        # 新闻标题关键词
        self.news_keywords = ['杯', '大赛', '圆满', '成功', '荣获', '获奖',
                              '专项行动', '党日活动', '系列之', '取得', '重大突破',
                              '牵头发起', '联合', '成立']

    def is_bottom_noise(self, line):
        """判断是否为底部噪声(新闻标题、联系信息等)"""
        line_stripped = line.strip()

        if not line_stripped:
            return True

        # 检查是否是噪声行
        if line_stripped in self.noise_full_lines:
            return True

        # 检查联系信息模式
        for pattern in self.contact_patterns:
            if re.match(pattern, line_stripped):
                return True

        # 检查是否是底部新闻链接
        for pattern in self.bottom_news_patterns:
            if re.match(pattern, line_stripped):
                return True

        # 检查是否是新闻标题
        news_kw_count = sum(1 for kw in self.news_keywords if kw in line_stripped)
        if news_kw_count >= 1 and len(line_stripped) > 15:
            # 可能是新闻标题,但需要更多判断
            if not any(key in line_stripped for key in ['人工智能', 'AI', 'AIGC', '生成式']):
                return True

        # 以冒号结尾的短行(可能是表单标签)
        if line_stripped.endswith(':') or line_stripped.endswith('：'):
            if len(line_stripped) < 20:
                return True

        return False

    def clean_content(self, text):
        """清洗内容"""
        lines = text.split('\n')
        cleaned = []

        # 第一遍:删除明显的噪声行
        for line in lines:
            line_stripped = line.strip()

            if not line_stripped:
                continue

            if self.is_bottom_noise(line_stripped):
                continue

            cleaned.append(line_stripped)

        # 第二遍:删除底部开始的无关新闻列表
        # 找到第一个底部新闻的位置
        final_cleaned = []
        found_bottom_news_start = False

        for i, line in enumerate(cleaned):
            # 检查是否开始出现底部新闻
            if not found_bottom_news_start:
                # 如果这一行看起来像新闻标题,检查后续是否也是
                if any(kw in line for kw in self.news_keywords):
                    # 检查后续3行
                    if i + 2 < len(cleaned):
                        next_lines_are_news = sum(1 for next_line in cleaned[i+1:i+3]
                                                  if any(kw in next_line for kw in self.news_keywords))
                        if next_lines_are_news >= 1:
                            # 确认这里开始是底部新闻区域
                            found_bottom_news_start = True
                            break

                final_cleaned.append(line)

        return '\n'.join(final_cleaned)

    def clean_policy(self, policy):
        """清洗政策"""
        text = policy.get('content', '')

        if not text:
            return policy

        # 清洗内容
        text = self.clean_content(text)

        # 最终清理
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        policy['content'] = text.strip()
        policy['content_length'] = len(policy['content'])

        return policy

    def clean_all(self, input_file='data/policies_cleaned.json',
                  output_file='data/policies_cleaned_final.json'):
        """清洗所有政策"""
        print("=" * 60)
        print("最终数据清洗...")
        print("=" * 60)

        with open(input_file, 'r', encoding='utf-8') as f:
            policies = json.load(f)

        print(f"\n加载了 {len(policies)} 份政策文档")

        total_before = sum(len(p['content']) for p in policies)
        print(f"清洗前总字符数: {total_before}")

        cleaned_policies = []
        for i, policy in enumerate(policies, 1):
            print(f"\n[{i}/{len(policies)}] {policy['university']} - {policy['title'][:30]}...")
            length_before = len(policy['content'])

            cleaned = self.clean_policy(policy.copy())
            length_after = len(cleaned['content'])

            reduction = length_before - length_after
            print(f"  {length_before} -> {length_after} 字符 (减少 {reduction})")

            cleaned_policies.append(cleaned)

        total_after = sum(len(p['content']) for p in cleaned_policies)
        total_reduction = total_before - total_after

        print("\n" + "=" * 60)
        print("清洗完成!")
        print(f"总字符数: {total_before} -> {total_after}")
        print(f"总减少: {total_reduction} 字符 ({total_reduction/total_before*100:.1f}%)")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_policies, f, ensure_ascii=False, indent=2)

        print(f"\n已保存到: {output_file}")

        return cleaned_policies


if __name__ == '__main__':
    cleaner = PolicyDataCleanerFinal()
    cleaner.clean_all()
