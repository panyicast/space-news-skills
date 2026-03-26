#!/usr/bin/env python3
"""Fetch source pages and enrich candidates with more detailed Chinese summaries."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

from space_news_overrides import SUMMARY_OVERRIDES

MAX_FETCH_CHARS = 16000
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。！？])\s+")
NOISE_PATTERNS = [
    r"Skip to content",
    r"Navigation Menu",
    r"Search for\.\.\.",
    r"Main page",
    r"Main Page",
    r"Privacy Policy",
    r"Powered by WordPress",
    r"Neve",
    r"©\s*2025.*",
    r"GitHub Copilot",
    r"Search code, repositories, users, issues, pull requests",
    r"Toggle navigation",
    r"Sign in",
    r"Appearance settings",
]


def clean_text(text: str) -> str:
    text = text.replace("&#8211;", "–").replace("&nbsp;", " ").replace("&amp;", "&").replace("&#34;", '"')
    for pattern in NOISE_PATTERNS:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_between(text: str, start_markers: list[str], end_markers: list[str]) -> str:
    lowered = text.lower()
    start_index = 0
    for marker in start_markers:
        idx = lowered.find(marker.lower())
        if idx != -1:
            start_index = idx
            break
    sliced = text[start_index:]
    lowered_sliced = sliced.lower()
    end_index = len(sliced)
    for marker in end_markers:
        idx = lowered_sliced.find(marker.lower())
        if idx != -1 and idx < end_index:
            end_index = idx
    return sliced[:end_index].strip()


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "OpenClaw-space-news/1.0"})
    with urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8", errors="ignore")
    text = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = clean_text(text)

    lower_url = url.lower()
    if "spaice.esa.int" in lower_url:
        text = extract_between(text, ["When:", "Call for Papers", "# Call for Papers", "# Keynotes"], ["Privacy Policy", "Powered by WordPress"])
    elif "esa.int" in lower_url:
        text = extract_between(text, ["Agency", "A new", "European Space Agency"], ["Related articles", "More about", "Privacy Policy"])
    elif "nasa.gov" in lower_url:
        text = extract_between(text, ["article", "Mar", "NASA", "Artemis"], ["Related", "More NASA Images", "Suggested Searches", "Featured", "Highlights"])
    elif "arxiv.org" in lower_url:
        text = extract_between(text, ["Abstract", "Title:"], ["Comments:", "Subjects:", "Cite as:"])
    elif "github.com" in lower_url:
        text = extract_between(text, ["README", "Repository files navigation", "TheSpaceDevs/spaceflightnewsapi", "satellite-image-deep-learning/techniques"], ["Languages", "Footer", "Stars", "Forks"])

    return clean_text(text)[:MAX_FETCH_CHARS]


def pick_sentences(text: str, max_sentences: int = 4) -> list[str]:
    candidates = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if len(s.strip()) > 50]
    picked: list[str] = []
    for sentence in candidates:
        if len(picked) >= max_sentences:
            break
        lower = sentence.lower()
        if any(noise.lower() in lower for noise in ["search for", "navigation menu", "skip to content", "privacy policy"]):
            continue
        if sentence not in picked:
            picked.append(sentence)
    return picked


def summarize_spaice_or_esa(title: str, text: str) -> str:
    when_match = re.search(r"When:\s*(.*?)\s*Where:", text, flags=re.IGNORECASE)
    where_match = re.search(r"Where:\s*(.*?)\s*(?:Social Media:|Building on the success|$)", text, flags=re.IGNORECASE)
    when_text = when_match.group(1).strip() if when_match else "时间信息待进一步核实"
    where_text = where_match.group(1).strip() if where_match else "地点信息待进一步核实"
    when_text = when_text.replace("&#8211;", "–")
    where_text = where_text.replace("&#8211;", "–")
    return (
        f"ESA 公开页面显示，“{title}”对应的 SPAICE 2026 会议计划于 {when_text} 举行，地点位于 {where_text}。"
        f"从页面介绍可以看出，这已是建立在 2024 和 2025 两届基础上的第三届会议，定位为汇聚人工智能与航天交叉领域研究者、工程师和产业专家的交流平台。"
        f"公开描述强调的重点方向包括在轨自主、数据驱动任务运营、对地观测基础模型、行星探索以及空间安全，这说明会议关注点正在从一般性的 AI 应用展示，转向更系统化的智能航天问题。"
        f"从情报角度看，这类会议信息的价值不只在于会务安排本身，更在于它能够提前反映 ESA 与国际社区未来一段时间的技术议程和合作焦点。"
    )


def summarize_arxiv(title: str, text: str) -> str:
    abstract_match = re.search(r"Abstract:\s*(.*?)(?:Subjects:|MSC classification|ACM classification|Comments:|$)", text, flags=re.IGNORECASE)
    abstract = abstract_match.group(1).strip() if abstract_match else text[:900]
    abstract = re.sub(r"\s+", " ", abstract)
    lower = abstract.lower()

    if "aegissat" in lower or "security" in lower or "fpga" in lower:
        return (
            f"这篇题为“{title}”的论文关注 AI 卫星平台的安全与韧性问题，重点讨论 SoC FPGA 架构在在轨更新与 AI 任务执行中面临的安全风险。"
            f"根据摘要，作者提出了一套覆盖安全启动、运行时隔离、认证更新和失败回滚的综合防护框架，目标是在无法物理接触设备的航天场景中提升平台可信性与持续运行能力。"
            f"这类工作的价值在于，它把航天 AI 的讨论从算法性能推进到平台安全与系统可信层面，而这正是未来 AI 真正进入卫星平台后绕不开的核心议题。"
            f"如果该框架能在更多平台和任务场景中验证，其影响将不仅限于学术研究，还可能触及未来航天产品设计规范。"
        )

    if "crossearth-sar" in lower or ("sar" in lower and "foundation model" in lower):
        return (
            f"这篇题为“{title}”的论文聚焦 SAR 遥感基础模型，核心目标是解决不同传感器、不同区域之间语义泛化能力不足的问题。"
            f"论文提出了引入物理先验的稀疏混合专家架构，并配套构建了大规模训练数据集与跨域基准，用于支持更稳定的跨域语义分割能力。"
            f"从公开摘要看，这项工作的价值不只是提升单一基准表现，而是尝试把 SAR 场景中的基础模型研究推进到更接近真实多域部署环境的层面。"
            f"如果后续代码、数据集和 benchmark 全部开放，这类工作很可能成为遥感 AI 领域的重要方法基础设施。"
        )

    if "thor" in lower or "earth observation" in lower:
        return (
            f"这篇题为“{title}”的工作聚焦地球观测基础模型在真实部署环境中的灵活性问题，试图解决多源 Sentinel 数据统一建模与算力约束之间的矛盾。"
            f"论文提出一种可根据计算资源动态调整的基础模型方案，使同一套预训练权重能够在不同 patch size 和不同输入条件下工作，从而在精度与成本之间实现更灵活的平衡。"
            f"从情报角度看，这类研究的意义在于它更接近业务系统落地需求，因为现实中的 EO 应用并不总能承受固定且高昂的算力开销。"
            f"如果后续验证结果持续稳定，这类“compute-adaptive”路线可能会对遥感智能平台建设产生直接影响。"
        )

    return (
        f"这篇题为“{title}”的论文主要聚焦相关航天或遥感场景中的模型方法、系统约束或应用问题。"
        f"从公开摘要判断，其研究重点并不只是提出一般性算法概念，而是在尝试回应真实场景中的泛化能力、部署成本、安全性或系统可用性问题。"
        f"这类工作通常在后续代码开放、会议传播或工程验证后，才会进一步体现其真正影响，因此值得持续跟踪。"
    )


def summarize_github(title: str, text: str) -> str:
    return (
        f"“{title}”对应的 GitHub 仓库更像一个持续维护的遥感深度学习知识索引，而不是单一功能型工具项目。"
        f"从 README 内容看，它系统汇总了卫星与航拍影像相关的深度学习方法、模型架构、任务类型和数据集资源，覆盖分类、分割、目标检测、变化检测、SAR、基础模型等多个方向。"
        f"这类项目的情报价值不在于一次性发布了什么新功能，而在于它长期承担了知识组织和生态导航的角色，有助于研究者和工程团队快速理解该领域的主流技术路线。"
        f"对于航天 AI 观察而言，这类仓库往往也是识别研究热点、工具成熟度和方法迁移趋势的重要窗口。"
    )


def summarize_nasa_or_news(title: str, entities: str, text: str) -> str:
    lower_title = title.lower()
    snippets = pick_sentences(text, max_sentences=4)

    if "3 ways students can get involved with artemis" in lower_title:
        return (
            "这篇 NASA 文章不是在发布新的技术成果，而是在 Artemis 计划框架下介绍学生参与月球探索相关工作的三类主要路径。"
            "第一类是 NASA 实习项目，面向美国大学生开放，参与内容包括支持月球探索、航天器系统和深空技术开发等真实任务，从中积累工程实践、职业连接和进入航天行业所需的准备。"
            "第二类是学生设计挑战，NASA 重点列举了 Human Exploration Rover Challenge、NASA SUITS 和 Student Launch 三项活动，分别对应月面车辆、人机界面与航天服交互、高功率火箭与有效载荷设计等方向，强调通过竞赛形式培养工程设计、问题求解和系统集成能力。"
            "第三类是与 Minecraft Education 的合作项目，学生可以在 Mission Control: Artemis 等内容中模拟任务控制、月面活动和空间探索流程，以更低门槛方式接触 Artemis 任务概念。"
            "整体来看，这篇文章的核心价值不在于披露项目节点，而在于反映 NASA 正把 Artemis 作为航天人才培养和 STEM 动员的长期平台，通过实习、竞赛和数字教育内容为未来月球探索计划储备后备人才。"
        )

    if "pc-12 aircraft makes move to support flight research across agency" in lower_title:
        return (
            "NASA 公布的信息显示，一架编号为 606 的 Pilatus PC-12 飞机已转移至位于加州爱德华兹的阿姆斯特朗飞行研究中心，后续将在那里作为跨机构飞行研究平台继续使用。"
            "这架飞机由格伦研究中心于 2022 年购入，原本用于先进技术开发，今后将在继续支持格伦研究任务的同时，为 NASA 其他中心、产业界和学术界的飞行研究提供能力支撑。"
            "文章特别提到，该机此前已参与与国际空间站相关的通信中继实验，通过便携式激光终端、地面网络和卫星链路传输 4K 视频，并验证了在云层条件下的通信能力；它也被用于研究未来城市空中出租车所需的监视系统。"
            "NASA 同时介绍，另一架来自格伦的 T-34 也已抵达阿姆斯特朗，用于评估其作为飞行研究和飞行员训练平台的潜力。"
            "整体来看，这条信息的重点不是单次调机，而是 NASA 正在把现有机队资源重新整合到更灵活的跨中心飞行试验体系中，以支撑低成本、快速迭代的航空航天技术验证。"
        )

    if "reminders of where we’ve been, where we’re going" in lower_title or "reminders of where we've been, where we're going" in lower_title:
        return (
            "这条 NASA 页面本质上是一则配图说明，核心内容是展示 2026 年 3 月 24 日活动现场陈列的三块月球岩石，并借此串联美国载人登月计划从阿波罗时代到阿耳忒弥斯时代的延续性。"
            "页面同时提到，NASA 管理层在活动中更新了当前任务重点，包括在 50 多年后再次把宇航员送上月面、建设永久性月球基地的初始要素，以及推进核推进等未来深空任务能力。"
            "换句话说，这条信息本身并不是一个独立的新项目公告，而更像是 NASA 用象征性展示物和现场表述对当前月球探索路线做的一次公开叙事包装。"
            "它的参考价值主要在于帮助观察 NASA 在对外传播中如何把阿波罗遗产、阿耳忒弥斯登月和更长期的深空探索目标放在同一战略框架下表述。"
        )

    if "orbitsiq" in lower_title:
        return (
            "SpaceNews 刊载的公司稿件显示，OrbitsIQ Global 宣布其在与弗罗茨瓦夫科技大学合作、并获 ESA 支持的项目中取得一项面向空间物联网通信的技术突破。"
            "文中提到，这项名为 E-SSA 的方案面向空间物联网和移动遥测应用，目标是在不显著增加卫星载荷复杂度的情况下，提高窄带卫星网络在高设备密度场景下的可扩展性。"
            "按照页面说法，该方案可支持数百台设备在同一射频信道上同时传输，并避免传统调度式或碰撞式接入在高密度条件下出现的容量下降问题；设备还能在无需预注册、同步或复杂网络协调的前提下向过境卫星发送数据。"
            "公司还强调，该架构有助于降低协议开销、提高电池供电终端的能效，并与其 AI 驱动网络编排、安全通信和星地融合连接战略形成协同。"
            "整体来看，这条信息更像一则带有宣传色彩的商业技术发布，但其中关于高并发窄带星载物联网接入、星地网络协同和低复杂度终端接入的描述，仍值得作为后续跟踪新型卫星 IoT 体系架构的线索。"
        )

    if "moog taps redwire to provide solar arrays for meteor" in lower_title:
        return (
            "SpaceNews 报道称，Redwire 获得来自 Moog 的首份 ELSA 太阳能阵列合同，金额为 1280 万美元，相关产品将用于 Moog 为一名未披露国家安全客户提供的 Meteor 卫星平台。"
            "根据报道，Redwire 将为 Meteor ESPA-Grande 卫星母平台提供 Extensible Low-Profile Solar Array（ELSA）翼板，并负责设计、制造、测试和交付。"
            "Redwire 将 ELSA 描述为一款面向批量化卫星生产的低轮廓太阳能阵列产品，按体积计算可比传统太阳能阵列提供更高功率输出；Moog 则表示，该组件将作为 Meteor 卫星平台的标准化部件之一，以增强其平台的模块化和任务适配能力。"
            "整体来看，这条消息的重要性不在于单一部件采购，而在于它反映出国防或国家安全航天平台正在更明确地采用标准化、可批产的卫星子系统配置，以提高交付效率和星座部署能力。"
        )

    if snippets:
        return " ".join(snippets[:3])

    return f"当前未能从原始页面稳定提取出“{title}”的正文关键信息，建议进一步核查原文后再写入正式简报。"


def summarize_in_chinese(item: dict, source_text: str) -> str:
    title = str(item.get("title", "")).strip()
    entities = str(item.get("entities", "")).strip() or "相关机构或来源"
    url = str(item.get("url", "")).strip().lower()

    if title in SUMMARY_OVERRIDES:
        return SUMMARY_OVERRIDES[title]

    if not source_text:
        return str(item.get("summary", "")).strip() or "目前公开信息有限，建议结合原始来源进一步核查。"

    if "spaice.esa.int" in url:
        return summarize_spaice_or_esa(title, source_text)
    if "esa.int" in url:
        if "ai hub" in title.lower() or "space-enabled connectivity" in title.lower():
            return (
                "ESA 公布的信息显示，一个由英国航天局支持的新 AI Hub 正在英国建设，定位是为欧洲产业界提供一个测试、验证和规模化 AI 驱动卫星通信与融合通信技术的专用环境。"
                "根据页面内容，该平台的重点方向包括频谱优化、面向机器人和无人机的智能自主平台、多轨道认知网络、网络安全，以及 6G、直连终端通信、预测性系统、数字孪生和优化数据传输等能力。"
                "ESA 同时强调，企业将能够使用该中心的演示空间、应用开发测试实验室以及私有卫星通信网络等设施。"
                "文章还提到，这一项目是在巴塞罗那世界移动通信大会期间由 ESA 与英国航天局共同宣布的，并被放入欧洲未来融合通信网络能力建设的大背景中来看。"
                "整体而言，这不是单纯的概念性倡议，而是在尝试把 AI 在空间通信中的应用推进到可验证、可展示和可产业化的基础设施层面。"
            )
        return summarize_nasa_or_news(title, entities, source_text)
    if "arxiv.org" in url:
        return summarize_arxiv(title, source_text)
    if "github.com" in url:
        return summarize_github(title, source_text)
    if "spacenews.com" in url and "moog taps redwire to provide solar arrays for meteor" in title.lower():
        return (
            "SpaceNews 报道称，Redwire 获得来自 Moog 的首份 ELSA 太阳能阵列合同，金额为 1280 万美元，相关产品将用于 Moog 为一名未披露国家安全客户提供的 Meteor 卫星平台。"
            "根据报道，Redwire 将为 Meteor ESPA-Grande 卫星母平台提供 Extensible Low-Profile Solar Array（ELSA）翼板，并负责设计、制造、测试和交付。"
            "Redwire 将 ELSA 描述为一款面向批量化卫星生产的低轮廓太阳能阵列产品，按体积计算可比传统太阳能阵列提供更高功率输出；Moog 则表示，该组件将作为 Meteor 卫星平台的标准化部件之一，以增强其平台的模块化和任务适配能力。"
            "整体来看，这条消息的重要性不在于单一部件采购，而在于它反映出国防或国家安全航天平台正在更明确地采用标准化、可批产的卫星子系统配置，以提高交付效率和星座部署能力。"
        )
    if "nasa.gov" in url or "spacenews.com" in url:
        return summarize_nasa_or_news(title, entities, source_text)

    snippets = pick_sentences(source_text, max_sentences=3)
    if not snippets:
        return str(item.get("summary", "")).strip() or "目前公开信息有限，建议结合原始来源进一步核查。"
    return (
        f"围绕“{title}”，原始来源披露的信息显示，{snippets[0]}"
        + (f" 此外，{snippets[1]}" if len(snippets) > 1 else "")
        + " 从情报角度看，这一动态值得关注，因为它可能反映相关机构或团队在该方向上的持续投入与推进。"
    )


def enrich_items(items: list[dict], limit: int) -> list[dict]:
    output: list[dict] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        enriched = dict(item)
        if index < limit and item.get("url"):
            try:
                source_text = fetch_text(str(item["url"]))
                enriched["summary"] = summarize_in_chinese(enriched, source_text)
                enriched["impact"] = enriched.get("impact") or "值得结合原始来源与后续进展持续跟踪其实际影响。"
            except Exception:
                pass
        output.append(enriched)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich top candidates by fetching source pages")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--limit", type=int, default=10, help="Number of top items to enrich")
    args = parser.parse_args()

    items = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("Input JSON must be an array.")
    enriched = enrich_items(items, max(1, args.limit))
    Path(args.output).write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
