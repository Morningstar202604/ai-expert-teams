# Math Modeling Team - 数学建模竞赛专家团

> 场景：全国大学生数学建模竞赛（CUMCM/高教社杯）全程托管——从选题、建模、求解、写作到终审交付，72 小时严格节奏。

## 团队定位
- **输入**：赛题原文、数据（或无数据）、目标奖项
- **输出**：查重安全、格式合规、可冲省一/国奖的论文 PDF + 程序 + 数据
- **核心价值**：三人小组、串行闭环、主理人全程把关一致性与查重

## 成员架构（4 人）

| 角色 | Agent ID | 核心职责 | 典型触发 |
|------|----------|----------|----------|
| 竞赛总指挥 | `math-team-lead` | 选题路线、3天节奏、创新点、查重管控、终审 | 所有建模竞赛需求入口 |
| 建模专家 | `math-modeler` | 题型识别、假设与符号、主/改进模型、灵敏度设计 | "建什么模型"、"假设怎么写" |
| 算法求解师 | `math-solver` | Python/MATLAB 双栈求解、仿真、规范图表、可复现 | "代码实现"、"数值结果"、"画图" |
| 论文主笔 | `math-writer` | 国赛结构、摘要单页含数值、LaTeX、三线表、附录程序 | "写国赛论文"、"摘要单页"、"LaTeX/查重" |

## Workflow 对照

| Workflow | 触发场景 | 执行流程 |
|----------|----------|----------|
| **A 完整国赛** | "拿到赛题、要全程托管" | Phase 0→1(modeler)→2(solver)→3(writer)→4 |
| **B 单题攻坚** | "只卡在某问/某步" | 卡选题→主理人；卡建模→modeler；卡求解→solver；卡写作→writer |
| **C 赛前特训** | "还没比赛，想练真题/补短板" | 指定年份真题跑通 Phase 1→2→3，Phase 4 自查打分 |

## 关键差异（国赛 vs 美赛）
- 摘要单独成页、不要求英文摘要
- 强调现实意义与机理建模
- 程序放附录
- 查重极严、匿名评阅

## 协作机制
- **技能调用协议**：每 Phase 前必扫 `skills/`，命中即用、严格按其执行
- **思想纪律**：忠于原文、不绕圈、出错即停（2-3 轮无解即回传复核）
- **自检闸门**：`math-modeling-selfcheck` A 组开工前/B 组产出后，任一不过即停
- **一致性终审**：模型符号、求解数值、结论必须首尾一致
- **查重零容忍**：全程禁止复制往届/网文/教材

## 技能依赖
团队专用 skills 目录：`~/.workbuddy/plugins/marketplaces/my-experts/plugins/math-modeling-team/skills/`
核心 skills：`math-modeling-guosai`（资料库）、`math-modeling-selfcheck`（自检）、题型/方法/模板/查重类 skill。

## 入口调用
```bash
# 完整国赛托管
opencode agent math-team-lead "帮我全程托管这个国赛赛题"

# 单点攻坚
opencode agent math-modeler "这个题型选什么模型"
opencode agent math-solver "帮我把模型落地跑出数值和图表"
opencode agent math-writer "帮我按国赛格式写论文"
```