---
name: helm-chart-builder
description: Kubernetes Helm Chart 生成与规范化指南。当需要为服务编写/重构 Helm Chart、组织 values 与模板、配置 Ingress、探针、资源限制、HPA、Secret 与 ConfigMap、做 Chart 版本化与 lint 时，由 fullstack-devops-engineer 加载执行。
license: MIT
compatibility: opencode>=0.1
---

# Helm Chart 构建规范

本 skill 面向 fullstack-devops-engineer，产出可复用、可参数化、可 lint 通过的 Helm Chart。

## 何时使用
- 新服务要在 K8s 部署，需要从 0 写 Chart；
- 已有 Deployment YAML 要抽成模板化 Chart；
- 多环境（dev/staging/prod）通过 values 覆盖差异。

## 标准目录结构
```
charts/myapp/
├── Chart.yaml          # apiVersion、name、version、appVersion
├── values.yaml         # 默认值（生产兜底，最小权限/最小副本）
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl    # 命名/标签/选择器 helper
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── NOTES.txt
└── templates/tests/
    └── test-connection.yaml
```

## 核心约定
- **命名**：一律用 `_helpers.tpl` 里的 `include "myapp.fullname" .`，禁止散落硬编码名字。
- **标签**：统一打 `app.kubernetes.io/name/instance/version/managed-by`，选择器与 label 解耦。
- **values 默认偏安全**：默认副本数 1、资源 request/limit 都给、探针都配，环境 values 只做覆盖。
- **Secret 不入库**：Chart 里只放模板，真实值由外部 Secret（ExternalSecrets / sealed-secrets / CI 注入）填充。

## Deployment 模板要点
```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "myapp.name" . }}
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          readinessProbe:
            httpGet: { path: /health/ready, port: http }
            initialDelaySeconds: 5
          livenessProbe:
            httpGet: { path: /health/live, port: http }
            periodSeconds: 30
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          envFrom:
            - configMapRef: { name: {{ include "myapp.fullname" . }} }
```

## Ingress 模板要点
- 用 `{{- if .Values.ingress.enabled }}` 包裹。
- host、className、annotations（TLS 签发、限流、CORS）全部走 values。
- TLS secretName 必须在 values 显式声明，不要生成随机名。

## 清单（交付前逐项过）
- [ ] `Chart.yaml` 的 `version`（Chart 版本）与 `appVersion`（应用版本）分开维护。
- [ ] `helm lint .` 零 warning；`helm template . --set env=prod` 渲染干净。
- [ ] 所有命名/标签都走 helper，无硬编码字符串拼接。
- [ ] 容器设了 `securityContext.runAsNonRoot` 与资源 request/limit。
- [ ] liveness 与 readiness 探针分开，readiness 不依赖重启动作。
- [ ] Secret 值不入库，模板用 `{{- if .Values.secrets }}` 守卫。
- [ ] HPA（如需要）按 CPU/自定义指标伸缩，且设了 min/max。
- [ ] 提供了 `values-dev.yaml` 与 `values-prod.yaml` 示例。
- [ ] `NOTES.txt` 打印访问方式与下一步命令。

## 易错点
- **改了 selector 标签**：Helm 不会自动改 Deployment selector，会导致滚动更新失败，selector 一旦发布就别再动。
- **`{{ }}` 与 `{{- -}}` 横线方向错**：多空格/少空格导致渲染 YAML 缩进错乱，用 `helm template` 验证。
- **把大段配置写死在模板**：所有环境差异必须进 values，否则 Chart 不可复用。
- **镜像 tag 用 `latest`**：Helm 升级不会拉新镜像，必须用不可变 tag（git sha）。
- **忘记 `helm dependency update`**：子 Chart 没拉下来，CI 渲染失败。
- **探针路径与应用不匹配**：readiness 打到需要鉴权的接口，永远 NotReady，Pod 起不来。
