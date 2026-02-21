#!/usr/bin/env python3
"""
GitHub Green Wall 刷贡献工具
用法:
  python green_wall.py --start 2025-01-01 --end 2025-12-31 --intensity 3
  python green_wall.py --today --intensity 5
  python green_wall.py --pattern random --start 2025-01-01 --end 2025-12-31
"""

import subprocess
import os
import random
from datetime import datetime, timedelta
import argparse

# ───────────────────────────────────────────────
# 配置区（可修改）
# ───────────────────────────────────────────────
COMMIT_FILE = "contributions.txt"  # 用于写入的占位文件
AUTHOR_NAME = "ZSFan888"           # 你的 GitHub 用户名
AUTHOR_EMAIL = "your@email.com"    # 你的 GitHub 邮箱（需与 GitHub 账号绑定）


def run(cmd, env=None):
    """执行 shell 命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr.strip()}")
    return result.stdout.strip()


def make_commit(date: datetime, index: int):
    """在指定日期创建一次 commit"""
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    # 写入内容（每次略有不同，避免 empty commit）
    with open(COMMIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date_str} - commit #{index}\n")

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL

    run(f'git add {COMMIT_FILE}', env=env)
    run(f'git commit -m "contribution: {date_str}"', env=env)
    print(f"  ✅ Committed: {date_str}")


def date_range(start: datetime, end: datetime):
    """生成日期范围"""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def fill_range(start: datetime, end: datetime, intensity: int, skip_weekends: bool):
    """
    在日期范围内，每天提交 intensity 次
    intensity: 1=浅绿, 3=中绿, 5+=深绿
    """
    total = 0
    for day in date_range(start, end):
        if skip_weekends and day.weekday() >= 5:  # 跳过周末
            continue
        for i in range(intensity):
            make_commit(day.replace(hour=9 + i, minute=random.randint(0, 59)), total)
            total += 1
    print(f"\n🎉 共创建 {total} 个 commits")


def fill_random(start: datetime, end: datetime, max_per_day: int):
    """
    随机模式：每天随机 0~max_per_day 次，模拟真实贡献
    """
    total = 0
    for day in date_range(start, end):
        count = random.randint(0, max_per_day)
        for i in range(count):
            make_commit(day.replace(hour=random.randint(8, 22), minute=random.randint(0, 59)), total)
            total += 1
    print(f"\n🎉 随机模式共创建 {total} 个 commits")


def fill_art(pattern_matrix: list, base_date: datetime, intensity: int):
    """
    像素画模式：传入 7×N 的 0/1 矩阵，1 代表要填充的格子
    base_date 应为某个星期日
    """
    total = 0
    for col_idx, col in enumerate(pattern_matrix):
        for row_idx, cell in enumerate(col):
            if cell:
                day = base_date + timedelta(weeks=col_idx, days=row_idx)
                for i in range(intensity):
                    make_commit(day.replace(hour=9 + i, minute=random.randint(0, 59)), total)
                    total += 1
    print(f"\n🎉 像素画模式共创建 {total} 个 commits")


def push():
    """推送到远程"""
    print("\n📤 正在推送到 GitHub...")
    run("git push origin main")
    print("✅ 推送完成！稍等几分钟刷新 GitHub 主页查看绿墙")


def main():
    parser = argparse.ArgumentParser(description="GitHub 绿墙刷贡献工具")
    parser.add_argument("--start", help="开始日期 (YYYY-MM-DD)", default=None)
    parser.add_argument("--end", help="结束日期 (YYYY-MM-DD)", default=None)
    parser.add_argument("--today", action="store_true", help="仅填充今天")
    parser.add_argument("--intensity", type=int, default=3, help="每天提交次数 (1-10)，越多颜色越深")
    parser.add_argument("--pattern", choices=["fill", "random", "art"], default="fill",
                        help="模式: fill=均匀填充, random=随机, art=像素画")
    parser.add_argument("--skip-weekends", action="store_true", help="跳过周末")
    parser.add_argument("--no-push", action="store_true", help="只提交不推送")
    args = parser.parse_args()

    # 初始化文件
    if not os.path.exists(COMMIT_FILE):
        with open(COMMIT_FILE, "w") as f:
            f.write("# GitHub Green Wall contributions\n")
        run(f"git add {COMMIT_FILE}")
        run(f'git commit -m "init: create contribution file"')

    if args.today:
        start = end = datetime.now().replace(hour=9, minute=0, second=0)
        fill_range(start, end, args.intensity, False)
    elif args.start and args.end:
        start = datetime.strptime(args.start, "%Y-%m-%d")
        end = datetime.strptime(args.end, "%Y-%m-%d")
        if args.pattern == "fill":
            fill_range(start, end, args.intensity, args.skip_weekends)
        elif args.pattern == "random":
            fill_random(start, end, args.intensity)
        elif args.pattern == "art":
            # 示例：写出 "HI" 像素字
            hi_pattern = [
                [1,0,1,0,1,1,1],  # H
                [1,1,1,0,1,0,0],
                [1,0,1,0,1,1,1],
                [0,0,0,0,0,0,0],  # 间隔
                [0,1,1,0,0,1,0],  # I
                [0,0,1,0,0,1,0],
                [0,1,1,0,0,1,0],
            ]
            # 找到最近的周日作为起始
            while start.weekday() != 6:
                start += timedelta(days=1)
            fill_art(hi_pattern, start, args.intensity)
    else:
        parser.print_help()
        return

    if not args.no_push:
        push()


if __name__ == "__main__":
    main()
