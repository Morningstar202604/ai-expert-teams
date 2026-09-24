---
name: terraform-patterns
description: Terraform IaC 编写规范与安全实践。当需要组织 Terraform 模块、配置远程状态与状态锁、管理多环境工作区、编写变量/输出、做 plan 审查、最小权限与 state 安全时，由 fullstack-devops-engineer 加载执行。
license: MIT
compatibility: opencode>=0.1
---

# Terraform 模式与安全

本 skill 面向 fullstack-devops-engineer，产出**可复用、状态安全、可审计**的基础设施即代码。

## 何时使用
- 新建云资源（VPC、GKE/EKS、RDS、CDN、DNS）需要 Terraform 落地；
- 现有 TF 代码要抽模块、接远程状态、做多环境；
- 审查 plan、排查 state 漂移、治理密钥与权限。

## 核心原则
1. **状态远程化 + 锁**：禁止本地 state，S3/GCS 后端 + DynamoDB 锁。
2. **模块分层**：可复用资源抽 module，环境只做组合与变量覆盖。
3. **显式而非隐式**：版本约束、provider 版本、region 全部显式声明。
4. **最小权限**：IAM 按资源粒度授权，不用 `*`。
5. **plan 必审**：CI 里 `plan` 输出留档，人工/自动审批后再 `apply`。

## 远程状态后端模板
```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    bucket         = "myorg-tfstate-prod"
    key            = "services/webapp/terraform.tfstate"
    region         = "ap-northeast-1"
    dynamodb_table = "myorg-tfstate-locks"
    encrypt        = true
  }
}
```

## 模块目录结构
```
modules/
├── network/        # vpc/subnet/security_group
├── eks/            # cluster/node_pool
└── rds/            # instance/参数/备份
envs/
├── dev/            # main.tf 调模块 + terraform.tfvars
├── staging/
└── prod/
```

## 变量与输出规范
- 所有变量声明类型（`string`/`number`/list/map），必填变量**不设默认值**。
- 敏感变量加 `sensitive = true`（如 db 密码、API key）。
- 输出只暴露必要值，敏感输出同样标 `sensitive`。
- 用 `*.tfvars` 分环境，不把生产值写进 `variables.tf` 默认值。

## 标准工作流
1. `terraform fmt -recursive` 统一格式。
2. `terraform init -backend=false`（本地校验）/ `terraform init`。
3. `terraform validate` 语法校验。
4. `terraform plan -out=tfplan` 留档。
5. 评审通过后 `terraform apply tfplan`。
6. 禁止 `terraform apply -auto-approve` 直接上生产。

## 清单（交付前逐项过）
- [ ] 后端远程化，state 加密 + 锁表，state 文件不入库（`.gitignore` 含 `*.tfstate*`、`.terraform/`）。
- [ ] provider 与 terraform 版本都有 `required_version` / `required_providers` 约束。
- [ ] 资源抽成模块，环境目录只组合、不重复造轮子。
- [ ] IAM 策略无 `*` 通配，按资源 ARN 最小授权。
- [ ] 敏感值用 secret 管理（SSM/Secrets Manager/Vault），不硬编码、不进 state 明文。
- [ ] `terraform fmt` / `validate` / `plan` 在 CI 全绿。
- [ ] 生产 apply 有人工审批或环境保护。
- [ ] 标签规范（team/owner/env/cost-center）统一打。
- [ ] 破坏性操作（`ForceNew`、删除资源）在 plan 里已人工确认。

## 易错点
- **本地 state 提交进 Git**：state 里常含密钥，泄露即事故；后端必须先配好再 init。
- **手改控制台资源**：造成 state 漂移，下次 plan 会被覆盖；改资源一律走 TF。
- **`default` 变量塞生产值**：dev 不小心 apply 就用了生产配置，默认值要保守。
- **循环依赖**：模块间互相引用输出，`terraform init` 报 cycle，拆接口或用 data source。
- **忘记 `terraform init -upgrade`**：provider 版本漂移导致团队间 plan 不一致。
- **state 锁没配**：多人同时 apply 会损坏 state，DynamoDB 锁表必须建。
