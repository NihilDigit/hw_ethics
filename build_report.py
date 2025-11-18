#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键编译PDF工作流脚本（Python版本）
此脚本会自动运行所有分析步骤并生成最终的PDF报告
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """打印格式化的标题"""
    print(f"\n{'='*50}")
    print(text)
    print('='*50)

def print_step(step_num, total_steps, text):
    """打印步骤信息"""
    print(f"\n[{step_num}/{total_steps}] {text}")

def run_command(cmd, description, verbose=False):
    """运行shell命令"""
    try:
        if verbose:
            result = subprocess.run(cmd, shell=True, check=True,
                                  capture_output=False, text=True)
        else:
            result = subprocess.run(cmd, shell=True, check=True,
                                  capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        if not verbose and e.stderr:
            print(f"错误信息: {e.stderr[:500]}")
        return False

def main():
    """主函数"""
    print_header("国内双一流高校生成式AI政策分析报告\n一键编译PDF工作流")

    # 切换到脚本所在目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"\n工作目录: {script_dir}")

    # 步骤1: 检查Python依赖
    print_step(1, 5, "检查Python依赖...")
    try:
        import numpy
        import pandas
        import matplotlib
        import seaborn
        import networkx
        import sklearn
        import gensim
        print("✓ Python依赖检查完成")
    except ImportError as e:
        print(f"缺少依赖: {e}")
        print("正在安装Python依赖...")
        if not run_command(
            "pip install -q numpy pandas matplotlib seaborn networkx scikit-learn gensim",
            "安装依赖"
        ):
            print("错误: 依赖安装失败")
            return 1
        print("✓ Python依赖安装完成")

    # 步骤2: 检查数据
    print_step(2, 5, "检查数据文件...")
    if Path("data/processed_policies.json").exists():
        print("✓ 跳过文本预处理（数据已存在）")
    else:
        print("运行文本预处理...")
        if not run_command("python text_preprocessing.py", "文本预处理"):
            return 1
        print("✓ 文本预处理完成")

    # 步骤3: 运行分析脚本
    print_step(3, 5, "运行数据分析...")

    analyses = [
        ("python lda_analysis.py", "LDA主题模型分析"),
        ("python text_analysis.py", "TF-IDF和共现网络分析"),
        ("python visualization.py", "生成可视化图表"),
        ("python generate_summary_report.py", "生成数据汇总报告")
    ]

    for cmd, desc in analyses:
        print(f"  - {desc}...")
        if not run_command(cmd, desc):
            print(f"  警告: {desc}可能未完全成功")
        else:
            print(f"  ✓ {desc}完成")

    # 步骤4: 编译LaTeX为PDF
    print_step(4, 5, "编译LaTeX文档为PDF...")

    # 检查LaTeX编译器
    latex_cmd = None
    for cmd in ['xelatex', 'pdflatex']:
        if subprocess.run(f"command -v {cmd}", shell=True,
                        capture_output=True).returncode == 0:
            latex_cmd = cmd
            break

    if not latex_cmd:
        print("错误: 未找到LaTeX编译器 (xelatex或pdflatex)")
        print("请安装 texlive-xetex 或 texlive-latex-base")
        return 1

    tex_file = "国内双一流高校生成式人工智能相关政策分析.tex"
    pdf_file = tex_file.replace('.tex', '.pdf')

    print(f"  使用 {latex_cmd} 编译...")

    # 编译两次以确保交叉引用正确
    for i in range(2):
        cmd = f"{latex_cmd} -interaction=nonstopmode '{tex_file}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if i == 0:
            print(f"  第一次编译完成")
        else:
            print(f"  第二次编译完成")

    # 清理临时文件
    temp_extensions = ['.aux', '.log', '.out', '.toc', '.bbl', '.blg', '.synctex.gz']
    for ext in temp_extensions:
        for f in Path('.').glob(f'*{ext}'):
            f.unlink()

    if Path(pdf_file).exists():
        print(f"✓ PDF编译成功: {pdf_file}")
    else:
        print("✗ PDF编译失败")
        print("请查看LaTeX错误日志")
        return 1

    # 步骤5: 总结
    print_step(5, 5, "构建完成")

    print_header("报告生成成功！")

    print("\n生成的文件：")
    print(f"  📄 PDF报告: {pdf_file}")
    print(f"  📊 图表目录: figures/ ({len(list(Path('figures').glob('*.png')))} 个图表)")
    print(f"  📈 数据文件: data/")
    print(f"  📝 汇总报告: data/analysis_summary.md")

    print("\n快速查看：")
    print(f"  - 查看PDF: xdg-open '{pdf_file}' (Linux)")
    print(f"  - 查看PDF: open '{pdf_file}' (macOS)")
    print(f"  - 查看图表: ls -lh figures/")
    print()

    return 0

if __name__ == '__main__':
    sys.exit(main())
