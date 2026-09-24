# 技能索引 - SKILLS_INDEX.md

> 本仓库共实装 **31 个 skill**（29 个新建 + 2 个数学建模已有）。
> 统一按归属团队登记；调用失败/未安装时自动回退通用经验，不阻塞。

## 目录结构
```
skills/                                 # 用户级通用 skill（11 个，全团队共用）
teams/<team-name>/skills/               # 团队专用 skill（相对本仓库根）
```

---

## 🔧 通用 skills/（11 个，全团队共用）

| 名称 | 位置 | 一句话用途 |
|------|------|------------|
| `web-search` | `skills/web-search/` | 通用联网搜索：query 改写、多源检索、去重可信度分级、TTL 缓存与引用溯源。 |
| `deep-research` | `skills/deep-research/` | 多轮深度调研：问题拆解、迭代检索、证据分级交叉验证、带引用的综合报告。 |
| `security-scan` | `skills/security-scan/` | 单遍仓库安全审计：依赖 CVE、硬编码密钥、IaC 配置、轻量 SAST 风险清单。 |
| `deep-security-scan` | `skills/deep-security-scan/` | 多遍深度安全扫描：业务逻辑漏洞、越权/注入深挖、攻击面测绘与修复排序。 |
| `performance-profiler` | `skills/performance-profiler/` | CPU/内存/IO 瓶颈定位：Python/Node/系统/前端工具链，先度量再优化。 |
| `ci-cd-pipeline-builder` | `skills/ci-cd-pipeline-builder/` | 流水线生成与质量门禁：阶段划分、覆盖率/漏洞门禁、蓝绿/金丝雀与回滚模板。 |
| `frontend-app-builder` | `skills/frontend-app-builder/` | 前端应用脚手架：Vite/Next.js 目录结构、状态管理选型、路由与 API 层封装。 |
| `frontend-testing-debugging` | `skills/frontend-testing-debugging/` | 前端 E2E/组件测试：Playwright/Vitest 选择器策略、调试与 flaky test 治理。 |
| `api-design-reviewer` | `skills/api-design-reviewer/` | REST/GraphQL 设计评审：命名、状态码、分页版本化、错误格式与安全检查清单。 |
| `test-case-generator-v2` | `skills/test-case-generator-v2/` | 企业级测试用例生成：等价类/边界值/决策表设计、标准化模板与回归集分层。 |
| `uml-and-software-architecture-visualization` | `skills/uml-and-software-architecture-visualization/` | 架构/时序/类/流程图：PlantUML 与 Mermaid、C4 模型与图表选型规则。 |

---

## 📚 学术论文团队 academic-paper-team（7 个）

| 名称 | 位置 | 一句话用途 |
|------|------|------------|
| `paper-topic-selector` | `teams/academic-paper-team/skills/paper-topic-selector/` | 选题缺口识别与可行性打分：研究空白/数据/创新/期刊匹配四维 0-5 分排序。 |
| `journal-adapt` | `teams/academic-paper-team/skills/journal-adapt/` | 目标期刊格式适配：字数、引用格式、图表编号、学术禁词逐项核对清单。 |
| `lit-review` | `teams/academic-paper-team/skills/lit-review/` | PRISMA 文献综述：检索式、纳入排除标准、去重筛选与四阶段流程图矩阵。 |
| `figure-maker` | `teams/academic-paper-team/skills/figure-maker/` | 论文级图表闸门：矢量导出、色盲友好配色、字号坐标轴规范与 Matplotlib 模板。 |
| `model-formulator` | `teams/academic-paper-team/skills/model-formulator/` | 自然语言问题→规范数学模型：决策变量/目标函数/约束/假设四件套。 |
| `model-solver` | `teams/academic-paper-team/skills/model-solver/` | 数学模型数值求解：按线性/非线性/启发式选求解器，给 Python 代码与正确性检查。 |
| `pdf-pipeline` | `teams/academic-paper-team/skills/pdf-pipeline/` | 学术 PDF 流水线：合并/拆分、文本表格提取、OCR、元数据批量写入与自检。 |

