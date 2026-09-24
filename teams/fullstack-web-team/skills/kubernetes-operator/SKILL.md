---
name: kubernetes-operator
description: Kubernetes Operator / CRD 开发指南。当需要定义 CRD 类型、基于 controller-runtime 写调和循环(Reconcile)、设计 finalizer 与 status conditions、配置 RBAC 与 Watches、做 Leader 选举与优雅终止时，由 fullstack-devops-engineer 加载执行。
license: MIT
compatibility: opencode>=0.1
---

# Kubernetes Operator 开发

本 skill 面向 fullstack-devops-engineer，规范基于 controller-runtime 的 Operator 开发。

## 何时使用
- 把领域运维知识自动化成 CRD（如自定义数据库/中间件/部署单元）；
- 已有脚本运维流程要收敛成声明式 API；
- 设计 Reconcile 循环、finalizer、状态上报。

## 核心思想
- **声明式 + 调和（Reconcile）**：用户声明期望状态（CR），Controller 不断对比实际与期望，收敛到一致。
- **幂等**：Reconcile 可被任意触发多次，结果一致，绝不依赖调用次数。
- **事件驱动**：Watch 相关资源变化入队，不轮询。

## CRD 设计要点
- 用 Kubebuilder / operator-sdk 脚手架：`kubebuilder init` + `create api`。
- Spec 是**期望状态**，Status 是**观测到的现实状态**，二者分开。
- Status 用 `conditions`（Available/Progressing/Degraded）+ `observedGeneration` 反映是否已处理最新 spec。
- 字段加 `// +kubebuilder:validation:Minimum` 等约束，OpenAPI schema 校验在服务端。

## Reconcile 模板要点
```go
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
  var app examplev1.MyApp
  if err := r.Get(ctx, req.NamespacedName, &app); err != nil {
    return ctrl.Result{}, client.IgnoreNotFound(err)
  }
  // 1. 处理删除（finalizer）
  if !app.DeletionTimestamp.IsZero() { /* 清理外部资源 */ return r.finalize(ctx, &app) }
  // 2. 确保 finalizer 存在
  // 3. 创建/更新依赖资源（Deployment/Service/...）
  // 4. 聚合状态写回 Status().Conditions
  // 5. 如需后续对账，return ctrl.Result{RequeueAfter: time.Minute}
}
```

## 关键机制
- **Finalizer**：删除 CR 前先清理外部资源（云数据库、DNS），否则资源泄漏。清理完再删 finalizer。
- **Watches**：除了 watch 自己的 CR，还要 watch 创建出来的子资源（用 `Owns(&appsv1.Deployment{})`），子资源变了触发调和。
- **RBAC**：用 `// +kubebuilder:rbac:` 注解生成，controller-runtime 会据注解生成 RBAC YAML。
- **Leader 选举**：多副本高可用时启用 `manager.Options{LeaderElection: true}`，只有主实例调和。

## 清单（交付前逐项过）
- [ ] Spec 与 Status 分离，Status 带 conditions 与 observedGeneration。
- [ ] Reconcile 幂等，可重复执行无副作用。
- [ ] 删除路径有 finalizer 清理外部资源，不泄漏云资源。
- [ ] Watch 覆盖子资源变更，子资源漂移能被收敛。
- [ ] RBAC 按注解生成，最小权限（不发明唯一需要的 verbs）。
- [ ] 启用 Leader 选举，多副本安全。
- [ ] 关键步骤有结构化日志与 metrics（reconcile 次数/耗时/失败）。
- [ ] CRD 有 `additionalPrinterColumns`，`kubectl get` 能看到关键状态。
- [ ] 错误处理：可重试错误 requeue，永久错误记 condition 不无限重试。

## 易错点
- **Reconcile 里做长时间阻塞操作**：阻塞会占住 worker、延迟其他调和；长任务异步化或设短超时+requeue。
- **忽略 NotFound**：CR 被删后 Get 返回 NotFound 会一直报错重 queue，必须 `client.IgnoreNotFound`。
- **不写 Status**：用户 `kubectl describe` 看不到任何进展，像卡死了；务必回写 conditions。
- **Finalizer 忘清理**：外部资源删了但 CR 永远 Terminating；清理成功后一定要把 finalizer 从列表移除。
- **RBAC 给过宽**：Operator 一旦被攻破就是集群级权限，按资源粒度授权。
- **Watch 不全**：只 watch CR，子 Deployment 被人手动改坏后无人收敛；用 Owns 补全。
- **不设 Requeue 边界**：外部依赖没就绪就疯狂高频重试，打垮下游；用指数退避或固定间隔。
