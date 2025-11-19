#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版数据清洗脚本 - 更彻底地删除噪声
"""

import json
import re
from collections import Counter


class PolicyDataCleanerV2:
    def __init__(self):
        """初始化数据清洗器"""
        # 扩展的噪声关键词列表
        self.noise_keywords = {
            # 导航相关
            '首页', '网站首页', '学校主页', '返回', '旧版网站', '新版网站',
            '通知公告', '新闻动态', '学院动态', '教学信息', '机构简介',
            '学院简介', '部门简介', '学院概况', '组织机构', '机构设置',
            '领导团队', '领导分工', '师资队伍', '联系我们', '联系方式',
            '办事指南', '下载专区', '常用下载', '模板下载', '教学管理',
            '学生事务', '教师教学', '科学研究', '党建工作', '规章制度',
            '工作动态', '学术动态', '媒体报道', '快速导航', '站点导航',
            '友情链接', '相关链接', '教育部', '省教育厅', '信息服务',
            '校历', '作息时间', '留言板', '信箱', '院长信箱', '书记信箱',
            '旧版', '员工版', '国际版', 'English', 'ENGLISH',
            # 教务相关
            '学籍管理', '课程考试', '毕业学位', '交流交换', '课程管理',
            '教学业务', '奖项申报', '综合事务', '实践教学', '培养方案',
            '教学资源', '教学名师', '精品课程', '精品教材', '成果获奖',
            '通识课程', '专业与辅修', '教学日历', '教务管理系统',
            '教学发展中心', '本科教育教学节',
            # 医院相关
            '医院概况', '医院简介', '就诊服务', '预约挂号', '专家出诊',
            '体检服务', '医保服务', '护理到家', '就诊须知', '就医流程',
            '科室导航', '内科系统', '外科系统', '医技', '住院指南',
            '专家介绍', '医院要闻', '科室动态', '人文关怀', '媒体二院',
            '数字院报', '医护工作', '医疗动态', '护理动态', '住培专培',
            '继续教育', '教学之窗', '科研动态', '科研管理', '学科建设',
            '重点学科', '医工交叉', '信息公开', '医院环境', '行风建设',
            '医疗服务', '财务信息', '招标采购', '采购公告', '中标公告',
            '人才招聘', '微博', '微信公众号',
            # 图书馆相关
            '新闻动态', '赛事信息', '学分课程', '培训讲座', '在线学习资源',
            '数据库在线课堂', '信息素养慕课', '领导信箱', '收集站',
            # 其他
            '特别声明', '仅供参考', '不作为诊断', '医疗依据',
        }

        # 需要完全删除的行模式
        self.remove_line_patterns = [
            # 导航和链接
            r'^(首页|通知公告|新闻动态|教学信息|规章制度)\s*$',
            r'^(学院简介|机构设置|师资队伍|联系我们)\s*$',
            r'^(教学管理|科学研究|党建工作|学生事务)\s*$',
            r'^[A-Z]+\s*$',  # 全大写的导航词
            # 日期和元数据
            r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}\s*$',
            r'^\d{4}\.\d{1,2}\.\d{1,2}\s*$',
            r'^(发布|更新|时间|日期|来源|作者|编辑|审核|责编|主编|供稿单位)[：:].{0,100}$',
            r'^(浏览|点击|阅读)(次数|量)?[：:]?\s*\d*\s*$',
            # 链接和路径
            r'^/.{0,100}\.(html|htm|php)$',
            r'^www\.',
            r'^http',
            # 特殊符号包围
            r'^=+.{0,50}=+$',
            r'^\[\s*关闭\s*\]$',
            # 电话邮编等
            r'^(电话|邮编|地址)[：:].{0,100}$',
            r'^\d{5,}$',  # 长数字串
            # 版权信息
            r'^(Copyright|版权所有|All Rights Reserved)',
            r'^ICP备\d+号',
            # 按钮和操作
            r'^(打印|关闭|下载|返回|登录|注册)',
            # 附件
            r'^附件[【\[].*?[】\]]',
            # 无关链接
            r'^(中华人民共和国|教育部|陕西省)',
            r'^特别声明',
        ]

    def is_noise_line(self, line):
        """判断是否为噪声行"""
        line_stripped = line.strip()

        if not line_stripped or len(line_stripped) < 3:
            return True

        # 检查模式匹配
        for pattern in self.remove_line_patterns:
            if re.search(pattern, line_stripped, re.IGNORECASE):
                return True

        # 检查噪声关键词密度
        noise_count = sum(1 for kw in self.noise_keywords if kw in line_stripped)
        if noise_count >= 2:
            return True

        # 单独的噪声关键词行
        if line_stripped in self.noise_keywords:
            return True

        # 过短且无实质内容
        if len(line_stripped) < 10:
            has_meaningful = any(kw in line_stripped for kw in
                                 ['人工智能', 'AI', 'AIGC', '生成式', '教学', '学生', '教师',
                                  '管理', '政策', '规范', '伦理', '技术', '应用', '课程',
                                  '研究', '创新', '培养', '学习', '指南', '通知'])
            if not has_meaningful:
                return True

        return False

    def extract_policy_content(self, text, title):
        """提取政策实质内容"""
        lines = text.split('\n')
        content_lines = []
        in_content = False
        title_found = False

        # 尝试找到标题或关键起始点
        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if not line_stripped:
                continue

            # 跳过明显的噪声行
            if self.is_noise_line(line_stripped):
                continue

            # 寻找标题位置
            if not title_found and title:
                # 如果找到标题,标记为内容开始
                title_parts = [p for p in title.split() if len(p) > 5]
                if title_parts and any(part in line_stripped for part in title_parts[:2]):
                    title_found = True
                    in_content = True
                    if len(line_stripped) > 20:  # 标题行本身如果够长就保留
                        content_lines.append(line_stripped)
                    continue

            # 如果找到了类似通知标题的起始,开始收集内容
            if not in_content:
                if any(marker in line_stripped for marker in
                       ['通知', '公告', '关于', '各学院', '各单位', '为深入', '为加快',
                        '随着', '当今', '近日', '近年来', '自', '在']):
                    if len(line_stripped) > 15:
                        in_content = True
                        content_lines.append(line_stripped)
                        continue

            # 已经在内容区域
            if in_content:
                # 检查是否到达底部
                if any(end_marker in line_stripped for end_marker in
                       ['版权所有', 'Copyright', '友情链接', '快速导航', '相关链接',
                        '上一篇', '上一条', '最新动态', '通知公告', '要闻推荐']):
                    break

                content_lines.append(line_stripped)

        # 如果没找到内容,返回所有非噪声行
        if not content_lines:
            content_lines = [l.strip() for l in lines
                             if l.strip() and not self.is_noise_line(l.strip())]

        return '\n'.join(content_lines)

    def remove_duplicates(self, text):
        """删除重复的连续行"""
        lines = text.split('\n')
        result = []
        seen_recent = set()
        window_size = 3

        for i, line in enumerate(lines):
            line_normalized = re.sub(r'\s+', ' ', line.strip()).lower()

            if not line_normalized:
                continue

            # 检查最近的几行是否有相同内容
            if line_normalized in seen_recent:
                continue

            result.append(line.strip())

            # 维护滑动窗口
            seen_recent.add(line_normalized)
            if len(seen_recent) > window_size:
                # 移除最早的
                seen_recent = set(list(seen_recent)[1:])

        return '\n'.join(result)

    def final_polish(self, text):
        """最终润色"""
        # 删除URL残留
        text = re.sub(r'https?://[^\s]+', '', text)
        text = re.sub(r'www\.[^\s]+', '', text)
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)

        # 删除文件扩展名残留
        text = re.sub(r'\.(com|cn|edu|org|net|gov|html|htm|php|asp|jsp|pdf|docx?|xlsx?|pptx?)\b',
                      '', text, flags=re.IGNORECASE)

        # 删除路径
        text = re.sub(r'/[a-zA-Z0-9/_\-]+', '', text)

        # 删除多余的标点和空白
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # 最多两个换行
        text = re.sub(r' {2,}', ' ', text)

        # 删除孤立的单字符或两字符行
        lines = text.split('\n')
        filtered = []
        for line in lines:
            line_stripped = line.strip()
            if len(line_stripped) >= 3:  # 至少3个字符
                filtered.append(line_stripped)
            elif len(line_stripped) > 0 and any(c.isdigit() or c in '一二三四五六七八九十' for c in line_stripped):
                # 保留可能是编号的短行
                filtered.append(line_stripped)

        return '\n'.join(filtered)

    def clean_policy(self, policy):
        """清洗单个政策"""
        text = policy.get('content', '')
        title = policy.get('title', '')

        if not text:
            return policy

        # 1. 提取主要内容
        text = self.extract_policy_content(text, title)

        # 2. 删除重复内容
        text = self.remove_duplicates(text)

        # 3. 最终润色
        text = self.final_polish(text)

        policy['content'] = text
        policy['content_length'] = len(text)

        return policy

    def clean_all_policies(self, input_file='data/policies.json',
                           output_file='data/policies_cleaned.json'):
        """清洗所有政策"""
        print("=" * 60)
        print("开始数据清洗 (优化版 V2)...")
        print("=" * 60)

        with open(input_file, 'r', encoding='utf-8') as f:
            policies = json.load(f)

        print(f"\n加载了 {len(policies)} 份政策文档")

        total_length_before = sum(len(p['content']) for p in policies)
        print(f"清洗前总字符数: {total_length_before}")

        cleaned_policies = []
        for i, policy in enumerate(policies, 1):
            print(f"\n正在清洗 [{i}/{len(policies)}]: {policy['university']} - {policy['title'][:30]}...")
            length_before = len(policy['content'])

            cleaned_policy = self.clean_policy(policy.copy())
            length_after = len(cleaned_policy['content'])

            reduction = length_before - length_after
            reduction_pct = (reduction / length_before * 100) if length_before > 0 else 0

            print(f"  清洗前: {length_before} 字符")
            print(f"  清洗后: {length_after} 字符")
            print(f"  减少: {reduction} 字符 ({reduction_pct:.1f}%)")

            # 显示清洗后内容预览
            preview = cleaned_policy['content'][:150].replace('\n', ' ')
            print(f"  预览: {preview}...")

            cleaned_policies.append(cleaned_policy)

        total_length_after = sum(len(p['content']) for p in cleaned_policies)
        total_reduction = total_length_before - total_length_after
        total_reduction_pct = (total_reduction / total_length_before * 100) if total_length_before > 0 else 0

        print("\n" + "=" * 60)
        print("清洗完成!")
        print("=" * 60)
        print(f"清洗前总字符数: {total_length_before}")
        print(f"清洗后总字符数: {total_length_after}")
        print(f"总减少: {total_reduction} 字符 ({total_reduction_pct:.1f}%)")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_policies, f, ensure_ascii=False, indent=2)

        print(f"\n已保存清洗后的数据到: {output_file}")

        self.generate_report(cleaned_policies, output_file.replace('.json', '_report.txt'))

        return cleaned_policies

    def generate_report(self, policies, report_file):
        """生成清洗报告"""
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("数据清洗报告 (V2)\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"清洗文档数: {len(policies)}\n")
            f.write(f"平均内容长度: {sum(p['content_length'] for p in policies) / len(policies):.0f} 字符\n\n")

            for i, policy in enumerate(policies, 1):
                f.write(f"\n{i}. {policy['university']}\n")
                f.write(f"   标题: {policy['title']}\n")
                f.write(f"   类别: {policy['category']}\n")
                f.write(f"   内容长度: {policy['content_length']} 字符\n")
                f.write(f"   内容:\n")
                # 显示全部清洗后的内容
                f.write(f"   {policy['content']}\n")
                f.write(f"   {'-' * 60}\n")

        print(f"已生成清洗报告: {report_file}")


if __name__ == '__main__':
    cleaner = PolicyDataCleanerV2()
    cleaned_policies = cleaner.clean_all_policies()
