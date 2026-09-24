---
name: api-design-reviewer
description: REST/GraphQL 接口契约设计评审专用。当 software-api-designer 产出 API spec、或 software-reviewer 在门禁阶段审查接口正确性/一致性/安全时调用。覆盖资源建模、命名、HTTP 语义、状态码、错误模型、分页过滤、版本演进、GraphQL Schema 设计与 N+1/鉴权风险，输出可勾选评审清单与驳回项。
license: MIT
compatibility: opencode>=0.1
---

# API 设计评审（REST / GraphQL）

本 skill 供 **software-api-designer** 自审与 **software-reviewer** 门禁评审共用。目标是在写代码前把接口契约钉死：资源边界清晰、HTTP/GraphQL 语义正确、错误模型统一、鉴权与版本策略明确，避免实现阶段反复返工。

## 这是什么
一份可直接照单勾选的接口评审规程。它不替代架构师的模块划分，只对「对外暴露的契约」做正确性、一致性、安全性把关。REST 与 GraphQL 两套检查项分列，按需取用。

## 何时使用
- software-api-designer 写完 OpenAPI / Schema 草稿，准备交接实现前。
- software-reviewer 在门禁阶段看到 PR 改动了路由、Schema、错误码或鉴权逻辑。
- 跨团队对齐接口、或评审一份第三方 API 对接方案。

## 核心步骤
1. **先定资源再定动作**：列出本次涉及的实体（资源）、它们之间的关系（1:1 / 1:N / N:M），确认每个资源有明确命名与生命周期。
2. **REST 检查**：用名词复数建模集合，用嵌套表达从属；动作通过 HTTP 方法表达而非塞进 URL。
3. **GraphQL 检查**：核对 Query/Mutation 边界、类型 nullable、输入用 `input` 类型、分页用 connection/edges 或游标。
4. **错误模型统一**：所有失败返回同一结构（code / message / trace_id / details），不靠 200 包业务错误。
5. **鉴权与版本**：逐端点标注谁能调、需要什么 scope；破坏性变更走版本号或 deprecation 头。
6. **输出评审结论**：按 critical / major / minor 分级，每条给「问题—依据—建议改法」。

## REST 评审清单
- [ ] URL 为名词复数（`/orders`），动词在方法（GET/POST/PUT/PATCH/DELETE），未出现 `/getOrder` `/createUser`。
- [ ] 状态码语义正确：201 创建、204 删除成功、400 参数错、401 未认证、403 无权限、404 不存在、409 冲突、422 语义校验失败、429 限流、500 服务端错。
- [ ] 列表接口有分页（`page/cursor` + `size/limit`）、总数估算、排序参数，且默认排序稳定可复现。
- [ ] 过滤/字段裁剪/扩展通过查询参数，未把动态条件堆进路径段。
- [ ] 创建返回 201 且 `Location` 头指向新资源；幂等写操作（PUT）可安全重试。
- [ ] 时间统一 ISO-8601 UTC，金额用最小单位整数或明确精度，枚举固定取值集。
- [ ] 敏感字段（密码、手机号、内部 ID）不出现在响应里；错误信息不泄露堆栈/SQL。

## GraphQL 评审清单
- [ ] Query 只读、无副作用；写操作走 Mutation；订阅走 Subscription。
- [ ] 避免 N+1：列表字段有数据加载器（dataloader）或批量解析，N+1 已压成 O(1)~O(logN)。
- [ ] 每个字段/类型标注鉴权指令（`@auth`/`@hasRole`），敏感节点在解析层二次校验。
- [ ] 分页用游标或 connection，禁止无上限的 `allUsers` 这类全量字段；设最大复杂度/深度上限。
- [ ] 输入用 `input` 类型，错误放进 `errors` 或领域错误联合类型，不吞成 null。
- [ ] Schema 有变更演进策略（废弃字段标 `@deprecated`，不直接删）。

## 错误与安全模板
```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "订单不存在或无权访问",
    "trace_id": "req-7f3a...",
    "details": { "order_id": "88421" }
  }
}
```
- 鉴权失败一律 401/403，不透露「用户存在但密码错」这类枚举信息。
- 批量/导入接口必须设条数上限与幂等键，防止重放与放大。

## 易错点
- **把 CRUD 当 RPC**：在 URL 里塞动词（`/api/doLogin`），导致无法缓存、无法复用 HTTP 语义。
- **200 包错误**：HTTP 200 但 body 里 `success:false`，网关/监控无法按状态码告警。
- **分页漏总数/漏稳定排序**：翻页时数据漂移、重复或丢失。
- **GraphQL 不设深度/复杂度上限**：一个恶意深嵌套查询打垮服务。
- **破坏性改动直接上线**：未走版本/废弃周期，老客户端全挂。
- **评审只看风格不看契约**：本 skill 只评正确性/一致性/安全，命名风格偏好不作为驳回理由。
