#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
针对失败大学的重试爬虫
使用更多关键词和更深入的搜索策略
"""

import json
from crawler_real import RealUniversityPolicyCrawler
from universities_list import DOUBLE_FIRST_CLASS_UNIVERSITIES
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler_retry.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class RetryFailedUniversitiesCrawler(RealUniversityPolicyCrawler):
    """针对失败大学的改进爬虫"""

    def __init__(self, failed_universities_list, delay=2):
        # 只爬取失败的大学
        universities_dict = {
            name: DOUBLE_FIRST_CLASS_UNIVERSITIES[name]
            for name in failed_universities_list
            if name in DOUBLE_FIRST_CLASS_UNIVERSITIES
        }

        super().__init__(max_universities=None, delay=delay)
        self.universities = universities_dict

        # 使用更多更精准的关键词
        self.keywords = [
            '生成式人工智能 使用规定',
            '生成式人工智能 管理办法',
            'ChatGPT 使用 规定',
            '人工智能 使用 管理办法',
            'AI工具 使用规范',
            '生成式AI 管理',
            '大语言模型 使用',
            '人工智能 伦理规范',
            '人工智能技术 管理',
            'AIGC 使用规定',
        ]

    def crawl_university(self, university_name, university_url):
        """
        改进的大学爬取方法 - 尝试更多关键词
        """
        logging.info(f"正在重试爬取: {university_name}")
        found_policies = []

        # 尝试更多关键词（前4个而不是前2个）
        for keyword in self.keywords[:4]:
            search_results = self.search_university_policy(university_name, keyword, university_url)

            for result in search_results:
                logging.info(f"  找到结果: {result['title'][:60]}... (优先级: {result.get('priority', 0)})")

                # 获取页面内容
                content = self.fetch_page_content(result['url'])
                if content:
                    policy_info = self.extract_policy_info(
                        content,
                        result['title'],
                        university_name,
                        result['url']
                    )

                    if policy_info and len(policy_info['content']) > 200:
                        found_policies.append(policy_info)
                        logging.info(f"  ✓ 成功提取政策: {policy_info['title'][:60]}...")

                        # 找到1份政策就够了
                        if len(found_policies) >= 1:
                            break
                    else:
                        logging.info(f"  ✗ 内容质量不合格，跳过")

            if found_policies:
                break  # 找到政策就不继续其他关键词了

        if not found_policies:
            logging.warning(f"  ✗ 重试后仍未找到相关政策: {university_name}")
            self.failed_universities.append(university_name)

        return found_policies


def main():
    # 读取第一轮爬取的失败列表
    with open('data/crawler_report.json', 'r', encoding='utf-8') as f:
        report = json.load(f)

    failed_list = report['failed_list']

    logging.info("="*60)
    logging.info(f"开始重试爬取失败的 {len(failed_list)} 所大学...")
    logging.info("="*60)

    # 创建重试爬虫
    crawler = RetryFailedUniversitiesCrawler(failed_list, delay=2.0)

    # 运行爬虫
    new_policies = crawler.run()

    # 合并结果
    if new_policies:
        # 读取原有政策
        try:
            with open('data/policies.json', 'r', encoding='utf-8') as f:
                existing_policies = json.load(f)
        except:
            existing_policies = []

        # 合并并保存
        all_policies = existing_policies + new_policies
        with open('data/policies.json', 'w', encoding='utf-8') as f:
            json.dump(all_policies, f, ensure_ascii=False, indent=2)

        logging.info(f"\n✓ 第二轮成功爬取 {len(new_policies)} 份新政策")
        logging.info(f"总计政策: {len(all_policies)} 份")

        # 更新总报告
        total_successful = report['successful'] + (len(failed_list) - len(crawler.failed_universities))
        total_failed = len(crawler.failed_universities)

        final_report = {
            'crawl_time': crawler.policies[0]['date'] if crawler.policies else report['crawl_time'],
            'round_1': {
                'successful': report['successful'],
                'failed': report['failed'],
                'policies': report['total_policies']
            },
            'round_2': {
                'attempted': len(failed_list),
                'successful': len(failed_list) - len(crawler.failed_universities),
                'still_failed': len(crawler.failed_universities),
                'new_policies': len(new_policies)
            },
            'total': {
                'universities': 146,
                'successful': total_successful,
                'failed': total_failed,
                'policies': len(all_policies)
            },
            'still_failed_list': crawler.failed_universities
        }

        with open('data/crawler_report_final.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)

        logging.info(f"\n最终统计: {total_successful}/146 所大学成功，共 {len(all_policies)} 份政策")
    else:
        logging.info("\n✗ 第二轮未能爬取到新政策")


if __name__ == '__main__':
    main()
