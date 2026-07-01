# Config 模型定义与 JSON Schema 生成

## 核心概念

Config 模型是 **解析后模型**，不是输入模型。用户定义 config 时，所有有 `default` 的字段在解析后一定会有值，因此不应出现在 `optional` 数组中。

## 规则

1. **定义 config 用 `record()`，`optional` 填写规则：**
   - 有 `default` → **不放入** `optional`（解析后一定有值）
   - 无 `default` 且允许不传 → **放入** `optional`
   - 无 `default` 且必须传 → **不放入** `optional`

2. **生成 JSON Schema 时：**
   - 必须用 `generateConfigJsonSchema()`，**禁止** 用 `generateJsonSchema()`
   - `generateConfigJsonSchema()` 自动将有 `default` 的字段标记为 optional（反映输入格式）
   - `generateJsonSchema()` 按原样生成，有 `default` 的字段会被错误标记为 required

## 正确写法

```ts
const ServerConfig = record({
  id: "ServerConfig",
  properties: {
    port: int32({ description: "端口", default: 8080 }),
    host: string({ description: "地址", default: "0.0.0.0" }),
    tags: array({ base: string() }),
    name: string(),
  },
  optional: ["tags"],
})

import { generateConfigJsonSchema } from "@huanglangjian/specs"
const schema = generateConfigJsonSchema(ServerConfig)
```

## 常见错误

```ts
// ❌ 把有 default 的字段放入 optional
// 会导致生成的 TS 类型错误标记为 string?
const MyConfig = record({
  id: "MyConfig",
  properties: {
    url: string({ default: "http://localhost" }),
  },
  optional: ["url"], // ← 不要这样做
})

// ❌ 用 generateJsonSchema 生成 config 的 JSON Schema
const schema = generateJsonSchema(ServerConfig) // ← 应使用 generateConfigJsonSchema
```

## `generateConfigJsonSchema` 行为

- 自动把解析后模型转为输入模型（有 `default` 的字段变为 optional）
- 递归处理嵌套的 `record`、`taggedUnion`、`union`
- 对于 `array`/`set`/`map`，仅当 `base` 是带 `id` 的复杂模型时才递归
- 同一模型引用多次时通过缓存去重（避免重复 `$defs`）
- 所有复杂模型的 `id` 保持不变
- 签名与 `generateJsonSchema` 一致，支持 `{ toJsonSchema }` 回调
