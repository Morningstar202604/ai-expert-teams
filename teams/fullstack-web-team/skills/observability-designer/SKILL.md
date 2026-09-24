---
name: observability-designer
description: 可观测性体系设计指南。当需要为服务规划 metrics/logs/traces、定义 RED/USE 指标、设计仪表盘与告警、接入 OpenTelemetry、做健康检查与关键路径埋点时，由 fullstack-devops-engineer 加载执行。
license: MIT
compatibility: opencode>=0.1
---

# 可观测性设计

本 skill 面向 fullstack-devops-engineer，目标是让系统出问题时**能快速定位、能被用户感知到前发现**。

## 何时使用
- 新服务上线前要接监控/日志/链路追踪；
- 故障后复盘发现"看不见、查不到"；
- 设计仪表盘、告警规则、埋点方案。

## 三大支柱
1. **Metrics（指标）**：聚合数值，看趋势、配告警，低成本高覆盖。
2. **Logs（日志）**：离散事件，排查细节，结构化输出。
3. **Traces（链路）**：单次请求跨服务调用链，定位慢在哪一跳。
统一用 OpenTelemetry 埋点，后端可接 Prometheus/Grafana、Loki、Tempo/Jaeger。

## RED 方法（请求类服务）
- **Rate**：每秒请求数（QPS/RPM）。
- **Errors**：失败请求数/比例。
- **Duration**：请求延迟分布（p50/p95/p99），不只看平均值。

## USE 方法（资源类，如 DB/CPU）
- **Utilization**：利用率（CPU/内存/磁盘/连接池占用）。
- **Saturation**：饱和度（队列长度、等待时间）。
- **Errors**：错误计数（OOM、连接拒绝、慢查询数）。

## 必埋的黄金指标
- HTTP：`http_requests_total{route,method,status}`、`http_request_duration_seconds` 直方图。
- 业务：关键业务事件下单/支付成功量与失败量（**业务指标比技术指标更能反映用户受影响面**）。
- 依赖：DB 连接池使用率、外部 API 调用耗时与错误率。
- 容器：CPU/内存/重启次数/OOMKill。

## 结构化日志
- 每行 JSON，必带字段：`ts`、`level`、`service`、`trace_id`、`span_id`、`user_id`(脱敏)、`route`、`error`。
- 错误日志带 stack trace，不打印整个请求体（PII）。
- 日志级别分级：`debug`/`info`/`warn`/`error`，生产默认 info。

## 告警设计原则
- **告警"症状"而非"原因"**：告"用户看到 500 增多/延迟升高"，而不是"某台机器 CPU 高"。
- **少而精**：告警必须有人行动，告了没人理=没告。
- **分级**：Critical（立即响应）/ Warning（工作时间处理）/ Info（仅记录）。
- 每个告警带 runbook 链接：现象、影响、排查步骤、值班人。

## 清单（交付前逐项过）
- [ ] 服务暴露 `/health/live` 与 `/health/ready`（不含敏感信息）。
- [ ] RED 三指标已埋，延迟看 p95/p99 而非平均。
- [ ] 日志结构化、带 trace_id，可与 trace 串起来。
- [ ] 关键业务事件有业务指标。
- [ ] 仪表盘分层：高层（用户体验 SLO）+ 排障（服务/依赖下钻）。
- [ ] 每个告警有 runbook、有值班人、已分级。
- [ ] 外部依赖（DB/缓存/支付）的错误与延迟有监控。
- [ ] 重启/OOM/崩溃有告警。
- [ ] 告警经过演练，确认误报率可接受。

## 易错点
- **只看平均值**：平均延迟 200ms 可能掩盖 1% 请求 5s，必须看分位数。
- **告警风暴**：一个故障触发几十条告警，值班人麻木；做聚合与依赖抑制。
- **日志打印敏感信息**：手机号/身份证/卡号明文进日志，合规事故；脱敏。
- **健康检查做重了**：readiness 里连了 DB/外部 API，外部一抖就全量重启，探针要轻、要分层。
- **没 trace_id 贯穿**：跨服务请求查不到关联，日志像散沙；OTel 上下文必须透传。
- **指标维度爆炸**：label 里塞 user_id/order_id，时间序列数量爆炸，后端直接崩。
