# 🟢 GitHub Green Wall 刷贡献工具

自动填充 GitHub Contribution 贡献图，让你的绿墙更丰富！

## 功能

- 🎯 **指定日期范围**填充（回填历史贡献）
- 🎲 **随机模式**模拟真实开发习惯  
- 🎨 **像素画模式**在绿墙上画字/图案
- ⏰ **定时调度器**每天自动提交
- 🤖 **GitHub Actions**无需本地运行，全自动

## 快速开始

### 方法一：GitHub Actions（推荐，全自动）

1. Fork 或 clone 此仓库
2. 进入 **Actions** 页面，启用 Workflows
3. 每天 UTC 10:00 会自动提交 4 次
4. 也可以手动触发，自定义 intensity

### 方法二：本地脚本

```bash
# 克隆仓库
git clone https://github.com/ZSFan888/github-green-wall.git
cd github-green-wall

# 修改 green_wall.py 中的邮箱
# AUTHOR_EMAIL = "your@email.com"

# 填充过去一年
python green_wall.py --start 2025-01-01 --end 2025-12-31 --intensity 3

# 只填今天（深绿）
python green_wall.py --today --intensity 8

# 随机模式（更真实）
python green_wall.py --start 2025-01-01 --end 2025-12-31 --pattern random --intensity 5

# 跳过周末
python green_wall.py --start 2025-01-01 --end 2025-12-31 --skip-weekends
```

## 颜色深度对照

| intensity | 颜色深度 |
|-----------|----------|
| 1 | 浅绿 🟩 |
| 3-4 | 中绿 |
| 6-8 | 深绿 |
| 10+ | 最深绿 |

## ⚠️ 注意事项

- 本地运行时需确保 git 邮箱与 GitHub 账号绑定邮箱一致
- 历史提交使用 `GIT_AUTHOR_DATE` 覆盖时间，需要 `git push --force`（首次）
- 建议使用独立仓库，避免影响正式项目
