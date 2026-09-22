# 技能索引 - SKILLS_INDEX.md

> 统一维护所有可用 skill，按**归属团队**分类。调用失败/未安装时自动回退通用经验，不阻塞。

## 目录结构
```
~/.workbuddy/skills/                                    # 用户级通用 skill
~/.config/opencode/skills/                              # opencode 专用 skill
teams/<team-name>/skills/                               # 团队专用 skill（相对本目录）
```

---

## 📚 学术论文团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `paper-topic-selector` | 选题缺口识别/可行性打分 | academic-topic-strategist | 团队 skills/ | P1 |
| `journal-adapt` | 期刊格式/禁词/模板适配 | academic-format-guardian, academic-editor-liaison | 团队 skills/ | P1 |
| `lit-review` | PRISMA 流程文献综述 | academic-literature-synthesizer, academic-topic-strategist | 团队 skills/ | P1 |
| `figure-maker` | 论文级图表生成 | academic-data-visualizer | 团队 skills/ | P1 |
| `model-formulator` | 文字问题→数学模型 | academic-research-designer | 团队 skills/ | P1 |
| `model-solver` | 数学模型数值求解 | academic-statistical-methodologist | 团队 skills/ | P1 |
| `pdf-pipeline` | PDF 合并/拆分/提取/元数据 | academic-format-guardian | 团队 skills/ | P1 |

---

## 🌐 全栈 Web 团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `docker-development` | Dockerfile 优化/多阶段构建 | fullstack-devops-engineer | 用户级/团队 skills/ | P1 |
| `helm-chart-builder` | K8s Helm Chart 生成 | fullstack-devops-engineer | 用户级/团队 skills/ | P1 |
| `terraform-patterns` | IaC 模块/状态/安全 | fullstack-devops-engineer | 用户级/团队 skills/ | P1 |
| `github-actions-advanced` | 高级 Workflow/密钥/OIDC | fullstack-ci-cd-engineer | 用户级/团队 skills/ | P1 |
| `supabase-postgres-best-practices` | Postgres 性能/最佳实践 | fullstack-database-engineer | 用户级/团队 skills/ | P1 |
| `react-best-practices` | React/Next.js 性能模式 | fullstack-frontend-engineer | 用户级/团队 skills/ | P1 |
| `shadcn` | shadcn/ui 组件管理 | fullstack-frontend-engineer | 用户级/团队 skills/ | P1 |
| `stripe-best-practices` | Stripe 支付/订阅/Connect | fullstack-backend-engineer, fullstack-api-designer | 用户级/团队 skills/ | P1 |
| `observability-designer` | SLI/SLO/告警/指标 | fullstack-devops-engineer | 用户级/团队 skills/ | P1 |
| `slo-architect` | SLO 定义/错误预算/燃尽率 | fullstack-devops-engineer | 用户级/团队 skills/ | P1 |
| `kubernetes-operator` | CRD/Controller/Operator | fullstack-devops-engineer | 用户级/团队 skills/ | P1 |

---

## 🔢 数学建模团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `math-modeling-guosai` | 国赛建模/求解/写作资料库 | math-team-lead, math-data-analyst, math-literature-researcher, math-modeler, math-solver, math-visualizer, math-writer, math-reproducibility, math-qa-reviewer | 团队 skills/ | P0 |
| `math-modeling-selfcheck` | 自检清单（开工前/产出后） | math 团队全部成员 | 团队 skills/ | P0 |
| 题型/方法/模板/查重类 skill | 细分领域专用 | 对应成员 | 团队 skills/ | P1 |

---

## 💻 软件开发团队专用

| Skill ID | 描述 | 适配 Agent | 位置 | 优先级 |
|----------|------|------------|------|--------|
| `code-reviewer` (内置) | 代码评审规范/模板 | software-reviewer, software-code-quality-reviewer | 团队 skills/ | P1 |
| `test-case-generator-v2` | 企业级测试用例生成 | software-tester, software-qa-engineer, fullstack-qa-engineer | 用户级/团队 skills/ | P1 |
| `api-design-reviewer` | REST API 设计评审 | software-api-designer | 用户级 | P1 |
| `docker-development` / `ci-cd-pipeline-builder` | 容器与流水线 | software-devops-engineer | 用户级 | P1 |
| `aqg-security-review` / OWASP 类 | 安全审计 | software-security-engineer | 用户级 | P1 |
| `sql-database-assistant` | SQL/索引/迁移 | software-database-engineer | 用户级 | P1 |

---

## 🔧 通用基础 skill（全团队共用）

| Skill ID | 描述 | 适配团队 | 优先级 |
|----------|------|----------|--------|
| `web-search` | 免费联网搜索（SearXNG/DuckDuckGo）、缓存 | 全部 | P0 |
| `deep-research` | 多轮检索+综合报告、引用溯源 | 学术、全栈、软件开发 | P1 |
| `security-scan` | 单遍仓库安全审计 | 全栈、软件开发 | P1 |
| `deep-security-scan` | 多遍深度安全扫描 | 全栈 | P2 |
| `api-design-reviewer` | REST/GraphQL 设计评审 | 全栈、软件开发 | P1 |
| `performance-profiler` | CPU/内存/IO 瓶颈剖析 | 全栈、软件开发 | P1 |
| `ci-cd-pipeline-builder` | 流水线生成/门禁/发布 | 全栈、软件开发 | P1 |
| `test-case-generator-v2` | 企业级测试用例生成 | 全栈、软件开发 | P1 |
| `uml-and-software-architecture-visualization` | 架构/时序/类图生成 | 全栈、软件开发 | P1 |
| `frontend-app-builder` | 前端应用脚手架/组件实现 | 全栈 | P1 |
| `frontend-testing-debugging` | 前端 E2E/组件测试调试 | 全栈 | P1 |

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