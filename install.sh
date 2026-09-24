#!/usr/bin/env bash
#
# install.sh — opencode-expert-teams 一键安装脚本
#
# 把本仓库的 agents 与 skills 通过软链接接入 opencode 配置目录：
#   - agents: teams/<team>/agents/*.md 按文件名<name>.md 扁平软链到 $TARGET/agents/
#             （opencode 只发现 agents/ 顶层 .md，不递归子目录；根级 project-director.md 一并软链）
#   - skills: skills/*/ 与 teams/*/skills/*/ 共 52 个 skill 目录，
#             按目录名扁平软链到 $TARGET/skills/<name>/
#
# 用法:
#   bash install.sh [OPENDOCONFIG_DIR]
#   OPENDOCONFIG_DIR 默认 ~/.config/opencode
#
# 幂等：可重复执行，已存在的软链用 ln -sfn 覆盖。

set -euo pipefail

# ---------- 路径与参数 ----------
# 可选参数指定 opencode 配置目录，默认 ~/.config/opencode
TARGET="${1:-$HOME/.config/opencode}"
# 仓库根 = 本脚本所在目录
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$TARGET/agents" "$TARGET/skills"

agent_count=0
skill_count=0

echo "==> opencode 配置目录: $TARGET"
echo "==> 仓库根: $REPO_ROOT"
echo

# ---------- 1. agents：扁平软链（opencode 只发现 agents/ 顶层 .md） ----------
# 遍历 teams/<team>/agents/*.md，按文件名扁平软链到 $TARGET/agents/<name>.md
echo "==> 安装 agents ..."
declare -A _seen_names
for team_dir in "$REPO_ROOT"/teams/*/; do
    [ -d "$team_dir" ] || continue
    team="$(basename "$team_dir")"
    src_agents="$team_dir/agents"
    if [ ! -d "$src_agents" ]; then
        echo "    - 跳过 $team（无 agents 目录）"
        continue
    fi
    for agent_md in "$src_agents"/*.md; do
        [ -f "$agent_md" ] || continue
        name="$(basename "$agent_md" .md)"
        if [ -n "${_seen_names[$name]:-}" ]; then
            echo "    ! 重名 agent: $name（来自 $team 与 ${_seen_names[$name]}），跳过" >&2
            continue
        fi
        _seen_names[$name]="$team"
        ln -sfn "$agent_md" "$TARGET/agents/$name.md"
        agent_count=$((agent_count + 1))
    done
    n="$(find "$src_agents" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')"
    echo "    + $team/agents/  ($n 个 agent，扁平)"
done

# 仓库根级 agent（project-director.md 等），非文档/许可证类 .md
for root_md in "$REPO_ROOT"/*.md; do
    [ -f "$root_md" ] || continue
    base="$(basename "$root_md")"
    case "$base" in
        SKILLS_INDEX.md|README.md|AGENTS.md|CONTRIBUTING.md|CODE_OF_CONDUCT.md|SECURITY.md|LICENSE) continue ;;
    esac
    ln -sfn "$root_md" "$TARGET/agents/$base"
    agent_count=$((agent_count + 1))
    echo "    + $base (根级 agent)"
done

echo

# ---------- 2. skills：扁平软链 ----------
echo "==> 安装 skills ..."
# 收集所有 skill 目录：通用 skills/ + 各团队 teams/*/skills/*/
skill_dirs=()
for s in "$REPO_ROOT"/skills/*/; do
    [ -d "$s" ] && skill_dirs+=("$s")
done
for s in "$REPO_ROOT"/teams/*/skills/*/; do
    [ -d "$s" ] && skill_dirs+=("$s")
done

for src in "${skill_dirs[@]}"; do
    name="$(basename "$src")"
    # 源目录存在、且含 SKILL.md 才链接
    if [ ! -d "$src" ] || [ ! -f "$src/SKILL.md" ]; then
        echo "    - 跳过 $name（缺少 SKILL.md）"
        continue
    fi
    ln -sfn "$src" "$TARGET/skills/$name"
    skill_count=$((skill_count + 1))
    echo "    + $name"
done

echo

# ---------- 3. 安装摘要 ----------
echo "=============================================="
echo " 安装完成"
echo "   agents: $agent_count 个  -> $TARGET/agents/"
echo "   skills: $skill_count 个  -> $TARGET/skills/"
echo "   目标:   $TARGET"
echo "=============================================="
echo
echo "提示：重启 opencode 后生效。"
