#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-site.py —— 从仓库实装数据生成官网 index.html（数据永不漂移）

统计 teams/*/agents 与 teams/*/skills 及通用 skills/，计算官网模板占位符，
生成 site/index.html。

用法：
  python3 build-site.py            生成 site/index.html（覆盖写）
  python3 build-site.py --check    生成并对比现有 site/index.html，不一致则退出码 1（CI 防漂移）

口径（与 verify.py / SKILLS_INDEX.md 保持一致）：
  - 专家总数 = 7 个团队 agents 合计
  - 团队专属技能 = teams/*/skills 子目录数合计
  - 通用技能 = skills/ 子目录数
  - 总技能 = 团队专属 + 通用
  - software 团队无独立 skills，绑定 3 个通用技能（api-design-reviewer / test-case-generator-v2 / uml-and-software-architecture-visualization）
  - core 单兵 = 所有 teams/*/agents/ 下 core-* 前缀的 agent
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TEAMS = ["academic-paper-team", "fullstack-web-team", "math-modeling-team",
         "software-dev-team", "visual-design-team", "content-writing-team",
         "video-production-team"]
TEAM_LABELS = {
    "academic-paper-team": ("T_ACADEMIC", "S_ACADEMIC"),
    "fullstack-web-team": ("T_FULLSTACK", "S_FULLSTACK"),
    "math-modeling-team": ("T_MATH", "S_MATH"),
    "software-dev-team": ("T_SOFTWARE", "S_SOFTWARE"),
    "visual-design-team": ("T_VISUAL", "S_VISUAL"),
    "content-writing-team": ("T_CONTENT", "S_CONTENT"),
    "video-production-team": ("T_VIDEO", "S_VIDEO"),
}
SOFTWARE_BOUND_SKILLS = 3  # 绑定通用 skills/ 中 3 个（见 SKILLS_INDEX.md）


def count_agents(team):
    d = os.path.join(ROOT, "teams", team, "agents")
    return len([f for f in os.listdir(d) if f.endswith(".md")]) if os.path.isdir(d) else 0


def count_team_skills(team):
    d = os.path.join(ROOT, "teams", team, "skills")
    if not os.path.isdir(d):
        return 0
    return len([x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))])


def count_general_skills():
    d = os.path.join(ROOT, "skills")
    return len([x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))])


def count_core_agents():
    n = 0
    for team in TEAMS:
        d = os.path.join(ROOT, "teams", team, "agents")
        if not os.path.isdir(d):
            continue
        n += len([f for f in os.listdir(d) if f.startswith("core-") and f.endswith(".md")])
    return n


def compute():
    stats = {}
    team_agents = {}
    team_skills = {}
    for team in TEAMS:
        a = count_agents(team)
        s = count_team_skills(team)
        if team == "software-dev-team":
            s = SOFTWARE_BOUND_SKILLS
        team_agents[team] = a
        team_skills[team] = s
        tkey, skey = TEAM_LABELS[team]
        stats[tkey] = a
        stats[skey] = s
    general = count_general_skills()
    n_agents = sum(team_agents.values())
    n_team_skills = sum(team_skills.values()) - SOFTWARE_BOUND_SKILLS  # 团队专属（不含软件绑定的通用）
    n_skills = n_team_skills + general
    n_teams = len(TEAMS)
    n_core = count_core_agents()

    stats["N_AGENTS"] = n_agents
    stats["N_SKILLS"] = n_skills
    stats["N_TEAMS"] = n_teams
    stats["N_TEAM_SKILLS"] = n_team_skills
    stats["N_GENERAL_SKILLS"] = general
    stats["N_CORE_UNITS"] = n_core
    # BAR_DATA 按 yAxis 自上而下：视频/内容/视觉/软件/数学/全栈/学术
    stats["BAR_DATA"] = "[%d,%d,%d,%d,%d,%d,%d]" % (
        team_agents["video-production-team"], team_agents["content-writing-team"],
        team_agents["visual-design-team"], team_agents["software-dev-team"],
        team_agents["math-modeling-team"], team_agents["fullstack-web-team"],
        team_agents["academic-paper-team"])
    return stats


def build(stats):
    tpl = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()
    for k, v in stats.items():
        tpl = tpl.replace("{{%s}}" % k, str(v))
    leftovers = [m for m in __import__("re").findall(r"\{\{[A-Z_]+\}\}", tpl)]
    if leftovers:
        raise SystemExit("模板存在未替换占位符: %s" % leftovers)
    return tpl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="对比现有 site/index.html，不一致则失败")
    args = ap.parse_args()
    stats = compute()
    out = build(stats)
    if args.check:
        target = os.path.join(ROOT, "site", "index.html")
        if not os.path.exists(target):
            print("site/index.html 不存在，请先运行 python3 build-site.py")
            sys.exit(1)
        cur = open(target, encoding="utf-8").read()
        if cur != out:
            print("✗ site/index.html 与仓库实装数据不一致（数据漂移）。请运行 python3 build-site.py 重新生成。")
            sys.exit(1)
        print("✓ site/index.html 与仓库实装一致（%d 专家 / %d 技能 / %d 团队）" %
              (stats["N_AGENTS"], stats["N_SKILLS"], stats["N_TEAMS"]))
    else:
        target = os.path.join(ROOT, "site", "index.html")
        with open(target, "w", encoding="utf-8") as f:
            f.write(out)
        print("✓ site/index.html 已生成：%d 专家 / %d 技能 / %d 团队 / %d 通用技能 / %d core 单兵" %
              (stats["N_AGENTS"], stats["N_SKILLS"], stats["N_TEAMS"],
               stats["N_GENERAL_SKILLS"], stats["N_CORE_UNITS"]))


if __name__ == "__main__":
    main()
