# SecurityNews

本项目的目标是从指定的数据源收集最新安全研究与新闻更新，并自动生成汇总报告。

## 🚀 功能模块

1.  **[secnews](#secnews)**: 自动化安全资讯周报。从 BleepingComputer 和 ArXiv 抓取资讯，通过 LLM 总结并生成 PDF/HTML 报告。
2.  **[top-conf](#top-conf)**: 安全顶会论文全览。针对 USENIX Security, NDSS 等顶会进行深度抓取与分类分析，生成美观的科研报告。

---

## 🔒 secnews
每周自动从 RSS 抓取最新论文与安全新闻，经由 LLM 总结后保存至本地 JSONL 文件，并生成带排版的周报。

### 调用方法
```bash
# 1. 抓取新闻 (source: bleepingcomputer, arxiv_cs_cr, arxiv_cs_ai)
uv run python -m secnews.update bleepingcomputer

# 2. 生成报纸 JSON (总结文章)
uv run python -m secnews.generate_newspaper

# 3. 生成 PDF/HTML 报告 (保存在 secnews/data/report/)
uv run python -m secnews.generate_pdf
```

### 数据来源
- **BleepingComputer**: [RSS Feed](https://www.bleepingcomputer.com/feed/)
- **ArXiv CS.CR**: [Atom Feed](https://rss.arxiv.org/atom/cs.cr)
- **ArXiv CS.AI**: [Atom Feed](https://rss.arxiv.org/atom/cs.ai)

---

## 🎓 top-conf
针对近几年四大安全顶会的论文进行结构化抓取。通过 LLM 为每篇论文生成深度摘要，并根据研究方向自动分类。

### 调用方法（以 USENIX 2025 为例）
```bash
# 1. 网页抓取论文列表
uv run python top-conf/fetch_big4.py usenix 2025

# 2. 调用 LLM 生成总结与分类 (支持断点续传)
uv run python top-conf/generate_conf_summary.py usenix 2025

# 3. 生成美观的 Web/PDF 报告 (保存在 top-conf/data/report/)
uv run python top-conf/generate_conf_report.py usenix 2025
```

### 报告展示
- **USENIX Security 2025**: [[HTML]](top-conf/data/report/USENIX_2025_Report.html) [[PDF]](top-conf/data/report/USENIX_2025_Report.pdf) — 采用精美的 Card-Style 布局。

---

## 🛠️ GitHub Actions
本项目通过流水线实现了全自动化流程：
- **update / gen_newspaper**: 每日定时更新数据库并进行总结。
- **weekly_release**: 每周六自动生成周报并发布至 [GitHub Releases](https://github.com/fripSide/SecurityNews/releases)。
- **Top Conferences Release**: 手动触发，生成指定会议的完整分析报告。