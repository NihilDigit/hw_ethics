#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的政策文本数据清洗脚本
目标: 移除网站框架、导航菜单、元数据等噪声，保留政策实质内容
"""

import json
import re
from collections import Counter
import os


class PolicyDataCleaner:
    def __init__(self):
        """初始化数据清洗器"""
        # 导航和菜单相关关键词
        self.navigation_keywords = {
            '首页', '返回首页', '网站首页', '学校主页', '学院首页',
            '通知公告', '新闻动态', '学院动态', '教学信息', '科研信息',
            '机构简介', '学院简介', '部门简介', '学院概况', '机构设置',
            '组织机构', '领导团队', '领导分工', '师资队伍', '联系我们',
            '联系方式', '办事指南', '下载专区', '常用下载', '模板下载',
            '教学管理', '学生事务', '教师教学', '科学研究', '党建工作',
            '规章制度', '政策文件', '工作动态', '学术动态', '媒体报道',
            '快速导航', '站点导航', '教育站点导航', '友情链接', '相关链接',
            '二级教学单位', '中外大学', '教育部', '省教育厅',
            '学籍管理', '课程考试', '毕业学位', '交流交换', '课程管理',
            '教学业务', '奖项申报', '综合事务', '实践教学', '培养方案',
            '教学资源', '教学名师', '精品课程', '精品教材', '成果获奖',
            '通识课程', '专业与辅修', '信息服务', '校历', '作息时间',
            '留言板', '处长信箱', '书记信箱', '院长信箱', '领导信箱',
            '旧版网站', '进入旧版', '新版网站', '员工版', '国际版',
            '中文', 'English', 'ENGLISH',
        }

        # 医院相关噪声词汇
        self.hospital_keywords = {
            '医院概况', '医院简介', '就诊服务', '预约挂号', '专家出诊',
            '体检服务', '医保服务', '护理到家', '就诊须知', '就医流程',
            '多学科诊疗', '特色医疗', '来院交通', '住院指南', '价格公示',
            '科室导航', '内科系统', '外科系统', '医技', '平台', '病院',
            '中心', '专家介绍', '新闻中心', '医院要闻', '综合新闻',
            '科室动态', '人文关怀', '媒体二院', '数字院报', '医护工作',
            '医疗动态', '护理动态', '医学教育', '本科生教育', '研究生教育',
            '住培专培', '继续教育', '教学之窗', '科研动态', '科研管理',
            '学科建设', '重点学科', '医工交叉', '信息公开', '医院环境',
            '行风建设', '医疗服务', '财务信息', '招标采购', '采购公告',
            '中标公告', '人才招聘', '微博', '微信公众号',
        }

        # 图书馆相关噪声词汇
        self.library_keywords = {
            '新闻动态', '赛事信息', '学分课程', '培训讲座', '预约培训讲座',
            '小微课堂', '检索技术篇', '信息资源篇', '科研助手篇', '知识产权篇',
            'AI素养专题', 'AI术语', 'AI工具导航', 'AI政策文件',
            'AIGC使用规范及著录建议', '在线学习资源', '数据库在线课堂',
            '信息素养慕课', '领导信箱', '收集站', 'iFree讲座',
        }

        # 元数据标签
        self.metadata_labels = {
            '发布日期', '发布时间', '更新日期', '时间', '日期',
            '浏览次数', '点击次数', '阅读', '已浏览',
            '信息来源', '来源', '资料来源', '作者', '责编', '主编',
            '编辑', '审核人', '审核', '责任编辑', '供稿单位',
            '当前位置', '位置', '您现在的位置',
        }

        # 操作按钮
        self.action_buttons = [
            r'【[^】]*打印[^】]*】', r'【[^】]*关闭[^】]*】', r'【[^】]*下载[^】]*】',
            r'打印本页', r'关闭本页', r'关闭窗口', r'返回.*?页',
            r'上一篇[：:]', r'下一篇[：:]', r'上一条[：:]', r'下一条[：:]',
        ]

        # 联系和版权信息模式
        self.contact_patterns = [
            r'地址[：:].{0,100}',
            r'邮编[：:].{0,50}',
            r'电话[：:].{0,100}',
            r'邮箱[：:].{0,100}',
            r'联系电话[：:].{0,100}',
            r'Copyright\s*©.{0,200}',
            r'版权所有.{0,100}',
            r'All Rights Reserved',
            r'ICP备\d+号',
            r'公网安备\d+号',
            r'站点建设与维护.{0,100}',
            r'技术支持.{0,100}',
        ]

        # 高校名称列表(用于识别友情链接区域)
        self.university_names = {
            '清华大学', '北京大学', '上海交通大学', '浙江大学', '南京大学',
            '复旦大学', '哈尔滨工业大学', '中国科学技术大学', '西安交通大学',
            '北京航空航天大学', '华中科技大学', '武汉大学', '中山大学',
            '哈佛大学', '斯坦福大学', '麻省理工', '牛津大学', '剑桥大学',
            '伯克利加州大学', '耶鲁大学', '普林斯顿大学',
        }

    def remove_navigation_blocks(self, text):
        """删除导航菜单块"""
        lines = text.split('\n')
        cleaned_lines = []
        skip_count = 0

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # 检查是否为导航行
            if skip_count > 0:
                skip_count -= 1
                continue

            # 统计导航关键词密度
            all_nav_keywords = self.navigation_keywords | self.hospital_keywords | self.library_keywords
            nav_keyword_count = sum(1 for kw in all_nav_keywords if kw in line)

            # 如果一行中有多个导航关键词,很可能是导航菜单
            if nav_keyword_count >= 2 or (len(line) < 20 and nav_keyword_count >= 1):
                # 跳过后续可能相关的行
                skip_count = 0
                continue

            # 删除单独的导航关键词行
            if line in all_nav_keywords:
                continue

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def remove_breadcrumbs(self, text):
        """删除面包屑导航"""
        # 匹配 "首页 > 新闻 > 公告" 或 "首页 -> 新闻 -> 公告" 模式
        text = re.sub(r'[^\n]*?(?:首页|主页|Home)\s*[>→\-]+\s*.{0,100}(?:正文|详情)', '', text)
        text = re.sub(r'当前位置[：:].{0,100}(?:正文|详情)', '', text)
        text = re.sub(r'位置[：:].{0,100}(?:正文|详情)', '', text)
        return text

    def remove_metadata_lines(self, text):
        """删除元数据行"""
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            line_stripped = line.strip()
            # 检查是否是元数据行
            is_metadata = False
            for label in self.metadata_labels:
                if line_stripped.startswith(label) or f'{label}:' in line_stripped or f'{label}：' in line_stripped:
                    is_metadata = True
                    break

            if not is_metadata:
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def remove_action_buttons(self, text):
        """删除操作按钮"""
        for pattern in self.action_buttons:
            text = re.sub(pattern, '', text)
        return text

    def remove_contact_info(self, text):
        """删除联系和版权信息"""
        for pattern in self.contact_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text

    def remove_url_and_paths(self, text):
        """删除URL和路径"""
        # 删除完整URL
        text = re.sub(r'https?://[^\s]+', ' ', text)
        text = re.sub(r'www\.[^\s]+', ' ', text)

        # 删除邮箱
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ' ', text)

        # 删除路径
        text = re.sub(r'/[a-zA-Z0-9/_\-\.]+\.(?:html|htm|php|asp|jsp|pdf|doc|docx)', ' ', text)

        # 删除域名后缀
        text = re.sub(r'\.(com|cn|edu|net|org|gov|html|htm|php|asp|jsp)\b', ' ', text, flags=re.IGNORECASE)

        return text

    def remove_delimited_text(self, text):
        """删除特殊分隔符包围的文本"""
        # 删除 == 包围的文本
        text = re.sub(r'==.{0,50}==', ' ', text)
        return text

    def remove_duplicate_blocks(self, text):
        """删除重复文本块"""
        lines = text.split('\n')
        # 使用滑动窗口检测重复块
        window_size = 5
        seen_blocks = set()
        cleaned_lines = []

        for i in range(len(lines)):
            if i + window_size <= len(lines):
                block = '\n'.join(lines[i:i+window_size])
                block_normalized = re.sub(r'\s+', ' ', block).strip()

                if block_normalized and block_normalized in seen_blocks:
                    # 跳过重复块
                    continue
                else:
                    seen_blocks.add(block_normalized)

            cleaned_lines.append(lines[i])

        return '\n'.join(cleaned_lines)

    def remove_university_link_sections(self, text):
        """删除高校名称列表(友情链接区域)"""
        lines = text.split('\n')
        cleaned_lines = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # 统计高校名称出现次数
            uni_count = sum(1 for uni in self.university_names if uni in line_stripped)

            # 如果一行包含多个高校名称,很可能是链接区域
            if uni_count >= 2:
                continue

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def extract_main_content(self, text, title):
        """提取主要内容"""
        lines = text.split('\n')
        content_lines = []
        found_title = False
        content_started = False

        for line in lines:
            line_stripped = line.strip()

            if not line_stripped:
                continue

            # 跳过标题之前的内容
            if not found_title:
                if title and any(part in line_stripped for part in title.split() if len(part) > 3):
                    found_title = True
                    content_started = True
                continue

            # 检查是否到达底部区域
            if any(keyword in line_stripped for keyword in ['版权所有', 'Copyright', '友情链接']):
                break

            if content_started:
                content_lines.append(line_stripped)

        # 如果没找到标题,返回所有内容
        if not content_lines:
            return '\n'.join([l.strip() for l in lines if l.strip()])

        return '\n'.join(content_lines)

    def clean_text_final(self, text):
        """最终文本清理"""
        # 删除多余空白
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r' +', ' ', text)

        # 删除过短的行(可能是残留的噪声)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line_stripped = line.strip()
            # 保留至少10个字符的行,或包含关键政策词汇的短行
            if len(line_stripped) >= 10 or any(kw in line_stripped for kw in
                                                ['人工智能', 'AI', '生成式', '教学', '管理', '政策']):
                cleaned_lines.append(line_stripped)

        return '\n'.join(cleaned_lines).strip()

    def clean_policy(self, policy):
        """清洗单个政策文档"""
        text = policy.get('content', '')
        title = policy.get('title', '')

        if not text:
            return policy

        # 阶段1: 结构化噪声删除
        text = self.remove_navigation_blocks(text)
        text = self.remove_breadcrumbs(text)
        text = self.remove_metadata_lines(text)
        text = self.remove_action_buttons(text)

        # 阶段2: 模式匹配删除
        text = self.remove_contact_info(text)
        text = self.remove_url_and_paths(text)
        text = self.remove_delimited_text(text)
        text = self.remove_university_link_sections(text)

        # 阶段3: 重复内容删除
        text = self.remove_duplicate_blocks(text)

        # 阶段4: 提取主要内容
        text = self.extract_main_content(text, title)

        # 阶段5: 最终清理
        text = self.clean_text_final(text)

        # 更新政策内容
        policy['content'] = text
        policy['content_length'] = len(text)

        return policy

    def clean_all_policies(self, input_file='data/policies.json',
                           output_file='data/policies_cleaned.json'):
        """清洗所有政策文档"""
        print("=" * 60)
        print("开始数据清洗...")
        print("=" * 60)

        # 加载数据
        with open(input_file, 'r', encoding='utf-8') as f:
            policies = json.load(f)

        print(f"\n加载了 {len(policies)} 份政策文档")

        # 清洗前统计
        total_length_before = sum(len(p['content']) for p in policies)
        print(f"清洗前总字符数: {total_length_before}")

        # 清洗每个文档
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

            cleaned_policies.append(cleaned_policy)

        # 清洗后统计
        total_length_after = sum(len(p['content']) for p in cleaned_policies)
        total_reduction = total_length_before - total_length_after
        total_reduction_pct = (total_reduction / total_length_before * 100) if total_length_before > 0 else 0

        print("\n" + "=" * 60)
        print("清洗完成!")
        print("=" * 60)
        print(f"清洗前总字符数: {total_length_before}")
        print(f"清洗后总字符数: {total_length_after}")
        print(f"总减少: {total_reduction} 字符 ({total_reduction_pct:.1f}%)")

        # 保存清洗后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_policies, f, ensure_ascii=False, indent=2)

        print(f"\n已保存清洗后的数据到: {output_file}")

        # 生成清洗报告
        self.generate_cleaning_report(cleaned_policies, output_file.replace('.json', '_report.txt'))

        return cleaned_policies

    def generate_cleaning_report(self, policies, report_file):
        """生成清洗报告"""
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("数据清洗报告\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"清洗文档数: {len(policies)}\n\n")

            for i, policy in enumerate(policies, 1):
                f.write(f"{i}. {policy['university']} - {policy['title']}\n")
                f.write(f"   内容长度: {policy['content_length']} 字符\n")
                f.write(f"   内容预览: {policy['content'][:100]}...\n\n")

        print(f"已生成清洗报告: {report_file}")


if __name__ == '__main__':
    cleaner = PolicyDataCleaner()
    cleaned_policies = cleaner.clean_all_policies()
