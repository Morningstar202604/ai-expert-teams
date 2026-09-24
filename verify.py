#!/usr/bin/env python3
"""全局校验脚本：验证 skill 包、agent frontmatter、结构完整性。"""
import os
import re
import sys
import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
errors = []
warnings = []

def err(msg):
    errors.append(msg)
    print(f"  ❌ {msg}")

def ok(msg):
    print(f"  ✅ {msg}")

def warn(msg):
    warnings.append(msg)
    print(f"  ⚠️  {msg}")

def parse_frontmatter(text):
    """解析 markdown 文件的 YAML frontmatter，返回 (dict, body)。"""
    if not text.startswith('---'):
        return None, text
    lines = text.split('\n')
    # 找到闭合的 ---
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            close_idx = i
            break
    if close_idx is None:
        return None, text
    fm_text = '\n'.join(lines[1:close_idx])
    body = '\n'.join(lines[close_idx+1:])
    try:
        fm = yaml.safe_load(fm_text)
        if fm is None:
            fm = {}
        return fm, body
    except yaml.YAMLError as e:
        return f"YAML_ERROR: {e}", body

# ═══════════════════════════════════════════════════════
# 1. 校验 skill 包
# ═══════════════════════════════════════════════════════
print("\n=== 1. Skill 包校验 ===")
skill_dirs = []
# 团队 skills
for team in os.listdir(f"{BASE}/teams"):
    skills_path = f"{BASE}/teams/{team}/skills"
    if os.path.isdir(skills_path):
        for name in sorted(os.listdir(skills_path)):
            d = f"{skills_path}/{name}"
            if os.path.isdir(d):
                skill_dirs.append((name, d, f"teams/{team}/skills"))
# 通用 skills
if os.path.isdir(f"{BASE}/skills"):
    for name in sorted(os.listdir(f"{BASE}/skills")):
        d = f"{BASE}/skills/{name}"
        if os.path.isdir(d):
            skill_dirs.append((name, d, "skills"))

print(f"  发现 {len(skill_dirs)} 个 skill 包")
skill_names = set()
for name, path, location in skill_dirs:
    skill_md = f"{path}/SKILL.md"
    if not os.path.isfile(skill_md):
        err(f"[{name}] 缺少 SKILL.md ({location})")
        continue
    text = open(skill_md, encoding='utf-8').read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        err(f"[{name}] 无 frontmatter")
        continue
    if isinstance(fm, str) and fm.startswith("YAML_ERROR"):
        err(f"[{name}] frontmatter YAML 语法错误: {fm}")
        continue
    # name 校验
    if 'name' not in fm:
        err(f"[{name}] frontmatter 缺 name 字段")
    elif fm['name'] != name:
        err(f"[{name}] name='{fm['name']}' 与目录名不一致")
    # name 格式校验
    if 'name' in fm and not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', str(fm['name'])):
        err(f"[{name}] name 格式不合规（须小写字母数字单连字符）")
    # description 校验
    if 'description' not in fm:
        err(f"[{name}] frontmatter 缺 description 字段")
    else:
        desc_len = len(str(fm['description']))
        if desc_len < 1 or desc_len > 1024:
            err(f"[{name}] description 长度 {desc_len} 超出 1-1024")
    # 行数校验
    line_count = len(text.split('\n'))
    if line_count < 50:
        warn(f"[{name}] 仅 {line_count} 行，建议 50-120 行")
    elif line_count > 120:
        warn(f"[{name}] {line_count} 行，超出 120 行上限")
    # 检查关键章节
    if '## ' not in body:
        warn(f"[{name}] 正文无 ## 章节标题")
    skill_names.add(name)

ok(f"{len(skill_dirs)} 个 skill 包校验完成（{len(errors)} 错误，{len(warnings)} 警告）")

# ═══════════════════════════════════════════════════════
# 2. 校验 agent frontmatter
# ═══════════════════════════════════════════════════════
print("\n=== 2. Agent frontmatter 校验 ===")
agent_files = []
for team in os.listdir(f"{BASE}/teams"):
    agents_path = f"{BASE}/teams/{team}/agents"
    if os.path.isdir(agents_path):
        for fname in sorted(os.listdir(agents_path)):
            if fname.endswith('.md'):
                agent_files.append((fname[:-3], f"{agents_path}/{fname}", team))

# 加上 project-director
agent_files.append(("project-director", f"{BASE}/project-director.md", "root"))

print(f"  发现 {len(agent_files)} 个 agent 文件")
READONLY_CORE = {"core-architect", "core-code-reviewer", "core-security-auditor", "core-test-engineer"}
TEAM_LEADS = {"academic-team-lead", "fullstack-team-lead", "math-team-lead", "software-team-lead"}
TEAM_DIR_MAP = {
    "academic-team-lead": "academic-paper-team",
    "fullstack-team-lead": "fullstack-web-team",
    "math-team-lead": "math-modeling-team",
    "software-team-lead": "software-dev-team",
}

