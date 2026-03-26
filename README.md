# Space News Skills

这是一套围绕 `space-news` 工作流整理出来的技能仓库，当前主要包含三个技能：

- `space-news`
- `wechat-space-news-draft`
- `github-deep-research`（已按当前环境做过适配）

仓库目标不是单独保存几个 `SKILL.md` 文件，而是把一整套可维护的航天情报生产链路沉淀下来，包括：
- 搜索原则
- 来源边界
- 输出模板
- 协同工具规则
- 自动化脚本
- 微信公众号草稿上传能力

## 目录结构

### `space-news`
用于生成中文航天情报简报，重点关注：
- 航天 AI
- 遥感基础模型
- SAR 智能处理
- 月球探测
- 深空探测
- 在轨自主
- 空间安全
- 空间数据网络
- 开源项目与工具生态

包含内容：
- `SKILL.md`：主规则文件
- `references/`：检索、模板、分类、协同流程等说明
- `scripts/`：候选收集、合并、改写、补全、排序、成稿脚本
- `examples/`：示例输出

### `wechat-space-news-draft`
用于把整理好的航天月报 / 周报上传为微信公众号草稿。

包含内容：
- `SKILL.md`：上传流程说明
- `scripts/`：草稿上传脚本

## 当前搜索与分析原则

### 1. 默认多源检索
`space-news` 不依赖单一来源。默认要求覆盖：
- 官方机构站点
- 行业媒体
- 论文与预印本
- GitHub / 项目页
- 必要时的 X / YouTube 补充线索

### 2. Tavily 优先，Brave 可选
在当前环境下：
- `Tavily` 作为默认发现层
- `Brave` 作为可选补充搜索源
- 两者都不能作为唯一信息来源

### 3. GitHub 深挖作为辅助层
已引入 `github-deep-research` 作为辅助分析工具之一，用于：
- 仓库活跃度分析
- Issue / PR / commit / release 节奏补充
- 开源项目演化与维护状态判断
- 竞品关系补充

但它不能替代：
- 官方源
- 仓库原始页面
- release / docs / 论文页
- 多源交叉验证

### 4. 搜索逻辑持续扩张
该工作流采用“只扩不缩”的维护原则：
- 每次搜索发现新的高价值关键词，加入默认查询族
- 每次发现新的高价值来源，加入默认来源池
- 不主动缩小搜索范围

## 协同工具关系

当前推荐协同链路：

- `space-news`：主工作流与成稿层
- `Tavily`：发现层
- `web_fetch`：正文回读层
- `browser`：复杂页面补抓层
- `gh`：GitHub 原生证据层
- `github-deep-research`：开源项目深挖层
- `wechat-space-news-draft`：公众号草稿输出层

更详细的协同规则见：
- `space-news/references/tool-orchestration.md`

## 关键参考文件

### `space-news/references/output-template.md`
固定输出格式模板。

### `space-news/references/search-playbook.md`
检索原则、关键词族、来源扩张规则。

### `space-news/references/tool-orchestration.md`
工具协同规则，说明 `space-news`、Tavily、`github-deep-research`、`gh`、`web_fetch`、`browser` 如何配合。

### `space-news/references/no-api-workflow.md`
在没有某些搜索 API 时的替代工作流。

## 脱敏与安全原则

本仓库不会提交以下内容：
- API keys
- tokens
- appid / secret
- 本地缓存与中间产物
- `__pycache__`
- 临时候选 JSON、临时输出草稿、私有配置

脚本只保留：
- 通用逻辑
- 环境变量入口
- 命令行参数入口

## 维护约定

当前维护方式：
- 本地修改 skill
- 本地检查是否有敏感信息
- 同步到本仓库
- 提交并推送到 GitHub

如果后续继续演进，建议保持：
- 规则层更新写进 `SKILL.md`
- 执行层更新写进 `references/`
- 自动化能力更新写进 `scripts/`
- 对外发布继续遵循脱敏原则

## 仓库定位

这个仓库的定位不是“通用搜索技能合集”，而是：

**一套面向航天情报生产的、可持续优化的技能工作流仓库。**

重点不在某一个搜索接口，而在：
- 多源检索
- 原始来源回读
- 开源项目深挖
- 固定格式成稿
- 规则持续沉淀与扩张
