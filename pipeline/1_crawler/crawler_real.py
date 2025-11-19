#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国内双一流高校生成式人工智能政策文本爬虫（真实数据版本）
通过搜索引擎和网页爬取获取高校的真实政策文本
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import os
from urllib.parse import quote, urljoin
from universities_list import DOUBLE_FIRST_CLASS_UNIVERSITIES
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class RealUniversityPolicyCrawler:
    def __init__(self, max_universities=None, delay=2):
        """
        初始化爬虫
        :param max_universities: 限制爬取的大学数量（用于测试），None表示爬取所有
        :param delay: 请求之间的延迟（秒）
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        # 获取大学列表
        universities_dict = DOUBLE_FIRST_CLASS_UNIVERSITIES.copy()
        if max_universities:
            universities_dict = dict(list(universities_dict.items())[:max_universities])

        self.universities = universities_dict
        self.delay = delay

        # 搜索关键词组合（优化后更精准）
        self.keywords = [
            '生成式人工智能 使用规定',
            '生成式人工智能 管理办法',
            'ChatGPT 使用 规定',
            '人工智能 使用 管理',
            'AI工具 使用规范',
            '生成式AI 管理规定',
            '大语言模型 使用 管理',
            '人工智能 伦理',
        ]

        self.policies = []
        self.failed_universities = []

    def create_data_dir(self):
        """创建数据存储目录"""
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/raw_policies', exist_ok=True)

    def search_university_policy(self, university_name, keyword, university_url=''):
        """
        使用百度搜索查找高校政策
        :param university_name: 大学名称
        :param keyword: 搜索关键词
        :param university_url: 大学官网URL
        :return: 搜索结果列表
        """
        search_query = f"{university_name} {keyword} site:.edu.cn"
        encoded_query = quote(search_query)

        # 使用百度搜索
        search_url = f"https://www.baidu.com/s?wd={encoded_query}"

        try:
            time.sleep(self.delay)  # 延迟避免被封
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            # 解析百度搜索结果
            for result in soup.select('.result'):
                title_elem = result.select_one('h3 a')
                url_elem = result.select_one('a')
                abstract_elem = result.select_one('.c-abstract')

                if title_elem and url_elem:
                    title = title_elem.get_text().strip()
                    url = url_elem.get('href', '')
                    abstract = abstract_elem.get_text().strip() if abstract_elem else ''

                    # 过滤相关结果
                    if self._is_relevant_result(title, abstract, university_name):
                        priority = self._get_url_priority(url, university_url)
                        results.append({
                            'title': title,
                            'url': url,
                            'abstract': abstract,
                            'priority': priority
                        })

            # 按优先级排序
            results.sort(key=lambda x: x['priority'], reverse=True)
            return results[:5]  # 取前5个结果（增加候选）

        except Exception as e:
            logging.error(f"搜索失败 {university_name} - {keyword}: {str(e)}")
            return []

    def _is_relevant_result(self, title, abstract, university_name):
        """判断搜索结果是否相关"""
        text = (title + ' ' + abstract).lower()

        # 必须包含学校名
        if university_name not in text:
            return False

        # 包含相关关键词
        relevant_keywords = [
            '生成式', 'chatgpt', '人工智能', 'ai', '大语言模型',
            '政策', '规定', '办法', '通知', '意见', '指南', '规范'
        ]

        return any(keyword in text for keyword in relevant_keywords)

    def _get_url_priority(self, url, university_url):
        """
        评估URL优先级，优先选择学校官网
        :return: 优先级分数，分数越高优先级越高
        """
        score = 0
        url_lower = url.lower()

        # 提取学校官网域名
        from urllib.parse import urlparse
        uni_domain = urlparse(university_url).netloc
        if uni_domain:
            # 去掉www.
            uni_domain = uni_domain.replace('www.', '')
            if uni_domain in url_lower:
                score += 100  # 学校官网最高优先级

        # 教育机构域名优先
        if '.edu.cn' in url_lower:
            score += 50

        # 政府域名次优先
        if '.gov.cn' in url_lower:
            score += 30

        # 降低新闻媒体网站优先级
        news_sites = ['sohu.com', 'sina.com', '163.com', 'qq.com', 'baidu.com',
                     'toutiao.com', 'ifeng.com', 'netease.com', 'tencent.com']
        if any(site in url_lower for site in news_sites):
            score -= 50

        return score

    def fetch_page_content(self, url):
        """
        获取网页内容
        :param url: 网页URL
        :return: 提取的文本内容
        """
        try:
            # 如果是百度链接，先解析真实URL
            if 'baidu.com' in url:
                real_url = self._get_real_url_from_baidu(url)
                if not real_url:
                    return None
                url = real_url

            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')

            # 移除脚本和样式
            for script in soup(['script', 'style', 'nav', 'header', 'footer']):
                script.decompose()

            # 尝试找到主要内容区域
            main_content = None
            content_selectors = [
                'article', '.content', '.article', '#content',
                '.main-content', '.post-content', '.entry-content',
                'main', '[role="main"]'
            ]

            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            if not main_content:
                main_content = soup.body

            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
                # 清理多余空行
                text = re.sub(r'\n{3,}', '\n\n', text)
                return text

            return None

        except Exception as e:
            logging.error(f"获取页面内容失败 {url}: {str(e)}")
            return None

    def _get_real_url_from_baidu(self, baidu_url):
        """从百度链接中解析真实URL"""
        try:
            response = requests.get(baidu_url, headers=self.headers, timeout=10, allow_redirects=True)
            return response.url
        except:
            return None

    def extract_policy_info(self, content, title, university_name, url=''):
        """
        从内容中提取政策信息
        :param content: 网页文本内容
        :param title: 标题
        :param university_name: 大学名称
        :param url: 网页URL
        :return: 政策信息字典
        """
        if not content or len(content) < 100:
            return None

        # 检查内容质量
        if not self._is_quality_content(content, title):
            return None

        # 提取日期（多种模式）
        date = self._extract_date(content, title)

        # 分类
        category = self._classify_policy(title, content)

        # 确定目标角色
        target_role = self._identify_target_role(content)

        # 限制内容长度
        max_length = 5000
        if len(content) > max_length:
            content = content[:max_length] + '...'

        return {
            'university': university_name,
            'title': title,
            'date': date,
            'category': category,
            'target_role': target_role,
            'content': content,
            'url': url
        }

    def _is_quality_content(self, content, title):
        """检查内容质量"""
        # 检查是否包含太多无关内容
        bad_indicators = [
            '返回搜狐，查看更多',
            '特别声明：以上内容',
            '为自媒体平台',
            '仅提供信息存储服务',
            '阅读下一篇',
            '下载网易新闻客户端'
        ]

        # 如果内容主要是这些无关文本，则质量不合格
        bad_count = sum(1 for indicator in bad_indicators if indicator in content[:500])
        if bad_count >= 2:
            return False

        # 检查有效内容比例
        effective_content = content[:1000]
        # 至少应该包含一些政策相关词汇
        policy_words = ['政策', '规定', '办法', '通知', '要求', '管理', '使用', '规范', '指南']
        if not any(word in effective_content for word in policy_words):
            return False

        return True

    def _extract_date(self, content, title):
        """提取日期（多种模式）"""
        # 尝试多种日期格式
        date_patterns = [
            r'(\d{4})[-年/.](\d{1,2})[-月/.](\d{1,2})',  # 2024-01-01, 2024年1月1日
            r'(\d{4})[-年/.](\d{1,2})',  # 2024-01, 2024年1月
        ]

        # 先在标题中查找
        for pattern in date_patterns:
            match = re.search(pattern, title)
            if match:
                if len(match.groups()) == 3:
                    return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                else:
                    return f"{match.group(1)}-{match.group(2).zfill(2)}-01"

        # 在内容前1000字符中查找
        for pattern in date_patterns:
            match = re.search(pattern, content[:1000])
            if match:
                if len(match.groups()) == 3:
                    return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                else:
                    return f"{match.group(1)}-{match.group(2).zfill(2)}-01"

        return '未知'

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
        if '管理' in content[:500]:
            roles.append('管理人员')

        return '、'.join(roles) if roles else '全体师生'

    def crawl_university(self, university_name, university_url):
        """
        爬取单个大学的政策
        :param university_name: 大学名称
        :param university_url: 大学官网
        :return: 找到的政策列表
        """
        logging.info(f"正在爬取: {university_name}")
        found_policies = []

        # 尝试不同的关键词搜索
        for keyword in self.keywords[:2]:  # 只用前2个关键词避免请求过多
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

                        # 每个学校最多找2份政策
                        if len(found_policies) >= 2:
                            break
                    else:
                        logging.info(f"  ✗ 内容质量不合格，跳过")

            if found_policies:
                break  # 找到政策就不继续其他关键词了

        if not found_policies:
            logging.warning(f"  ✗ 未找到相关政策: {university_name}")
            self.failed_universities.append(university_name)

        return found_policies

    def save_policies(self, policies):
        """保存政策数据"""
        if not policies:
            logging.warning("没有政策数据可保存")
            return

        # 保存为JSON格式
        with open('data/policies.json', 'w', encoding='utf-8') as f:
            json.dump(policies, f, ensure_ascii=False, indent=2)

        # 保存为单独的文本文件
        for i, policy in enumerate(policies, 1):
            # 清理文件名中的特殊字符，保留完整标题用于内容
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', policy['title'][:80])
            filename = f"data/raw_policies/{i}_{policy['university']}_{safe_title}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"高校: {policy['university']}\n")
                f.write(f"标题: {policy['title']}\n")  # 保存完整标题
                f.write(f"日期: {policy['date']}\n")
                f.write(f"类别: {policy['category']}\n")
                f.write(f"适用对象: {policy['target_role']}\n")
                f.write(f"来源URL: {policy.get('url', '未知')}\n")
                f.write(f"\n内容:\n{policy['content']}\n")

        logging.info(f"成功保存 {len(policies)} 份政策文件")

    def save_crawler_report(self):
        """保存爬取报告"""
        report = {
            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_universities': len(self.universities),
            'successful': len(self.universities) - len(self.failed_universities),
            'failed': len(self.failed_universities),
            'failed_list': self.failed_universities,
            'total_policies': len(self.policies)
        }

        with open('data/crawler_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logging.info(f"\n爬取报告已保存到 data/crawler_report.json")

    def run(self):
        """运行爬虫"""
        logging.info("="*60)
        logging.info("开始爬取国内双一流高校生成式人工智能政策...")
        logging.info(f"目标高校数量: {len(self.universities)}")
        logging.info("="*60)

        self.create_data_dir()

        for i, (university_name, university_url) in enumerate(self.universities.items(), 1):
            logging.info(f"\n[{i}/{len(self.universities)}] {university_name}")

            try:
                policies = self.crawl_university(university_name, university_url)
                self.policies.extend(policies)
            except Exception as e:
                logging.error(f"爬取异常 {university_name}: {str(e)}")
                self.failed_universities.append(university_name)

        # 保存数据
        self.save_policies(self.policies)
        self.save_crawler_report()

        # 打印统计信息
        logging.info("\n" + "="*60)
        logging.info("爬取完成!")
        logging.info(f"成功: {len(self.universities) - len(self.failed_universities)}/{len(self.universities)}")
        logging.info(f"总计政策: {len(self.policies)} 份")

        if self.policies:
            logging.info(f"\n按高校统计:")
            uni_count = {}
            for p in self.policies:
                uni_count[p['university']] = uni_count.get(p['university'], 0) + 1
            for uni, count in sorted(uni_count.items(), key=lambda x: x[1], reverse=True)[:10]:
                logging.info(f"  {uni}: {count} 份")

            logging.info(f"\n按类别统计:")
            cat_count = {}
            for p in self.policies:
                cat_count[p['category']] = cat_count.get(p['category'], 0) + 1
            for cat, count in sorted(cat_count.items(), key=lambda x: x[1], reverse=True):
                logging.info(f"  {cat}: {count} 份")

        logging.info("="*60)

        return self.policies


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='爬取双一流高校生成式AI政策')
    parser.add_argument('--max', type=int, default=None,
                       help='限制爬取的大学数量（用于测试），默认爬取所有')
    parser.add_argument('--delay', type=float, default=2.0,
                       help='请求之间的延迟秒数，默认2秒')

    args = parser.parse_args()

    crawler = RealUniversityPolicyCrawler(
        max_universities=args.max,
        delay=args.delay
    )

    policies = crawler.run()

    if policies:
        print(f"\n✓ 成功爬取 {len(policies)} 份政策")
        print(f"数据已保存到 data/policies.json")
    else:
        print("\n✗ 未能爬取到任何政策，请检查网络连接或调整搜索策略")
