# 技能索引 - SKILLS_INDEX.md

> 统一维护所有可用 skill，按**归属团队**分类。调用失败/未安装时自动回退通用经验，不阻塞。

## 目录结构
```
skills/                                                   # 通用 skill（全团队共用，install.sh 软链到 ~/.config/opencode/skills/）
teams/<team-name>/skills/                                 # 团队专用 skill（install.sh 软链到 ~/.config/opencode/skills/）
~/.config/opencode/skills/                                # 安装后的 skill 目录（全部为一层软链）
```

> 全部 31 个 skill 已实装（学术 7 + 数学 2 + 软件 3 + 全栈 11 + 通用 8）。`install.sh` 自动将团队专用与通用 skill 统一软链到 `~/.config/opencode/skills/<name>/`，opencode 按 `<name>/SKILL.md` 发现。

---

## 📚 学术论文团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `paper-topic-selector` | 选题缺口识别/可行性打分 | academic-topic-strategist | teams/academic-paper-team/skills/ | P1 |
| `journal-adapt` | 期刊格式/禁词/模板适配 | academic-format-guardian, academic-editor-liaison | teams/academic-paper-team/skills/ | P1 |
| `lit-review` | PRISMA 流程文献综述 | academic-literature-synthesizer, academic-topic-strategist | teams/academic-paper-team/skills/ | P1 |
| `figure-maker` | 论文级图表生成 | academic-data-visualizer | teams/academic-paper-team/skills/ | P1 |
| `model-formulator` | 文字问题→数学模型 | academic-research-designer | teams/academic-paper-team/skills/ | P1 |
| `model-solver` | 数学模型数值求解 | academic-statistical-methodologist | teams/academic-paper-team/skills/ | P1 |
| `pdf-pipeline` | PDF 合并/拆分/提取/元数据 | academic-format-guardian | teams/academic-paper-team/skills/ | P1 |

---

## 📐 数学建模团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `math-modeling-guosai` | 国赛资料库：题型映射/模型速查/LaTeX 骨架/评审自查表 | math-team-lead, math-modeler, math-writer, math-qa-reviewer | teams/math-modeling-team/skills/ | P0 |
| `math-modeling-selfcheck` | 国赛自检闸门：思想纪律 + 思维强化，开工前/产出后强制过单 | 全员（math-* 每 Phase 必过） | teams/math-modeling-team/skills/ | P0 |

---

## 🧩 软件开发交付团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `api-design-reviewer` | REST/GraphQL 设计评审 | software-api-designer, software-reviewer | teams/software-dev-team/skills/ | P1 |
| `test-case-generator-v2` | 企业级测试用例生成 | software-qa-engineer, software-tester | teams/software-dev-team/skills/ | P1 |
| `uml-and-software-architecture-visualization` | 架构/时序/类图生成 | software-architect | teams/software-dev-team/skills/ | P1 |

> software 团队各成员遵循「开工前 Glob 扫团队 skills 目录」协议，命中即用、失败退回通用经验；上表 3 个 skill 已实装于团队 skills/ 目录。

---

## 🌐 全栈 Web 团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `docker-development` | Dockerfile 优化/多阶段构建 | fullstack-devops-engineer | teams/fullstack-web-team/skills/ | P1 |
| `helm-chart-builder` | K8s Helm Chart 生成 | fullstack-devops-engineer | teams/fullstack-web-team/skills/ | P1 |
| `terraform-patterns` | IaC 模块/状态/安全 | fullstack-devops-engineer | teams/fullstack-web-team/skills/ | P1 |
| `github-actions-advanced` | 高级 Workflow/密钥/OIDC | fullstack-ci-cd-engineer | teams/fullstack-web-team/skills/ | P1 |
| `supabase-postgres-best-practices` | Postgres 性能/最佳实践 | fullstack-database-engineer | teams/fullstack-web-team/skills/ | P1 |
| `react-best-practices` | React/Next.js 性能模式 | fullstack-frontend-engineer | teams/fullstack-web-team/skills/ | P1 |
| `shadcn` | shadcn/ui 组件管理 | fullstack-frontend-engineer | teams/fullstack-web-team/skills/ | P1 |
| `stripe-best-practices` | Stripe 支付/订阅/Connect | fullstack-backend-engineer, fullstack-api-designer | teams/fullstack-web-team/skills/ | P1 |
| `observability-designer` | SLI/SLO/告警/指标 | fullstack-devops-engineer | teams/fullstack-web-team/skills/ | P1 |
| `slo-architect` | SLO 定义/错误预算/燃尽率 | fullstack-devops-engineer | teams/fullstack-web-team/skills/ | P1 |
| `kubernetes-operator` | CRD/Controller/Operator | fullstack-devops-engineer | teams/fullstack-web-team/skills/ | P1 |

---

## 🔧 通用基础 skill（全团队共用）

| Skill ID | 描述 | 适配团队 | 位置 | 优先级 |
|----------|------|----------|------|--------|
| `web-search` | 免费联网搜索（SearXNG/DuckDuckGo）、缓存 | 全部 | skills/ | P0 |
| `deep-research` | 多轮检索+综合报告、引用溯源 | 学术、全栈、数学建模 | skills/ | P1 |
| `security-scan` | 单遍仓库安全审计 | 全栈、软件开发 | skills/ | P1 |
| `deep-security-scan` | 多遍深度安全扫描 | 全栈、软件开发 | skills/ | P2 |
| `performance-profiler` | CPU/内存/IO 瓶颈剖析 | 全栈、软件开发 | skills/ | P1 |
| `ci-cd-pipeline-builder` | 流水线生成/门禁/发布 | 全栈、软件开发 | skills/ | P1 |
| `frontend-app-builder` | 前端应用脚手架/组件实现 | 全栈 | skills/ | P1 |
| `frontend-testing-debugging` | 前端 E2E/组件测试调试 | 全栈 | skills/ | P1 |

> `api-design-reviewer`、`test-case-generator-v2`、`uml-and-software-architecture-visualization` 同时被全栈与软件团队复用，实装于 `teams/software-dev-team/skills/`，install.sh 统一软链后全团队可调用。

---

## 调用约定

```python
# 伪代码：skill 调用标准模式
def use_skill(skill_id: str, team_context: str = None, fallback: bool = True):
    try:
        # 1. 优先加载团队专用 skill
        if team_context:
            load_team_skill(team_context, skill_id)
        # 2. 回退用户级/全局 skill
        load_skill(skill_id)
        return execute_skill(skill_id)
    except SkillNotFound:
        if fallback:
            log(f"[Skill Fallback] {skill_id} 未安装，退回通用经验")
            return generic_experience()
        raise
```

### 调用优先级
1. **Team-lead 指定** → 成员必须按指定 skill 执行
2. **成员自查** → Phase 开工前扫描本列表，关键词匹配（含 `team_context`）
3. **无匹配** → 退回通用经验，不阻塞

---

## 维护规则
- 新增 skill → 必须在此表登记（ID/描述/适配 Agent/归属团队/位置/优先级）
- 废弃 skill → 标记 `DEPRECATED`，保留 90 天
- 团队专用 skill → 仅在对应团队目录，不污染全局
- 版本变更 → 更新 `versions.md` 记录 skill 版本