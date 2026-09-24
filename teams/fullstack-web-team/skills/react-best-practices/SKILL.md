---
name: react-best-practices
description: React / Next.js 性能与工程模式指南。当需要优化组件渲染、使用 Server/Client Component、配置 Suspense 与代码分割、治理 re-render、优化 Next.js 图片/字体/包体积、做性能 checklist 审查时，由 fullstack-frontend-engineer 加载执行。
license: MIT
compatibility: universal
---

# React / Next.js 最佳实践

本 skill 面向 fullstack-frontend-engineer，聚焦 React 18+ 与 Next.js App Router 的性能与可维护模式。

## 何时使用
- 页面卡顿、列表滚动掉帧、客户端 bundle 过大；
- 新写组件需要判断该放 Server 还是 Client；
- 审查性能：re-render、图片、字体、第三方脚本。

## 核心原则
1. **默认 Server Component**：App Router 里组件默认在服务端渲染，只有需要交互/状态/浏览器 API 才加 `"use client"`。
2. **数据获取放服务端**：在 Server Component 直接查库/调 API，不要为了取数把整个树变成客户端。
3. **按需优化**：`useMemo`/`useCallback`/`memo` 不是越多越好，先 profile 再优化。
4. **路由级代码分割**：用 `dynamic()` 与 Suspense 隔离加载，不一次性打全量。
5. **Next 内置资源优化**：用 `next/image`、`next/font`，不要裸用 `<img>` 与系统字体。

## Server / Client 边界
- `"use client"` 标记的文件及其子树都在客户端渲染。
- 能在服务端做的：取数、访问后端资源、密钥、直接查数据库。
- 必须客户端：事件处理（onClick）、状态（useState）、effect（useEffect）、浏览器 API。
- 把"交互孤岛"尽量做小：页面外壳是 Server，只有按钮/弹窗加 client。

## 渲染优化 checklist
- [ ] 列表渲染用稳定 key（业务 id，不用 index）。
- [ ] 把状态下放到最小子树，避免顶层 state 变化重渲染整页。
- [ ] 昂贵计算用 `useMemo`，传给子组件的稳定回调用 `useCallback`，配合 `memo`。
- [ ] Context 按职责拆分，避免一个大 Context 让所有订阅者跟着无关更新重渲染。
- [ ] 大表单用受控组件库或 `useForm`，避免每次按键都重渲染整棵树。
- [ ] 第三方重组件（图表、富文本、编辑器）用 `next/dynamic` 懒加载 + `ssr:false`（如需要）。

## Next.js 专项
- **图片**：`<Image />` 自动懒加载、响应式尺寸、现代格式；固定布局写 `width/height` 或 `fill`。
- **字体**：`next/font` 自托管，避免布局偏移（CLS）。
- **脚本**：第三方脚本用 `next/script` 的 `strategy="lazyOnload"`。
- **路由缓存**：用 `loading.tsx`、`error.tsx`、Suspense 边界，给出流式加载态。
- **包体积**：`@next/bundle-analyzer` 看依赖，lodash 用按需引入，moment 换 dayjs/date-fns。

## 排查流程
1. 用 React DevTools Profiler 录一段交互，看哪些组件被重渲染、为什么。
2. 确认 props/state 变化是否必要；不必要就 memo 或下钻状态。
3. 用 Lighthouse / Web Vitals 看 LCP、INP、CLS。
4. 针对最大项优化：图片 → LCP；长任务 → 代码分割/懒加载；频繁重渲染 → memo。

## 易错点
- **整个页面加 `"use client"`**：本来能服务端渲染的内容全打到客户端，bundle 暴涨、SEO 变差。
- **滥用 `useMemo`**：每个值都包一层，反而增加比较开销；只有真正昂贵的计算才值得。
- **列表 key 用 index**：列表会增删排序时状态错位，必须用稳定业务 id。
- **`<img>` 直接用**：不压缩、不响应式、布局偏移，Lighthouse 直接扣分。
- **在 useEffect 里取数**：App Router 应在 Server Component 直接 await；客户端取数要处理 loading/错误/竞态。
- **不传 key 或传随机值**：`Math.random()` 当 key 导致每次都重挂载，性能与状态双输。
