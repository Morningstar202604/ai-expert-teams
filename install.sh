#!/usr/bin/env bash
# opencode-expert-teams 一键安装脚本
# 用法: ./install.sh [--dry-run|-c]
#   --dry-run / -c : 仅列出将执行的操作，不实际创建软链

set -euo pipefail

# ── 配置 ──────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCODE_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
AGENTS_TARGET="${OPENCODE_CONFIG}/agents"
SKILLS_TARGET="${OPENCODE_CONFIG}/skills"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" || "${1:-}" == "-c" ]]; then
  DRY_RUN=true
  echo "[dry-run] 以下操作仅预览，不会实际执行"
  echo "----------------------------------------"
fi

# ── 辅助函数 ──────────────────────────────────────────
log()  { echo "  $*"; }
ok()   { echo "  ✅ $*"; }
skip() { echo "  ⏭️  $*"; }

run() {
  if $DRY_RUN; then
    echo "  [dry-run] $*"
  else
    eval "$@"
  fi
}

# ── 1. 创建 opencode 配置目录 ─────────────────────────
echo ""
echo "[1/4] 准备 opencode 配置目录"
if [[ ! -d "${OPENCODE_CONFIG}" ]]; then
  run "mkdir -p '${OPENCODE_CONFIG}'"
  ok "创建 ${OPENCODE_CONFIG}"
else
  skip "${OPENCODE_CONFIG} 已存在"
fi

# ── 2. 软链仓库到 agents 目录 ─────────────────────────
echo ""
echo "[2/4] 链接 agents 目录"
run "ln -sfn '${REPO_ROOT}' '${AGENTS_TARGET}'"
if $DRY_RUN; then
  log "将链接: ${AGENTS_TARGET} -> ${REPO_ROOT}"
else
  if [[ -L "${AGENTS_TARGET}" ]]; then
    ok "agents 软链已更新: ${AGENTS_TARGET} -> $(readlink "${AGENTS_TARGET}")"
  else
    ok "agents 软链已创建: ${AGENTS_TARGET} -> ${REPO_ROOT}"
  fi
fi

# ── 3. 软链全部 skill 包到 skills 目录 ────────────────
echo ""
echo "[3/4] 链接 skill 包"
if [[ ! -d "${SKILLS_TARGET}" ]]; then
  run "mkdir -p '${SKILLS_TARGET}'"
  ok "创建 ${SKILLS_TARGET}"
else
  skip "${SKILLS_TARGET} 已存在"
fi

SKILL_COUNT=0

# 3a. 团队专用 skills: teams/<team>/skills/<name>/
for team_dir in "${REPO_ROOT}"/teams/*/skills/*/; do
  [[ -d "${team_dir}" ]] || continue
  skill_name="$(basename "${team_dir}")"
  # 校验 SKILL.md 存在
  if [[ ! -f "${team_dir}/SKILL.md" ]]; then
    echo "  ⚠️  跳过 ${skill_name}: 缺少 SKILL.md"
    continue
  fi
  run "ln -sfn '${team_dir}' '${SKILLS_TARGET}/${skill_name}'"
  if $DRY_RUN; then
    log "将链接: ${SKILLS_TARGET}/${skill_name} -> ${team_dir}"
  else
    ok "skill: ${skill_name}"
  fi
  SKILL_COUNT=$((SKILL_COUNT + 1))
done

# 3b. 通用 skills: skills/<name>/
if [[ -d "${REPO_ROOT}/skills" ]]; then
  for skill_dir in "${REPO_ROOT}"/skills/*/; do
    [[ -d "${skill_dir}" ]] || continue
    skill_name="$(basename "${skill_dir}")"
    if [[ ! -f "${skill_dir}/SKILL.md" ]]; then
      echo "  ⚠️  跳过 ${skill_name}: 缺少 SKILL.md"
      continue
    fi
    # 防重名：如果团队 skill 已占用同名，通用 skill 加前缀
    target_path="${SKILLS_TARGET}/${skill_name}"
    if [[ -L "${target_path}" || -d "${target_path}" ]]; then
      existing_target="$(readlink "${target_path}" 2>/dev/null || echo "${target_path}")"
      if [[ "${existing_target}" == "${skill_dir}" ]]; then
        skip "skill: ${skill_name} (已指向同一路径)"
        SKILL_COUNT=$((SKILL_COUNT + 1))
        continue
      fi
      echo "  ⚠️  命名冲突: ${skill_name} 已存在 (指向 ${existing_target})，跳过通用版本"
      continue
    fi
    run "ln -sfn '${skill_dir}' '${target_path}'"
    if $DRY_RUN; then
      log "将链接: ${target_path} -> ${skill_dir}"
    else
      ok "skill: ${skill_name} (通用)"
    fi
    SKILL_COUNT=$((SKILL_COUNT + 1))
  done
fi

echo "  共链接 ${SKILL_COUNT} 个 skill 包"

# ── 4. 验证 ───────────────────────────────────────────
echo ""
echo "[4/4] 安装验证"
if $DRY_RUN; then
  log "dry-run 模式跳过实际验证"
else
  # 验证 agents 软链
  if [[ -L "${AGENTS_TARGET}" && -d "${AGENTS_TARGET}" ]]; then
    ok "agents 目录可访问: $(ls "${AGENTS_TARGET}"/*.md 2>/dev/null | wc -l) 个根级 agent 文件"
  else
    echo "  ❌ agents 软链异常"
    exit 1
  fi

  # 验证 skills 目录
  linked_skills=0
  for skill_dir in "${SKILLS_TARGET}"/*/; do
    [[ -d "${skill_dir}" ]] || continue
    if [[ -f "${skill_dir}/SKILL.md" ]]; then
      linked_skills=$((linked_skills + 1))
    fi
  done
  ok "skills 目录可访问: ${linked_skills} 个已安装 skill（含 SKILL.md）"

  # 验证 opencode.json
  if [[ -f "${REPO_ROOT}/opencode.json" ]]; then
    ok "opencode.json 存在（skill 权限已配置）"
  else
    echo "  ⚠️  未找到 opencode.json，skill 可能需要手动授权"
  fi
fi

# ── 完成 ──────────────────────────────────────────────
echo ""
echo "========================================"
if $DRY_RUN; then
  echo "  dry-run 完成，共 ${SKILL_COUNT} 个 skill 将被链接"
else
  echo "  安装完成！"
  echo "  agents: ${AGENTS_TARGET}"
  echo "  skills: ${SKILLS_TARGET} (${SKILL_COUNT} 个)"
fi
echo "========================================"
echo ""
echo "使用示例:"
echo "  opencode run --agent project-director \"你的任务\""
echo "  opencode run --agent teams/fullstack-web-team/agents/fullstack-team-lead \"做个 Web 应用\""
echo ""
