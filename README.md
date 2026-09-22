# opencode-expert-teams

> **4 个自包含的专家团队**，覆盖学术论文、全栈 Web、数学建模竞赛、软件开发交付四大核心场景。每个团队内含主理人 + 专家成员，内置 Workflow、门禁、Checkpoint、技能依赖，开箱即用。

## 🎯 适用场景

| 团队 | 核心场景 | 典型触发语 |
|------|----------|------------|
| **Academic Paper** | 学术论文全流程：选题→文献→设计→方法→写作→审查→投稿 | "帮我写篇论文"、"选题可行性"、"审稿回复" |
| **Fullstack Web** | Web 应用全链路交付：架构→前后端→API→DB→DevOps→测试→安全→上线 | "从零做个 Web 应用"、"重构加固"、"发布就绪" |
| **Math Modeling** | 全国大学生数学建模竞赛（CUMCM）72h 全程托管 | "国赛托管"、"建模攻坚"、"求解出图" |
| **Software Dev** | 软件开发强门禁交付：拆解→设计→实现→评审→测试 | "新功能开发"、"代码评审"、"补测试" |

## 🚀 快速开始

### 方式一：克隆后安装（推荐）
```bash
git clone https://github.com/<your-username>/opencode-expert-teams.git
cd opencode-expert-teams

# 方式 A：复制到 opencode 配置目录（仓库根即 agents 目录内容）
mkdir -p ~/.config/opencode/agents
cp -r ./* ~/.config/opencode/agents/

# 方式 B：软链接（便于更新）
ln -sfn "$(pwd)" ~/.config/opencode/agents
```

### 方式二：直接引用（开发中）
```bash
# 在 opencode 中直接使用
opencode run --agent project-director "帮我写篇论文并配套实现代码"
opencode run --agent academic-team-lead "从选题到投稿全流程"
opencode run --agent fullstack-team-lead "做个电商 Web 应用上线"
```

## 📁 仓库结构

```
opencode-expert-teams/
├── project-director.md            # 总调度：按场景路由到团队
├── SKILLS_INDEX.md                # 50+ skill 统一索引（含归属团队）
├── AGENTS.md                      # 使用手册：Workflow/协议/结构
├── LICENSE                        # MIT
└── teams/
    ├── academic-paper-team/       # 18 专家（17 academic + core-researcher）
    │   ├── agents/
    │   ├── skills/
    │   └── TEAM.md
    ├── fullstack-web-team/        # 15 专家 + 4 core 单兵
    │   ├── agents/
    │   ├── skills/
    │   └── TEAM.md
    ├── math-modeling-team/        # 9 专家（数据/文献/建模/求解/图表/写作/复现/质检+主理人）
    │   ├── agents/
    │   ├── skills/
    │   └── TEAM.md
    └── software-dev-team/         # 12 专家（架构/API/DB/前后端/DevOps/安全/测试/评审+主理人）
        ├── agents/
        ├── skills/
        └── TEAM.md
```

## ⚙️ 核心机制

- **场景路由**：`project-director` 自动识别意图 → 派发对应 Team-lead
- **Workflow 内置**：每团队 3-5 个预设 Workflow（全链路/快速/加固/单点...）
- **Phase 门禁**：前序未完成不得跳后续，主理人执行 `git tag phase-N` + `checkpoint-N.md`
- **并行显式**：Phase 注释「并行 Task 调用」，非串行假装并行
- **交接标准**：4 块模板（产出/决策/风险/重点），缺一不可
- **监测断路**：3 轮无新增=卡死，同义=死循环，自动触发降级/换人/回退
- **技能回退**：Phase 前扫 `SKILLS_INDEX.md`，调用失败自动退回通用经验，**不阻塞**

## 🛠️ 技能生态

| 团队 | 专用 Skill 示例 | 通用 Skill |
|------|----------------|------------|
| Academic | `paper-topic-selector`、`journal-adapt`、`lit-review`、`figure-maker` | `web-search`、`deep-research` |
| Fullstack | `docker-development`、`helm-chart-builder`、`github-actions-advanced`、`supabase-postgres-best-practices` | `security-scan`、`performance-profiler`、`ci-cd-pipeline-builder` |
| Math Modeling | `math-modeling-guosai`、`math-modeling-selfcheck` | `web-search`、`deep-research` |
| Software Dev | 团队内置评审/测试模板 | `test-case-generator-v2`、`api-design-reviewer` |

> 详见 [`SKILLS_INDEX.md`](SKILLS_INDEX.md)

## 📖 文档导航

| 文档 | 说明 |
|------|------|
| [`AGENTS.md`](AGENTS.md) | 总使用手册：Workflow/协议/结构/常见问题 |
| [`SKILLS_INDEX.md`](SKILLS_INDEX.md) | 技能索引：50+ skill 含归属/优先级/调用约定 |
| 各 `TEAM.md` | 团队内部：成员/Workflow/协作/技能/入口调用 |

## 🔧 维护指南

```bash
# 新增团队/成员
1. 在 teams/ 下建目录结构
2. 编写 agents/*.md（含输入规范/交接模板/监测断路）
3. 写 TEAM.md（成员表/Workflow/协作/技能/入口）
4. 更新 SKILLS_INDEX.md + AGENTS.md + project-director.md 路由表

# Skill 升级
1. 更新 SKILLS_INDEX.md 优先级/位置/适配 Agent
2. 团队 skills/ 目录下增删 skill 文件夹

# Workflow 变更
1. 同步 Team-lead 文档 Phase 定义
2. 同步 TEAM.md Workflow 对照表
```

## 📄 License

MIT License — 可自由使用、修改、分发。建议保留仓库来源引用。

---

**Enjoy expert team collaboration!** 🤝