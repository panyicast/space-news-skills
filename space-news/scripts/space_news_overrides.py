#!/usr/bin/env python3
"""High-priority overrides for known space-news titles.

Maintenance notes:
- Only add overrides for items that repeatedly regress into template-like summaries.
- Prefer high-value original sources or frequently recurring media patterns.
- Each override should be source-grounded and manually checked at least once.
- If a recurring pattern can be handled generically in extraction logic, prefer moving it out of overrides later.
- Keep titles exact to avoid unintended matches.
"""

from __future__ import annotations

# Pure-English titles that should render as `English Title（中文标题）`.
TITLE_TRANSLATIONS = {
    "CrossEarth-SAR: A physically grounded sparse MoE foundation model for SAR remote sensing": "面向 SAR 遥感的物理先验稀疏混合专家基础模型",
    "THOR: Compute-adaptive Earth observation foundation model across Sentinel data": "面向 Sentinel 数据的算力自适应对地观测基础模型",
    "AegisSat: resilient and secure AI satellite platform architecture": "具备韧性与安全性的 AI 卫星平台架构",
    "3 Ways Students Can Get Involved With Artemis": "学生参与阿耳忒弥斯计划的三种方式",
    "OrbitsIQ Global Announces Breakthrough in Space-Based IoT Connectivity": "OrbitsIQ 发布空间物联网连接技术突破",
    "Smile fuelled for launch": "Smile 任务完成发射前推进剂加注",
    "Launch Preview: Russia to debut Soyuz-5; Falcon 9 and Atlas V to launch internet satellites": "发射前瞻：俄将首飞 Soyuz-5，Falcon 9 与 Atlas V 将执行互联网卫星发射",
    "Celeste: Countdown to Launch 1": "Celeste 首次发射倒计时",
    "Progress MS-33 set to resume Russian flights to ISS from repaired pad": "Progress MS-33 将从修复后的发射台恢复俄方向国际空间站飞行",
    "NASA Exploration, Science Inspire “Project Hail Mary” Film": "NASA 探索与科学任务启发《挽救计划》电影创作",
    "Restless Kīlauea Launches Lava and Ash": "持续活跃的基拉韦厄火山喷发熔岩与火山灰",
    "NASA Laser Reflecting Instrument Makes GPS Satellite More Accurate": "NASA 激光反射仪提升 GPS 卫星测量精度",
    "NASA’s Roman Observatory Passes Final Major Prelaunch Tests": "NASA 罗曼太空望远镜通过发射前最后重大测试",
    "Booster 19 concludes initial test campaign on Pad 2": "Booster 19 在 2 号发射台完成初步测试",
    "NASA to Cover Progress 94 Spacecraft Launch, Space Station Docking": "NASA 将直播 Progress 94 飞船发射与空间站对接",
    "Reminders of Where We’ve Been, Where We’re Going": "我们从哪里来、将往何处去的提醒",
    "Launch Preview: Russia to debut Soyuz-5; Falcon 9 and Atlas V to launch internet satellites": "发射前瞻：俄罗斯将首飞 Soyuz-5，Falcon 9 与 Atlas V 将执行互联网卫星发射",
    "Progress MS-33 set to resume Russian flights to ISS from repaired pad": "Progress MS-33 将从修复后的发射台恢复俄方向国际空间站飞行",
    "NASA Exploration, Science Inspire “Project Hail Mary” Film": "NASA 探索与科学任务启发《挽救计划》电影创作",
    "NASA Exploration, Science Inspire \"Project Hail Mary\" Film": "NASA 探索与科学任务启发《挽救计划》电影创作",
    "NASA Data Hackathon Inspires Community Action": "NASA 数据黑客松激发社区行动",
    "China’s Astronstone raises $29 million for reusable rocket with chopstick-style recovery": "中国 Astronstone 融资 2900 万美元推进筷子式回收火箭",
    "China's Astronstone raises $29 million for reusable rocket with chopstick-style recovery": "中国 Astronstone 融资 2900 万美元推进筷子式回收火箭",
    "US-Based Katalyst Selects Ariane 6 to Launch Satellite Servicing Spacecraft": "美国 Katalyst 选择 Ariane 6 发射在轨服务航天器",
    "Artemis 2 returns to the pad for April launch attempt": "Artemis 2 为 4 月发射尝试重新返回发射台",
    "Rocket Lab launches eighth Synspective radar imaging satellite": "Rocket Lab 发射 Synspective 第八颗雷达成像卫星",
    "Another GPS launch shifts from ULA to SpaceX as Vulcan investigation continues": "在 Vulcan 调查持续期间，又一项 GPS 发射从 ULA 转交 SpaceX",
    "SES targets 28 satellites with K2 Space for next-gen MEO network": "SES 拟与 K2 Space 部署 28 颗卫星建设下一代中轨网络",
    "SLS enters pad flow ahead of historic Artemis II mission": "SLS 在历史性 Artemis II 任务前进入发射台流程",
    "Moog taps Redwire to provide solar arrays for Meteor": "Moog 选择 Redwire 为 Meteor 平台提供太阳能阵列",
    "Live coverage: SpaceX to launch 29 Starlink satellites on Falcon 9 rocket from Cape Canaveral": "直播：SpaceX 将从卡纳维拉尔角用 Falcon 9 发射 29 颗 Starlink 卫星",
    "Live coverage: SpaceX to launch 25 Starlink satellites on Falcon 9 rocket from Vandenberg SFB": "直播：SpaceX 将从范登堡用 Falcon 9 发射 25 颗 Starlink 卫星",
    "SpaceX launches 25 Starlink satellites on Falcon 9 rocket from Vandenberg SFB": "SpaceX 从范登堡用 Falcon 9 发射 25 颗 Starlink 卫星",
}

