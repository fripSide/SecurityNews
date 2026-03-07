# SecurityNews

本项目的目标是从指定的数据源收集最新安全研究与新闻更新，并自动生成汇总报告。

## secnews  
每周自动更新最新论文与安全新闻，保存至本地 JSONL 文件中。  

**调用方法**：
```bash
# source: bleepingcomputer, arxiv cs.cr, arxiv cs.ai
python -m secnews.update <source>
```

**数据来源**：
- bleepingcomputer: [RSS](https://www.bleepingcomputer.com/feed/)
- arxiv cs.cr: [RSS](https://rss.arxiv.org/atom/cs.cr)
- arxiv cs.ai: [RSS](https://rss.arxiv.org/atom/cs.ai)

## top-conf
手动更新近几年四大安全顶会的论文。  
自动生成每年的论文摘要简介与分类报告。

**调用方法（以 USENIX 2025 为例）**：
```bash
uv run python top-conf/fetch_big4.py usenix 2025
uv run python top-conf/generate_conf_newspaper.py usenix 2025
uv run python top-conf/generate_conf_pdf.py usenix 2025
```

**生成的报告样例**：
- USENIX Security 2025 论文全览 [[HTML]](top-conf/data/report/USENIX_2025_Report.html) [[PDF]](top-conf/data/report/USENIX_2025_Report.pdf)

TODO:
1. 数据分析，生成感兴趣方向的论文列表以及摘要简介。