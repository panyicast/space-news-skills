# 检索指引

用于生成航天领域情报简报，重点关注 AI 在航天领域的发展。

## 核心原则

- 先扩搜索面，再做筛选，不要一开始就把范围收得过窄。
- 默认进行多源检索，不依赖单一搜索接口、单一媒体或单一站点。
- 搜索逻辑应持续吸收前序检索中发现的高价值关键词、机构、任务名、模型名、仓库名、会议名和新来源。
- 任何时候都不要主动降低搜索范围。可以调整权重，但不要静默删除已有主题簇、关键词族或来源族。

## 默认检索顺序

先找高权威来源，再补充媒体、开源社区与社交/视频线索：

1. 官方机构与官方页面
2. 高校、实验室、论文、会议页面
3. GitHub 与项目主页
4. 高质量航天媒体与主流媒体
5. 官方社交账号、官方视频频道、二级转载页面（仅作补充与交叉验证）

## 建议来源类型

### 官方与机构
- NASA
- ESA
- JAXA
- ISRO
- CNSA 及相关公开页面
- 商业航天公司官网、新闻稿、博客
- 各类任务官网、项目页、实验室页面、大学新闻页

### 高校与科研
- 高校新闻页、实验室页面
- arXiv
- 会议官网
- 期刊或技术报告页面
- 研究团队项目主页、论文代码页

### 开源与项目
- GitHub 仓库
- 官方项目文档站点
- 发布说明、release notes、路线图页面
- 模型页、数据集页、开源基准页

### 媒体
- SpaceNews
- Spaceflight Now
- Space.com
- Reuters
- AP
- 其他可信航天媒体与科技媒体

### 社交与视频补充源
- X 上的机构账号、公司账号、研究人员与记者账号
- YouTube 上的官方发布会、媒体简报、任务讲解、技术演示
- 仅作为发现线索或补充上下文，最终应尽量回到原始来源确认

## 搜索范围扩张规则

### 1. 时间切片

如果时间范围超过一周，默认不要只跑一次泛搜索。

建议做法：
- 月报：按上旬 / 中旬 / 下旬，或按周切片检索
- 多月专题：按月切片，再按主题补检
- 避免后期热点淹没前期有效信息

### 2. 主题分簇

不要只用一个“大而泛”的 query。默认按子方向拆分检索，例如：

- 遥感基础模型
- SAR 智能处理
- 轨道动力学
- 交会对接与轨迹优化
- 小推力变轨
- 月球探测
- 深空探测
- 在轨自主与任务规划
- 空间安全 / SSA / STM
- 空间数据网络 / 轨道数据中心 / 空间计算
- 开源项目与工具生态

### 3. 来源分族

同一主题应尽量跨来源族交叉检索：
- 官方机构
- 行业媒体
- 论文与预印本
- GitHub 与项目页
- X / YouTube 补充线索

### 4. 结果驱动扩词

每次检索完成后，如果发现以下内容反复出现且信号较强，应加入后续默认检索逻辑：
- 任务名
- 计划名
- 模型名
- 数据集名
- 仓库名
- 会议名
- 机构名
- 公司名
- 研究团队名

### 5. 结果驱动扩源

如果某个新站点、新频道或新来源反复产出高价值内容，应加入默认来源池，例如：
- 新的实验室项目页
- 新的开源组织仓库
- 新的会议官网
- 新的行业媒体栏目
- 新的官方视频频道

## 推荐检索维度

围绕下面几类关键词组合检索：

### 航天 AI 总体
- 航天 AI / AI for space / space AI
- satellite AI
- onboard AI
- mission operations AI
- space autonomy
- on-orbit autonomy
- space robotics

### 遥感与对地观测
- remote sensing AI
- Earth observation foundation model
- remote sensing foundation model
- SAR AI
- SAR foundation model
- Earth observation vision language model
- cross-view geo-localization satellite
- satellite stereo pipeline learning

### 轨道动力学与任务设计
- orbital dynamics AI
- space rendezvous trajectory optimization
- autonomous rendezvous docking
- mission design via transformers
- guidance navigation control AI

### 小推力变轨与深空自主
- low-thrust orbit transfer AI
- reinforcement learning spacecraft
- deep space probe autonomy
- Mars powered descent guidance learning
- interplanetary transfer deep networks

### 月球探测与在轨自主
- lunar exploration AI
- moon robotics spacecraft autonomy
- lunar rover autonomy
- on-orbit autonomy mission planning

### 空间安全与数据网络
- space situational awareness AI
- SSA AI
- STM intelligence
- space data center
- orbital data center
- LEO data network
- space edge computing

### 开源与项目生态
- space GitHub
- remote sensing GitHub
- satellite imagery deep learning GitHub
- mission analysis GitHub
- orbit optimization GitHub

检索时要主动覆盖下列场景，不要只盯科研或机构新闻：

- 军事与国防航天：太空态势感知、导引控制、侦察监视、军用卫星、空间安全
- 商业航天：初创公司、融资、产品发布、合同合作、商业遥感与卫星服务
- 民用与公共服务：气象、灾害监测、导航、通信、城市与农业遥感应用
- 科研与学术：论文、实验室成果、会议、技术验证、开源工具
- 国际机构与国家项目：NASA、ESA、JAXA、ISRO、CNSA 等机构及国家级计划

## 去重与筛选

- 同一事件优先保留原始来源。
- 二次转载如果没有新增信息，通常不单独入选。
- 与航天关系弱、只有“AI”但没有空间应用场景的内容剔除。
- 只保留在当前时间范围内公开发布、更新、发稿或具有明确时间锚点的内容。
- 一篇论文、一个项目、一个仓库、一次正式发布，原则上只保留一条主事件。
- 搜索接口如 Tavily、Brave 仅作发现工具，不作为唯一来源依据。

## 写作提醒

- 最终不是搜索结果清单，而是情报简报。
- 要先判断重要性，再写中文介绍。
- 如果候选很多，宁可少而精，也不要把低信号内容硬塞满。
- 对最终入选条目，尽量回读原始来源，再写 `内容摘要`。
- 对官方机构、高价值论文、核心仓库和重大任务，优先使用原始页面而不是二手摘要。
