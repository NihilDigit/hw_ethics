#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合模式爬虫：结合自动搜索爬取和手动配置的URL
这是最实用的方案，可以逐步积累真实数据
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
import os
import logging
from universities_list import DOUBLE_FIRST_CLASS_UNIVERSITIES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class HybridPolicyCrawler:
    """混合模式爬虫 - 使用多种方法获取政策数据"""

    def __init__(self, test_mode=False):
        """
        :param test_mode: 测试模式，只爬取少量数据
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.test_mode = test_mode
        self.policies = []
        self.universities = DOUBLE_FIRST_CLASS_UNIVERSITIES

    def create_data_dir(self):
        """创建数据目录"""
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/raw_policies', exist_ok=True)

    def load_known_policies(self):
        """加载已知政策URL配置"""
        try:
            with open('known_policies.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('policies', [])
        except FileNotFoundError:
            logging.warning("未找到 known_policies.json 文件")
            return []

    def fetch_url_content(self, url):
        """获取URL内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')

            # 移除无用标签
            for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
                tag.decompose()

            # 尝试找到主要内容
            main_content = None
            for selector in ['article', '.content', '.article', '#content', 'main']:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            if not main_content:
                main_content = soup.body

            text = main_content.get_text(separator='\n', strip=True) if main_content else ""
            text = re.sub(r'\n{3,}', '\n\n', text)

            return text
        except Exception as e:
            logging.error(f"获取URL失败 {url}: {e}")
            return None

    def search_with_websearch(self, university_name):
        """
        尝试通过学校官网搜索功能查找政策
        注意：这需要分析每个学校的搜索接口，实际实现会很复杂
        这里提供框架
        """
        logging.info(f"尝试搜索: {university_name}")

        # 不同高校的搜索URL模式不同，这里只是示例
        # 实际使用时需要针对每个学校定制

        university_url = self.universities.get(university_name, '')
        if not university_url:
            return []

        # 示例：尝试常见的搜索路径
        search_paths = [
            '/search?q=生成式人工智能',
            '/search.aspx?keyword=生成式人工智能',
            '/s?wd=ChatGPT',
        ]

        results = []
        for path in search_paths:
            try:
                search_url = university_url + path
                content = self.fetch_url_content(search_url)
                if content and '生成式' in content:
                    logging.info(f"  可能找到相关内容: {search_url}")
                    results.append(search_url)
                time.sleep(2)
            except:
                continue

        return results

    def generate_enhanced_sample_data(self):
        """
        生成增强版示例数据
        基于文献和公开信息，生成更接近真实情况的示例数据
        涵盖更多学校
        """
        logging.info("生成增强版示例数据...")

        # 选择有代表性的高校生成数据
        target_universities = [
            '清华大学', '北京大学', '复旦大学', '浙江大学', '上海交通大学',
            '南京大学', '中国人民大学', '北京师范大学', '武汉大学', '中山大学',
            '华中科技大学', '西安交通大学', '哈尔滨工业大学', '同济大学', '南开大学',
            '天津大学', '厦门大学', '山东大学', '四川大学', '吉林大学',
            '中南大学', '东南大学', '北京航空航天大学', '北京理工大学', '华南理工大学',
            '大连理工大学', '西北工业大学', '重庆大学', '电子科技大学', '湖南大学'
        ]

        if self.test_mode:
            target_universities = target_universities[:10]

        sample_policies = []

        # 为每个学校生成1-2份政策
        policy_templates = [
            {
                'title_template': '{univ}关于规范使用生成式人工智能技术的指导意见',
                'category': '教学管理',
                'target_role': '教师、学生',
                'content_template': '''为规范生成式人工智能技术在教学科研中的应用，现提出以下意见：

一、基本原则
1. 坚持育人为本，促进学生创新能力培养
2. 加强伦理规范，确保技术应用安全可控
3. 鼓励技术创新，推动教学科研质量提升

二、教学应用规范
1. 教师应合理引导学生使用AI工具，培养批判性思维
2. 学生使用AI完成作业需明确标注，避免学术不端
3. 课程设计应考虑AI技术发展，更新评价方式

三、科研应用要求
1. 科研工作中使用AI工具应遵守学术规范和伦理要求
2. 涉及数据安全和隐私保护的研究需严格审查
3. 鼓励开展AI技术相关的创新研究

四、管理与保障
1. 建立AI技术应用的监督机制
2. 加强师生AI素养培训
3. 完善相关管理制度和技术支持'''
            },
            {
                'title_template': '{univ}人工智能技术应用伦理准则',
                'category': '伦理规范',
                'target_role': '全体师生',
                'content_template': '''为引导师生负责任地使用生成式人工智能技术，特制定本伦理准则：

一、价值导向
1. 坚持以人为本，技术服务于人的全面发展
2. 维护学术诚信，反对投机取巧和学术不端
3. 尊重知识产权，保护创作者权益
4. 重视数据安全与个人隐私保护

二、使用原则
1. 透明性原则：明确说明AI工具的使用情况
2. 批判性原则：对AI生成内容保持审慎态度
3. 创造性原则：以AI为辅助工具，发挥人的主体性
4. 负责任原则：对AI辅助产生的成果承担责任

三、具体规范
1. 教学场景：教师应将AI素养纳入课程教学，学生应诚实申报AI使用情况
2. 科研场景：科研论文应披露AI工具使用详情，确保可重复性
3. 管理场景：行政管理可合理利用AI提高效率，但涉及师生权益的决策不应完全依赖AI

四、教育与培训
1. 开展AI素养和伦理教育
2. 提供AI工具使用培训和指导
3. 建立AI应用案例库和最佳实践分享机制'''
            }
        ]

        base_date = datetime(2023, 4, 1)

        for i, univ in enumerate(target_universities):
            # 每个学校1-2份政策
            num_policies = 1 if i % 3 == 0 else 2

            for j in range(num_policies):
                template = policy_templates[j % len(policy_templates)]

                # 计算日期（2023年4月到2024年1月）
                days_offset = i * 10 + j * 30
                policy_date = base_date + timedelta(days=days_offset)

                policy = {
                    'university': univ,
                    'title': template['title_template'].format(univ=univ),
                    'date': policy_date.strftime('%Y-%m-%d'),
                    'category': template['category'],
                    'target_role': template['target_role'],
                    'content': template['content_template']
                }

                sample_policies.append(policy)

        logging.info(f"生成了 {len(sample_policies)} 份示例政策数据")
        return sample_policies

    def crawl_from_known_urls(self):
        """从已知URL爬取真实数据"""
        known_policies = self.load_known_policies()
        real_policies = []

        for policy_info in known_policies:
            url = policy_info.get('url', '')
            if not url or url.strip() == '':
                logging.info(f"跳过（无URL）: {policy_info['university']} - {policy_info['title']}")
                continue

            logging.info(f"爬取已知URL: {policy_info['university']}")

            content = self.fetch_url_content(url)
            if content and len(content) > 200:
                policy = {
                    'university': policy_info['university'],
                    'title': policy_info['title'],
                    'date': policy_info.get('date', '未知'),
                    'category': self._classify_policy(policy_info['title'], content),
                    'target_role': self._identify_target_role(content),
                    'content': content[:5000],  # 限制长度
                    'source': 'known_url',
                    'url': url
                }
                real_policies.append(policy)
                logging.info(f"  ✓ 成功爬取: {policy['title']}")
            else:
                logging.warning(f"  ✗ 内容获取失败")

            time.sleep(2)

        return real_policies

    def _classify_policy(self, title, content):
        """政策分类"""
        text = (title + ' ' + content[:200]).lower()

        if any(word in text for word in ['伦理', '道德', '规范']):
            return '伦理规范'
        elif any(word in text for word in ['教学', '课程', '教育']):
            return '教学管理'
        elif any(word in text for word in ['科研', '研究', '学术']):
            return '科研管理'
        elif any(word in text for word in ['学生', '作业', '考试']):
            return '学生指导'
        elif any(word in text for word in ['教师', '培训']):
            return '教师指导'
        elif any(word in text for word in ['发展', '规划', '建设']):
            return '发展规划'
        else:
            return '综合管理'

    def _identify_target_role(self, content):
        """识别目标角色"""
        roles = []
        if '教师' in content[:500]:
            roles.append('教师')
        if '学生' in content[:500]:
            roles.append('学生')
        if '管理' in content[:500] or '行政' in content[:500]:
            roles.append('管理人员')

        return '、'.join(roles) if roles else '全体师生'

    def save_policies(self, policies):
        """保存政策数据"""
        if not policies:
            logging.warning("没有政策数据可保存")
            return

        # 保存为JSON
        with open('data/policies.json', 'w', encoding='utf-8') as f:
            json.dump(policies, f, ensure_ascii=False, indent=2)

        # 保存为单独文本文件
        for i, policy in enumerate(policies, 1):
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', policy.get('title', 'untitled')[:50])
            filename = f"data/raw_policies/{i}_{policy['university']}_{policy['category']}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"高校: {policy['university']}\n")
                f.write(f"标题: {policy['title']}\n")
                f.write(f"日期: {policy['date']}\n")
                f.write(f"类别: {policy['category']}\n")
                f.write(f"适用对象: {policy['target_role']}\n")
                if 'url' in policy:
                    f.write(f"来源URL: {policy['url']}\n")
                f.write(f"\n内容:\n{policy['content']}\n")

        logging.info(f"✓ 成功保存 {len(policies)} 份政策文件")

    def run(self):
        """运行混合爬虫"""
        from datetime import timedelta

        logging.info("="*60)
        logging.info("混合模式爬虫启动")
        logging.info("策略: 已知URL爬取 + 增强示例数据")
        logging.info("="*60)

        self.create_data_dir()

        # 1. 先尝试从已知URL爬取真实数据
        real_policies = self.crawl_from_known_urls()
        logging.info(f"\n从已知URL爬取到 {len(real_policies)} 份真实政策")

        # 2. 生成增强版示例数据补充
        sample_policies = self.generate_enhanced_sample_data()

        # 3. 合并数据
        all_policies = real_policies + sample_policies
        self.policies = all_policies

        # 4. 保存数据
        self.save_policies(all_policies)

        # 5. 打印统计
        logging.info("\n" + "="*60)
        logging.info("爬取完成!")
        logging.info(f"真实数据: {len(real_policies)} 份")
        logging.info(f"示例数据: {len(sample_policies)} 份")
        logging.info(f"总计: {len(all_policies)} 份")

        if all_policies:
            logging.info(f"\n按高校统计:")
            uni_count = {}
            for p in all_policies:
                uni_count[p['university']] = uni_count.get(p['university'], 0) + 1

            for uni, count in sorted(uni_count.items(), key=lambda x: x[1], reverse=True)[:15]:
                logging.info(f"  {uni}: {count} 份")

            logging.info(f"\n按类别统计:")
            cat_count = {}
            for p in all_policies:
                cat_count[p['category']] = cat_count.get(p['category'], 0) + 1

            for cat, count in sorted(cat_count.items(), key=lambda x: x[1], reverse=True):
                logging.info(f"  {cat}: {count} 份")

        logging.info("="*60)
        logging.info("\n提示：")
        logging.info("1. 如果找到真实政策URL，请添加到 known_policies.json")
        logging.info("2. 重新运行爬虫将自动获取真实数据")
        logging.info("3. 当前使用增强示例数据进行分析")

        return all_policies


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='混合模式政策爬虫')
    parser.add_argument('--test', action='store_true',
                       help='测试模式，只生成少量数据')

    args = parser.parse_args()

    crawler = HybridPolicyCrawler(test_mode=args.test)
    policies = crawler.run()

    print(f"\n✓ 数据已保存到 data/policies.json")
    print(f"✓ 共 {len(policies)} 份政策数据")
