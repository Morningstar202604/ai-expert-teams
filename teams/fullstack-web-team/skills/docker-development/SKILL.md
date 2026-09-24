---
name: docker-development
description: Dockerfile 编写与优化专用指南。当需要为 Node/Next.js、Python、Go 等服务编写或重构 Dockerfile、做镜像瘦身与多阶段构建、编写 .dockerignore、配置非 root 运行与健康检查、对接 CI 镜像扫描时，由 fullstack-devops-engineer 加载执行。
license: MIT
compatibility: opencode>=0.1
---

# Docker 开发与镜像优化

本 skill 面向 fullstack-devops-engineer，目标是产出**构建快、镜像小、可复现、安全**的容器镜像。

## 何时使用
- 新建服务需要写 Dockerfile；
- 现有镜像体积过大 / 构建慢 / 本地与线上行为不一致；
- 需要接入镜像漏洞扫描（Trivy/Grype）、SBOM、多架构构建。

## 核心原则
1. **多阶段构建**：构建依赖与运行时依赖分离，最终镜像只带运行所需。
2. **层缓存友好**：先拷依赖清单（package.json / go.mod / requirements.txt）并安装，再拷源码，让源码改动不重装依赖。
3. **最小基础镜像**：运行时用 alpine / distroless / slim，而非完整发行版。
4. **非 root 运行**：禁止以 root 跑业务进程。
5. **固定版本**：基础镜像 tag 必须带具体版本摘要或版本号，禁用 `latest`。

## 多阶段模板（Next.js / Node）
```dockerfile
# 依赖层：利用缓存
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

# 构建层
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

# 运行层
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S app && adduser -S app -G app
COPY --from=builder /app/public ./public
COPY --from=builder --chown=app:app /app/.next/standalone ./
COPY --from=builder --chown=app:app /app/.next/static ./.next/static
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

## 多阶段模板（Python FastAPI）
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
RUN useradd -m app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --chown=app:app . .
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## .dockerignore 必备清单
- `node_modules/`、`.next/`、`dist/`、`build/`（镜像内重新装/构建）
- `.git/`、`.github/`、`.vscode/`、`.idea/`
- `.env*`、`.env.local`（密钥绝不打进镜像）
- `README.md`、`*.md`、`Dockerfile`、`.dockerignore`
- `coverage/`、`.nyc_output/`、`*.log`、`npm-debug.log*`
- 操作系统杂项：`.DS_Store`、`Thumbs.db`

## 清单（交付前逐项过）
- [ ] 使用多阶段构建，最终镜像不含构建工具/源码 map。
- [ ] 基础镜像 tag 固定，无 `latest`。
- [ ] 依赖安装在源码拷贝之前，缓存命中路径正确。
- [ ] 以非 root 用户运行（`USER app`）。
- [ ] 有 `HEALTHCHECK` 或 K8s liveness/readiness 探针兜底。
- [ ] 没有把 `.env`、密钥、`.git` 打进镜像。
- [ ] `.dockerignore` 存在且覆盖上述条目。
- [ ] 镜像体积与构建时间已记录（`docker images`、`docker history`）。
- [ ] 已跑漏洞扫描（Trivy），严重/高危漏洞有处置说明。

## 易错点
- **把 `COPY . .` 放最前**：任何源码改动都触发重装依赖，缓存失效。
- **在 Node 镜像里用 root 跑**：容器逃逸风险，K8s `runAsNonRoot` 会直接拒绝。
- **Next.js 没用 standalone output**：镜像里塞进整个 `node_modules`，体积翻倍。
- **Alpine 的 musl 兼容问题**：部分原生依赖（如 sharp、某些 Python wheel）在 alpine 上要额外装 build-base，必要时改用 slim。
- **缓存挂载没用**：`RUN --mount=type=cache,target=/root/.npm` 可进一步加速 CI，注意 BuildKit 已默认开启。
- **忘记设定 `NODE_ENV=production`**：导致 React 走开发模式、体积大且慢。
