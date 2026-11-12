# 免费栈部署包 — 10 个工具分工（2026-11-12 核实）

结论：没有一个能当 24/7 常驻服务器，拼起来才能用。

## 架构

```
Sakupa 静态站 / Workers 轻量 API
        ↓
OpenRouter 免费模型（20/min，50/day）
        ↓
Supabase（Postgres 500MB + Auth） + R2（文件 10GB）
        ↑
Kaggle T4 x2（30h/周，后台 Commit）— 训练 / 批量跑模型
        ↑
GitHub Actions（~2000 分钟/月）— 定时同步、备份、保活
Simular Box（云 Linux 桌面）— AI 代操作浏览器 / 命令
Cloady（已有 xray）— 别动，已占满 0.5核/1GB/5GB
Colab — 只做随手试，不进常驻计划
```

## 分工表

| 工具 | 免费额度 | 硬限制 | 安排的工作 |
|---|---|---|---|
| Kaggle | 每周 30h GPU，T4 x2，单次 12h | 交互闲置 20 分钟断，保存只留 /kaggle/working 20GB | 训练 / 批量跑模型主力，后台 Commit + 定时 |
| Google Colab | 永久免费，官方不公布小时数 | 单次 12h，关浏览器就停，不能后台/定时，无免费 A100 | 随手试、交互调试 |
| Simular Box | Box $0，模型调用耗每日积分 | 会休眠，连续睡 14 天删机，无 GPU，不带 Agent | AI 操作云桌面 |
| Cloady | 永久免费 0.5核/1GB/5GB，出站 10GB/月 | 每人仅 1 个免费工作区 | 已有 xray，别动 |
| Supabase | Postgres 500MB，存储 1GB，带宽 10GB/月 | 最多 2 项目，闲置 1 周暂停，超 500MB 只读 | 主库 + Auth |
| OpenRouter | :free 模型，20/min，50/day | 名单轮换，部署前查实时页，勿硬编码 | 低频模型接口 |
| Cloudflare Workers | 10 万请求/天 | 每请求 CPU 10ms，内存 128MB | 轻量 API / 代理 / 定时 |
| Cloudflare R2 | 存储 10GB，A 类 100 万次，B 类 1000 万次，出站免费 | 仅 Standard 存储有免费额度 | 文件 / 图片 / 备份 |
| GitHub Actions | 私有仓约 2000 分钟/月，公开仓不限 | 并发 20，单次工作流最长 35 天 | 定时同步、备份、保活、CI |
| Sakupa | 免费 = 30 天临时预览，最多 3 个站 | 仅静态，无长期免费托管 | 静态站预览 |

## 使用顺序（账号授权后）

1. Supabase：跑 `supabase/schema.sql`，建表 + 拿 URL / anon key / service key
2. R2：建 bucket，拿 S3 兼容 endpoint + key，填 `r2/upload.py` 的占位符
3. OpenRouter：拿 API key，填 `openrouter/client.py`，先查实时免费名单再选模型
4. Workers：`workers/api.js` + `wrangler.toml`，把 key 设为 secret，不要写进代码
5. Kaggle：`kaggle/train_template.py` 拷进 Notebook，选 GPU T4 x2，Save & Run All 后台跑
6. GitHub Actions：把 `github-actions/` 两个 yml 放进仓库 `.github/workflows/`，填仓库 secrets
7. Sakupa：`static/index.html` 先预览，确认后再决定是否付费长期托管
8. Simular Box：`simular-box/mcp.json` 接入 Claude / Codex，作 AI 操作桌面

## 占位符说明

所有文件里的 `<...>` 都是待填项：API key、URL、bucket 名、仓库名。不要把真 key 提交到公开仓库，Workers / Actions 一律用 secret / env。

## 已知坑

- Supabase 1 周不用就暂停：Actions 保活任务每周至少跑一次
- OpenRouter 每天只有 50 次：不要做高频调用，超了等 UTC 午夜重置
- Workers 单次 CPU 只有 10ms：重计算拆到 Kaggle
- Kaggle / Colab 单次都只有 12 小时：都不是服务器
- Simular Box 14 天不用删机，Sakupa 30 天到期下线：别存重要文件
- Cloady 没有第二个免费工作区
