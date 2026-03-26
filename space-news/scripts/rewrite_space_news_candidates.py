#!/usr/bin/env python3
"""Rewrite mixed-language candidate summaries into Chinese intelligence-brief style."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from space_news_overrides import IMPACT_OVERRIDES, SUMMARY_OVERRIDES

ENGLISH_RE = re.compile(r"[A-Za-z]{4,}")

CATEGORY_HINTS = {
    "mission": "该信息主要反映近期航天任务、项目推进或任务节点变化。",
    "ai_product": "该信息主要反映人工智能在航天系统、任务运营或相关产品中的应用进展。",
    "eo_ai": "该信息主要涉及遥感、对地观测或相关智能处理能力的发展。",
    "research": "该信息主要体现科研论文、研究成果或技术验证方面的新进展。",
    "conference": "该信息主要体现会议、征稿或学术活动中的方向性信号。",
    "open_source": "该信息主要体现开源项目、工具链或知识基础设施的更新与价值。",
    "agency_program": "该信息主要体现航天机构的新项目、新平台或新能力布局。",
    "startup": "该信息主要体现商业航天公司或初创企业的最新动态。",
}

IMPACT_HINTS = {
    "defense": "值得关注其是否进一步影响空间安全、态势感知、国防航天能力或双用途技术布局。",
    "commercial": "值得关注其是否形成可商业化复制的产品能力、客户场景或服务模式。",
    "civil": "值得关注其在公共服务、民用遥感、通信导航或社会治理场景中的落地潜力。",
    "research_academic": "值得关注其是否在后续研究、会议、论文引用或开源生态中形成持续影响。",
    "agency_national": "值得关注其是否进入机构级项目管线，并影响后续国际合作、资金流向与技术路线。",
}


def needs_rewrite(text: str) -> bool:
    if not text:
        return True
    english_hits = len(ENGLISH_RE.findall(text))
    chinese_hits = len(re.findall(r"[\u4e00-\u9fff]", text))
    return english_hits > 12 or chinese_hits < 20


def rewrite_summary(item: dict) -> str:
    original = str(item.get("summary", "")).strip()
    title = str(item.get("title", "")).strip()
    if title in SUMMARY_OVERRIDES:
        return SUMMARY_OVERRIDES[title]
    entities = str(item.get("entities", "")).strip()
    category = str(item.get("category", "mission")).strip().lower()
    domain = str(item.get("domain_tag", "research_academic")).strip().lower()
    hint = CATEGORY_HINTS.get(category, "该信息体现了航天领域近期值得关注的动态。")

    if not original:
        return (
            f"{hint} 目前公开信息有限，但从标题与来源判断，这一动态与航天领域近期发展存在直接关联。"
            f"若后续有更多材料披露，建议重点关注其技术细节、合作背景与后续推进节点。"
        )

    cleaned = " ".join(original.split())
    if not needs_rewrite(cleaned):
        return cleaned

    subject = entities or "相关机构或团队"

    if category == "conference":
        return (
            f"{hint}{subject}近期公开了与“{title}”相关的信息。就会议或学术活动信号而言，"
            f"这类动态的价值往往不只在于活动本身，而在于它反映出当前社区正在重点关注哪些技术问题、应用场景或合作方向。"
            f"如果后续议程、征稿主题、主讲人与参会机构进一步明确，这类信息通常能够帮助外部观察者更早判断国际航天 AI 生态的重点变化。"
        )

    if category == "startup":
        return (
            f"{hint}{subject}近期围绕“{title}”释放了新的业务或技术进展信号。"
            f"从商业航天视角看，这类动态的意义通常不只是单次新闻发布，而在于它可能反映公司在产品化方向、市场切入点、客户需求或资本叙事上的最新布局。"
            f"如果后续伴随合同、融资、合作或实测结果披露，其情报价值会进一步上升。"
        )

    if category == "open_source":
        return (
            f"{hint}围绕“{title}”所代表的开源资源或工具链，当前公开信息显示该方向仍在持续积累方法、知识与工程入口。"
            f"这类开源动态的重要性通常不在于单次更新本身，而在于它是否持续降低研究与工程团队进入该领域的门槛，并帮助形成共享的技术基础设施。"
            f"对航天 AI 观察而言，这往往也是判断某个方向是否保持活跃的重要生态信号。"
        )

    if category == "research":
        return (
            f"{hint}从公开摘要判断，“{title}”所对应的工作更偏向技术方法、模型设计或系统验证层面的推进。"
            f"这类成果的价值通常不只体现在论文层面的新颖性，还体现在它是否回应了航天场景中的真实约束，例如泛化能力、算力限制、系统安全或任务可部署性。"
            f"如果后续出现更多实验结果、代码公开或会议传播，这类研究往往会对相关子方向形成更持续的影响。"
        )

    if category == "agency_program":
        return (
            f"{hint}{subject}围绕“{title}”释放出的信息，更多体现的是机构层面的项目布局、平台建设或能力方向选择。"
            f"从情报角度看，这类机构级信号的价值通常高于普通新闻，因为它往往与资源配置、合作机制、未来任务方向以及长期技术路线有关。"
            f"如果后续伴随项目细节、合作伙伴或试验计划公开，其战略参考价值会进一步提升。"
        )

    if category == "ai_product" and domain == "commercial":
        return (
            f"{hint}{subject}近期围绕“{title}”披露的内容，反映出 AI 能力正进一步进入商业航天产品与服务体系。"
            f"这类动态的关键不只在于技术表述本身，而在于它是否意味着公司正把 AI 作为差异化能力嵌入通信、遥感、任务支持或空间数据服务链条中。"
            f"若后续能看到客户采用、合作项目或产品迭代节奏，其商业情报价值会更高。"
        )

    return (
        f"{hint}{subject}近期公开了与“{title}”相关的阶段性进展。"
        f"从公开信息看，这类动态通常不只代表单次消息披露，更反映出相关主体在该方向上的持续投入与能力演进。"
        f"若后续有更具体的技术细节、合作安排或项目节点披露，其参考价值还会继续提升。"
    )


def rewrite_impact(item: dict) -> str:
    original = str(item.get("impact", "")).strip()
    title = str(item.get("title", "")).strip()
    if title in IMPACT_OVERRIDES:
        return IMPACT_OVERRIDES[title]
    if original and not needs_rewrite(original):
        return original

    domain = str(item.get("domain_tag", "research_academic")).strip().lower()
    return IMPACT_HINTS.get(domain, "值得关注其对后续技术路线、产业布局或研究方向的持续影响。")


def process_items(items: list[dict]) -> list[dict]:
    output: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        new_item = dict(item)
        new_item["summary"] = rewrite_summary(new_item)
        new_item["impact"] = rewrite_impact(new_item)
        output.append(new_item)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Rewrite candidate summaries into Chinese intelligence style")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    args = parser.parse_args()

    items = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("Input JSON must be an array.")
    rewritten = process_items(items)
    Path(args.output).write_text(json.dumps(rewritten, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
