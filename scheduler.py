#!/usr/bin/env python3
"""
定时刷绿墙调度器 - 每天自动提交一次
运行: python scheduler.py
后台运行: nohup python scheduler.py &
"""
import time
import subprocess
from datetime import datetime
import random

COMMIT_FILE = "contributions.txt"
AUTHOR_NAME = "ZSFan888"
AUTHOR_EMAIL = "your@email.com"
COMMITS_PER_DAY = 4  # 每天提交次数（控制绿色深度）


def daily_commit():
    import os
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(COMMIT_FILE, "a") as f:
        f.write(f"{date_str} - scheduled commit\n")

    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL

    subprocess.run("git add contributions.txt", shell=True, env=env)
    subprocess.run(f'git commit -m "scheduled: {date_str}"', shell=True, env=env)
    subprocess.run("git push origin main", shell=True, env=env)
    print(f"[{date_str}] ✅ Daily commit pushed")


if __name__ == "__main__":
    print("🟢 GitHub 绿墙调度器已启动，每天自动提交...")
    last_day = None
    while True:
        today = datetime.now().date()
        if today != last_day:
            # 随机延迟 0~2小时，模拟真实行为
            delay = random.randint(0, 7200)
            time.sleep(delay)
            for _ in range(COMMITS_PER_DAY):
                daily_commit()
                time.sleep(random.randint(60, 600))
            last_day = today
        time.sleep(300)  # 每5分钟检查一次
