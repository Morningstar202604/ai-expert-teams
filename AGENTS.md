# Agent 系统使用手册 - AGENTS.md

> **4 个专家团队 + 核心单兵** = 37 个 agent。按**场景**组织，每个团队自包含，不拆单兵池。

---

## 快速开始

### 1. 复杂/跨场景需求 → 找 **project-director**
> 「帮我写篇论文并配套实现代码」「做个 Web 应用还要写技术文档」
```bash
# 直接描述需求，project-director 自动路由到对应团队
```

### 2. 明确单一场景 → 直调 Team-lead
| 场景 | Team-lead | 典型触发 |
|------|-----------|----------|
| 学术论文全流程 | `academic-team-lead` | "写论文"、"投稿"、"审稿回复" |
| Web 应用全链路 | `fullstack-team-lead` | "做 Web 应用"、"上线"、"重构" |
| 数学建模竞赛 | `math-team-lead` | "国赛托管"、"建模攻坚" |
| 软件开发交付 | `software-team-lead` | "新功能开发"、"代码评审" |

### 3. 团队内部单兵 → 直调成员（仅用户明确指定）
- 学术团队：`academic-topic-strategist` / `academic-writer` / `academic-peer-reviewer` ...
- 全栈团队：`fullstack-architect` / `fullstack-frontend-engineer` / `fullstack-security-engineer` ...
- 数学建模：`math-modeler` / `math-solver` / `math-writer`
- 软件开发：`software-architect` / `software-reviewer` / `software-tester`
- 通用单兵：`core-architect` / `core-code-reviewer` / `core-security-auditor` / `core-test-engineer` / `core-researcher`

---

## 团队 Workflow 对照表

### Academic Team（学术论文）
| Workflow | 触发场景 | 执行 Phases |
|----------|----------|-------------|
| **W1 全链路** | "写完整论文"、"从选题到投稿" | 1→2→3(并行分支)→4→5→6→7→8 |
| **W2 快速选题** | "这个题行不行"、"缺什么创新" | 1 |
| **W3 稿件打磨** | "已有初稿要润色/查逻辑/出图" | 3(并行分支)→4 |
| **W4 审稿备战** | "拿到审稿意见要回复" | 7→5 |
| **W5 投稿定稿** | "投哪个刊"、"格式对不对" | 8→6 |

### Fullstack Team（全栈 Web）
| Workflow | 触发场景 | 执行 Phases |
|----------|----------|-------------|
| **W1 全链路** | "从零做个 Web 应用上线" | 1→2→3→4→5→6→7 |
| **W2 绿地脚手架** | "快速起步，先跑起来" | 1+2+3（不可跳过 Phase 2） |
| **W3 加固既有代码** | "安全/性能/质量/无障碍加固" | 5+6 |
| **W4 仅接口与数据** | "只做 API 设计 + 数据建模" | 2 |
| **W5 发布就绪** | "冲刺上线，CI/CD/部署" | 4 |

### Math Modeling Team（数学建模）
| Workflow | 触发场景 | 执行流程 |
|----------|----------|----------|
| **A 完整国赛** | "拿到赛题、要全程托管" | Phase 0→1(modeler)→2(solver)→3(writer)→4 |
| **B 单题攻坚** | "只卡在某问/某步" | 卡选题→主理人；卡建模→modeler；卡求解→solver；卡写作→writer |
| **C 赛前特训** | "练真题/补短板" | 指定年份真题跑通 1→2→3，4 自查打分 |

### Software Dev Team（软件开发）
| Workflow | 触发场景 | 执行流程 |
|----------|----------|----------|
| **W1 全流程** | "新功能从零到交付" | 拆解 → 设计 → 实现 → 评审 → 测试 → 交付 |
| **W2 仅设计** | "只出架构方案/接口契约" | 拆解 → 设计（ADR + 接口契约） |
| **W3 仅评审+测试** | "对现有代码跑门禁" | 评审 → 测试 |

---

## 交互协议（必读）

### 输入规范
- Team-lead 派发成员时，自动传递 `checkpoint-N.md` + 上阶段完整产出
- 成员声明 `## 输入规范`，说明接收什么格式/字段
- 用户直调成员时，需自备上一阶段产出或告知「无前序」

### 交接模板（4 块，缺一不可）
1. **阶段产出** —— 完整原文/代码/报告
2. **关键决策** —— 3 条，含取舍理由/代价
3. **遗留风险** —— H/M/L 分级 + 是否需下一环节兜住
4. **给下一阶段** —— 3 个重点，明确交接什么、别漏什么

### 监测与断路
- **停滞**：产出为空/重复/无关
- **死循环**：连续 2 次同义反复
- **卡死**：连续 **3 轮对话无实质新增**
- 触发 → 立即报告卡点 → 断路切换（换成员/降级 Workflow/拆任务/回退 checkpoint/请用户决策）

### 技能调用
- Phase 开工前扫描 `SKILLS_INDEX.md`，关键词匹配 + `team_context`
- **调用失败/未安装 → 退回通用经验，不阻塞**
- Team-lead 可指定优先 skill，成员必须遵守

---

## 文件结构

```
.config/opencode/agents/
├── project-director.md          # 总调度入口
├── SKILLS_INDEX.md              # 技能索引（含归属团队）
├── AGENTS.md                    # 本文档
├── teams/
│   ├── academic-paper-team/
│   │   ├── agents/ (17+1)       # team-lead + 16 专家 + 1 core
│   │   ├── skills/              # 团队专用 skill
│   │   └── TEAM.md              # 团队说明
│   ├── fullstack-web-team/
│   │   ├── agents/ (15+5)       # team-lead + 14 专家 + 5 core
│   │   ├── skills/
│   │   └── TEAM.md
│   ├── math-modeling-team/
│   │   ├── agents/ (4)          # team-lead + 3 专家
│   │   ├── skills/
│   │   └── TEAM.md
│   └── software-dev-team/
│       ├── agents/ (4)          # team-lead + 3 专家
│       ├── skills/
│       └── TEAM.md
```

---

## 常见问题

| 问题 | 解决 |
|------|------|
| 需求同时涉及论文+代码 | 找 `project-director`，并行派发两团队 |
| 想跳过某 Phase | 告知 Team-lead，需用户确认裁剪 |
| 成员卡死/死循环 | Team-lead 自动触发断路，汇报给用户 |
| Skill 未安装 | 自动回退通用经验，日志记录 fallback |
| 想用特定 skill | 在需求中指定「优先用 xxx skill」 |
| 需要回滚 | Team-lead 执行 `git tag phase-N` + `checkpoint-N.md`，按记录回退 |
| 版本追踪 | 每 Phase 结束自动写入 `versions.md` |

---

## 维护清单

- [ ] 新增团队/成员 → 更新 `SKILLS_INDEX.md` + `AGENTS.md` + 对应 `TEAM.md`
- [ ] Skill 版本升级 → 更新 `SKILLS_INDEX.md` 优先级/位置
- [ ] Workflow 变更 → 同步更新 Team-lead 文档 + `TEAM.md`
- [ ] 核心单兵能力变更 → 同步更新 `project-director` 路由表