# NASA original-source items: prefer concrete, source-grounded summaries.
NASA_SUMMARY_OVERRIDES = {
    "3 Ways Students Can Get Involved With Artemis": "这篇 NASA 文章不是在发布新的技术成果，而是在 Artemis 计划框架下介绍学生参与月球探索相关工作的三类主要路径。第一类是 NASA 实习项目，面向美国大学生开放，参与内容包括支持月球探索、航天器系统和深空技术开发等真实任务，从中积累工程实践、职业连接和进入航天行业所需的准备。第二类是学生设计挑战，NASA 重点列举了 Human Exploration Rover Challenge、NASA SUITS 和 Student Launch 三项活动，分别对应月面车辆、人机界面与航天服交互、高功率火箭与有效载荷设计等方向，强调通过竞赛形式培养工程设计、问题求解和系统集成能力。第三类是与 Minecraft Education 的合作项目，学生可以在 Mission Control: Artemis 等内容中模拟任务控制、月面活动和空间探索流程，以更低门槛方式接触 Artemis 任务概念。整体来看，这篇文章的核心价值不在于披露项目节点，而在于反映 NASA 正把 Artemis 作为航天人才培养和 STEM 动员的长期平台，通过实习、竞赛和数字教育内容为未来月球探索计划储备后备人才。",
    "NASA PC-12 Aircraft Makes Move to Support Flight Research Across Agency": "NASA 公布的信息显示，一架编号为 606 的 Pilatus PC-12 飞机已转移至位于加州爱德华兹的阿姆斯特朗飞行研究中心，后续将在那里作为跨机构飞行研究平台继续使用。这架飞机由格伦研究中心于 2022 年购入，原本用于先进技术开发，今后将在继续支持格伦研究任务的同时，为 NASA 其他中心、产业界和学术界的飞行研究提供能力支撑。文章特别提到，该机此前已参与与国际空间站相关的通信中继实验，通过便携式激光终端、地面网络和卫星链路传输 4K 视频，并验证了在云层条件下的通信能力；它也被用于研究未来城市空中出租车所需的监视系统。NASA 同时介绍，另一架来自格伦的 T-34 也已抵达阿姆斯特朗，用于评估其作为飞行研究和飞行员训练平台的潜力。整体来看，这条信息的重点不是单次调机，而是 NASA 正在把现有机队资源重新整合到更灵活的跨中心飞行试验体系中，以支撑低成本、快速迭代的航空航天技术验证。",
    "Reminders of Where We’ve Been, Where We’re Going": "这条 NASA 页面本质上是一则配图说明，核心内容是展示 2026 年 3 月 24 日活动现场陈列的三块月球岩石，并借此串联美国载人登月计划从阿波罗时代到阿耳忒弥斯时代的延续性。页面同时提到，NASA 管理层在活动中更新了当前任务重点，包括在 50 多年后再次把宇航员送上月面、建设永久性月球基地的初始要素，以及推进核推进等未来深空任务能力。换句话说，这条信息本身并不是一个独立的新项目公告，而更像是 NASA 用象征性展示物和现场表述对当前月球探索路线做的一次公开叙事包装。它的参考价值主要在于帮助观察 NASA 在对外传播中如何把阿波罗遗产、阿耳忒弥斯登月和更长期的深空探索目标放在同一战略框架下表述。",
}

# ESA original-source items with repeated extraction instability.
ESA_SUMMARY_OVERRIDES = {
    "ESA 宣布新 AI Hub 以推动 space-enabled connectivity": "ESA 公布的信息显示，一个由英国航天局支持的新 AI Hub 正在英国建设，定位是为欧洲产业界提供一个测试、验证和规模化 AI 驱动卫星通信与融合通信技术的专用环境。根据页面内容，该平台的重点方向包括频谱优化、面向机器人和无人机的智能自主平台、多轨道认知网络、网络安全，以及 6G、直连终端通信、预测性系统、数字孪生和优化数据传输等能力。ESA 同时强调，企业将能够使用该中心的演示空间、应用开发测试实验室以及私有卫星通信网络等设施。文章还提到，这一项目是在巴塞罗那世界移动通信大会期间由 ESA 与英国航天局共同宣布的，并被放入欧洲未来融合通信网络能力建设的大背景中来看。整体而言，这不是单纯的概念性倡议，而是在尝试把 AI 在空间通信中的应用推进到可验证、可展示和可产业化的基础设施层面。",
}