---

## 🌐 全栈 Web 团队 fullstack-web-team（11 个）

| 名称 | 位置 | 一句话用途 |
|------|------|------------|
| `docker-development` | `teams/fullstack-web-team/skills/docker-development/` | 生产级 Dockerfile：多阶段构建、层缓存、非 root、健康检查与镜像瘦身。 |
| `helm-chart-builder` | `teams/fullstack-web-team/skills/helm-chart-builder/` | Helm Chart 打包：values 分层、hooks 迁移、依赖管理与升级回滚模板。 |
| `terraform-patterns` | `teams/fullstack-web-team/skills/terraform-patterns/` | Terraform 工程化：模块、S3+DynamoDB 远程状态、workspace 分环境与 CI 门禁。 |
| `github-actions-advanced` | `teams/fullstack-web-team/skills/github-actions-advanced/` | 高级 Workflow：矩阵构建、缓存、environment 保护、OIDC 免密与并发控制。 |
| `supabase-postgres-best-practices` | `teams/fullstack-web-team/skills/supabase-postgres-best-practices/` | Postgres 实战：索引选型、EXPLAIN 慢查询、RLS 策略、分区与 vacuum。 |
| `react-best-practices` | `teams/fullstack-web-team/skills/react-best-practices/` | React/Next.js 性能：memo 取舍、代码分割、SSR/SSG/ISR 与数据获取模板。 |
| `shadcn` | `teams/fullstack-web-team/skills/shadcn/` | shadcn/ui 规范：初始化、组件引入、主题暗色、react-hook-form+zod 表单与 a11y。 |
| `stripe-best-practices` | `teams/fullstack-web-team/skills/stripe-best-practices/` | Stripe 接入：Payment Intent、Webhook 签名校验、订阅生命周期与 Connect 分账。 |
| `observability-designer` | `teams/fullstack-web-team/skills/observability-designer/` | 观测体系：OpenTelemetry 接入、Prometheus 指标命名、Grafana 面板与告警分级。 |
| `slo-architect` | `teams/fullstack-web-team/skills/slo-architect/` | SLO 可靠性：SLI 选型、错误预算计算、多窗口多燃尽率告警与预算冻结发布。 |
| `kubernetes-operator` | `teams/fullstack-web-team/skills/kubernetes-operator/` | Operator 模式：CRD 定义、Reconcile 循环、Finalizer、Webhook 与多版本兼容。 |

---

## 📐 数学建模团队 math-modeling-team（2 个，已有勿动）

| 名称 | 位置 | 一句话用途 |
|------|------|------------|
| `math-modeling-guosai` | `teams/math-modeling-team/skills/math-modeling-guosai/` | 国赛（CUMCM）资料库：题型映射、模型速查、LaTeX 骨架与评审自查表。 |
| `math-modeling-selfcheck` | `teams/math-modeling-team/skills/math-modeling-selfcheck/` | 国赛自检闸门：思想纪律 + 思维强化，开工前/产出后强制逐项过单。 |

---

## 🧩 软件开发交付团队 software-dev-team（无独立 skill）

引用通用 skills/：`api-design-reviewer`、`test-case-generator-v2`、`uml-and-software-architecture-visualization`
（位置：`skills/api-design-reviewer/`、`skills/test-case-generator-v2/`、`skills/uml-and-software-architecture-visualization/`）

> 团队成员遵循「开工前 Glob 扫 `skills/` 目录」协议，命中即用、失败退回通用经验。

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
- 新增 skill → 必须在此表登记（名称/位置/一句话用途）
- 废弃 skill → 标记 `DEPRECATED`，保留 90 天
- 团队专用 skill → 仅在对应团队目录，不污染全局 `skills/`
- 总数口径：本仓库统一为 **31 个 skill**，新增/删除时同步更新顶部数字