agent_errors_before = len(errors)
for agent_id, path, team in agent_files:
    text = open(path, encoding='utf-8').read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        err(f"[{agent_id}] 无 frontmatter")
        continue
    if isinstance(fm, str) and fm.startswith("YAML_ERROR"):
        err(f"[{agent_id}] frontmatter YAML 语法错误: {fm}")
        continue
    # 必填字段
    if 'description' not in fm:
        err(f"[{agent_id}] 缺 description")
    if 'mode' not in fm:
        err(f"[{agent_id}] 缺 mode")
    # 禁止 model 字段
    if 'model' in fm:
        err(f"[{agent_id}] 不应有 model 字段")
    # project-director 不需要 temperature
    if agent_id == "project-director":
        continue
    # temperature
    if 'temperature' not in fm:
        err(f"[{agent_id}] 缺 temperature")
    else:
        t = fm['temperature']
        if not isinstance(t, (int, float)) or t < 0 or t > 1:
            err(f"[{agent_id}] temperature={t} 不合规")
    # team-lead 校验
    if agent_id in TEAM_LEADS:
        if fm.get('mode') != 'primary':
            err(f"[{agent_id}] team-lead mode 应为 primary")
        if fm.get('temperature') != 0.1:
            err(f"[{agent_id}] team-lead temperature 应为 0.1")
        if 'permission' not in fm or 'task' not in fm['permission']:
            err(f"[{agent_id}] 缺 permission.task 配置")
        else:
            allow = fm['permission']['task'].get('allow', [])
            expected = f"teams/{TEAM_DIR_MAP[agent_id]}/agents/*"
            if expected not in allow:
                err(f"[{agent_id}] permission.task.allow 应含 '{expected}'")
    else:
        if fm.get('mode') != 'subagent':
            err(f"[{agent_id}] subagent mode 应为 subagent (实际 {fm.get('mode')})")
    # core-* 只读校验
    if agent_id in READONLY_CORE:
        if 'tools' not in fm:
            err(f"[{agent_id}] core-* 缺 tools 配置")
        else:
            if fm['tools'].get('write') is not False:
                err(f"[{agent_id}] core-* tools.write 应为 false")
            if fm['tools'].get('edit') is not False:
                err(f"[{agent_id}] core-* tools.edit 应为 false")

agent_err_count = len(errors) - agent_errors_before
ok(f"{len(agent_files)} 个 agent 校验完成（{agent_err_count} 错误）")

# ═══════════════════════════════════════════════════════
# 3. 校验 8 个重写 agent 的结构完整性
# ═══════════════════════════════════════════════════════
print("\n=== 3. 重写 Agent 结构校验 ===")
REWRITE_AGENTS = [
    "teams/academic-paper-team/agents/core-researcher.md",
    "teams/fullstack-web-team/agents/core-architect.md",
    "teams/fullstack-web-team/agents/core-code-reviewer.md",
    "teams/fullstack-web-team/agents/core-security-auditor.md",
    "teams/fullstack-web-team/agents/core-test-engineer.md",
    "teams/software-dev-team/agents/software-architect.md",
    "teams/software-dev-team/agents/software-reviewer.md",
    "teams/software-dev-team/agents/software-tester.md",
]
REQUIRED_SECTIONS = ["核心能力", "工作流程", "输出规范", "输入规范", "注意事项"]
for rel_path in REWRITE_AGENTS:
    path = f"{BASE}/{rel_path}"
    text = open(path, encoding='utf-8').read()
    line_count = len(text.split('\n'))
    if line_count < 30:
        err(f"[{rel_path}] 仅 {line_count} 行，疑似未重写")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            err(f"[{rel_path}] 缺章节: {section}")
    # 检查交接模板
    if "交接模板" not in text:
        err(f"[{rel_path}] 缺交接模板")
ok(f"8 个重写 agent 结构校验完成")

# ═══════════════════════════════════════════════════════
# 4. 人数口径校验
# ═══════════════════════════════════════════════════════
print("\n=== 4. 人数口径校验 ===")
team_counts = {}
for agent_id, path, team in agent_files:
    if team == "root":
        continue
    team_counts[team] = team_counts.get(team, 0) + 1

expected = {"academic-paper-team": 18, "fullstack-web-team": 19, "math-modeling-team": 9, "software-dev-team": 12}
total = 0
for team, count in sorted(team_counts.items()):
    exp = expected.get(team, "?")
    status = "✅" if count == exp else "❌"
    print(f"  {status} {team}: {count} (预期 {exp})")
    total += count
    if count != exp:
        err(f"{team} 人数 {count} != 预期 {exp}")
print(f"  总计: {total} (预期 58)")
if total != 58:
    err(f"总人数 {total} != 58")

# ═══════════════════════════════════════════════════════
# 5. 文件存在性校验
# ═══════════════════════════════════════════════════════
print("\n=== 5. 关键文件校验 ===")
for f in ["install.sh", "opencode.json", "SKILLS_INDEX.md", "README.md", "AGENTS.md", "project-director.md"]:
    if os.path.isfile(f"{BASE}/{f}"):
        ok(f"{f} 存在")
    else:
        err(f"{f} 不存在")

# opencode.json 内容校验
import json
try:
    with open(f"{BASE}/opencode.json") as f:
        cfg = json.load(f)
    if cfg.get("permission", {}).get("skill", {}).get("*") == "allow":
        ok("opencode.json skill 权限配置正确")
    else:
        err("opencode.json permission.skill.* 应为 allow")
except Exception as e:
    err(f"opencode.json JSON 解析失败: {e}")

# install.sh 可执行
if os.access(f"{BASE}/install.sh", os.X_OK):
    ok("install.sh 可执行")
else:
    err("install.sh 不可执行")

# ═══════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 50)
if errors:
    print(f"❌ 校验失败：{len(errors)} 个错误")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)
else:
    print(f"✅ 全部校验通过！{len(warnings)} 个警告（非阻断）")
    if warnings:
        for w in warnings:
            print(f"   ⚠️  {w}")
    sys.exit(0)