# Media-origin items that need anti-template, concrete summaries.
MEDIA_SUMMARY_OVERRIDES = {
    "OrbitsIQ Global Announces Breakthrough in Space-Based IoT Connectivity": "SpaceNews 刊载的公司稿件显示，OrbitsIQ Global 宣布其在与弗罗茨瓦夫科技大学合作、并获 ESA 支持的项目中取得一项面向空间物联网通信的技术突破。文中提到，这项名为 E-SSA 的方案面向空间物联网和移动遥测应用，目标是在不显著增加卫星载荷复杂度的情况下，提高窄带卫星网络在高设备密度场景下的可扩展性。按照页面说法，该方案可支持数百台设备在同一射频信道上同时传输，并避免传统调度式或碰撞式接入在高密度条件下出现的容量下降问题；设备还能在无需预注册、同步或复杂网络协调的前提下向过境卫星发送数据。公司还强调，该架构有助于降低协议开销、提高电池供电终端的能效，并与其 AI 驱动网络编排、安全通信和星地融合连接战略形成协同。整体来看，这条信息更像一则带有宣传色彩的商业技术发布，但其中关于高并发窄带星载物联网接入、星地网络协同和低复杂度终端接入的描述，仍值得作为后续跟踪新型卫星 IoT 体系架构的线索。",
    "Moog taps Redwire to provide solar arrays for Meteor": "SpaceNews 报道称，Redwire 获得来自 Moog 的首份 ELSA 太阳能阵列合同，金额为 1280 万美元，相关产品将用于 Moog 为一名未披露国家安全客户提供的 Meteor 卫星平台。根据报道，Redwire 将为 Meteor ESPA-Grande 卫星母平台提供 Extensible Low-Profile Solar Array（ELSA）翼板，并负责设计、制造、测试和交付。Redwire 将 ELSA 描述为一款面向批量化卫星生产的低轮廓太阳能阵列产品，按体积计算可比传统太阳能阵列提供更高功率输出；Moog 则表示，该组件将作为 Meteor 卫星平台的标准化部件之一，以增强其平台的模块化和任务适配能力。整体来看，这条消息的重要性不在于单一部件采购，而在于它反映出国防或国家安全航天平台正在更明确地采用标准化、可批产的卫星子系统配置，以提高交付效率和星座部署能力。",
}

NASA_IMPACT_OVERRIDES = {
    "3 Ways Students Can Get Involved With Artemis": "这类内容主要体现 NASA 围绕 Artemis 建设长期人才供给体系的思路，值得关注其后续是否继续扩大实习名额、挑战赛规模和教育合作范围，从而把月球探索计划进一步转化为机构级人才培养管线。",
    "NASA PC-12 Aircraft Makes Move to Support Flight Research Across Agency": "值得关注 NASA 是否继续把这类试验飞机用于通信、空域管理和低成本飞行验证任务，因为这反映其在跨中心试验资源整合和快速技术验证方面的能力建设方向。",
    "Reminders of Where We’ve Been, Where We’re Going": "这类内容更适合作为机构战略叙事信号观察，而不是具体项目进展；值得关注 NASA 后续是否把这些表述进一步落实为明确的任务节点、预算安排和工程计划。",
}

ESA_IMPACT_OVERRIDES = {
    "ESA 宣布新 AI Hub 以推动 space-enabled connectivity": "值得关注该中心后续是否形成明确试验项目、企业合作与技术验证成果，这将决定它是展示平台还是欧洲空间通信 AI 能力建设的实际枢纽。",
}

MEDIA_IMPACT_OVERRIDES = {
    "OrbitsIQ Global Announces Breakthrough in Space-Based IoT Connectivity": "值得关注其后续是否披露更具体的测试数据、载荷实现方式和商业落地计划，以判断这是否是真正可扩展的卫星 IoT 架构突破，还是偏市场叙事的技术宣传。",
    "Moog taps Redwire to provide solar arrays for Meteor": "值得关注 Meteor 平台后续面向国家安全客户的批量部署情况，以及 ELSA 这类标准化功率子系统是否会进一步进入更广泛的国防航天和双用途卫星供应链。",
}

SUMMARY_OVERRIDES = {
    **NASA_SUMMARY_OVERRIDES,
    **ESA_SUMMARY_OVERRIDES,
    **MEDIA_SUMMARY_OVERRIDES,
}

IMPACT_OVERRIDES = {
    **NASA_IMPACT_OVERRIDES,
    **ESA_IMPACT_OVERRIDES,
    **MEDIA_IMPACT_OVERRIDES,
}
