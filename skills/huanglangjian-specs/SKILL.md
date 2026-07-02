---
name: huanglangjian-specs
description: "Typed models, routes, and security; OpenAPI 3.2 & JSON Schema 2020-12 generation; TypeScript server stubs and fetch-based client SDKs. Use when declaring typed request/response models, building a router, emitting OpenAPI or JSON Schema, scaffolding server handlers, generating a typed fetch client, producing config.ts env-var parsing, or writing field titles/descriptions."
---

# @huanglangjian/specs

## Workflow

1. Check [Model kinds](./references/model-kinds.md) for available types and factory signatures.
2. Define data models with factory functions (`record`, `enums`, `union`, etc.).
3. Group routes with `router({ id, routes, tag?, basePath?, description? })`.
4. Call `generateOpenapi()`, `generateJsonSchema()`, or `generateConfigJsonSchema()` to produce output.
5. Call `generateTsServer({ routers, configuration?, validationLib? })` for server stubs.
6. Call `generateTsClient({ routers, validationLib? })` for client SDK.

## Key constraints

- `record`, `enums`, `union` must have an `id` — they become named schemas.
- `router` generates an OpenAPI tag from `tag ?? id`. Do NOT set `tags` on individual routes unless extra tags are needed.
- Never write raw `{ kind: "..." }` objects — always use factory functions.
- For config model JSON Schema, use `generateConfigJsonSchema()`, **not** `generateJsonSchema()`. Fields with `default` must not appear in `optional` — see [Config models](./references/config-models.md).
- Handler signature: `(request: Request, params?: Record<string, string>) => Promise<Response>`.
- `configuration` generates `config.ts` with env-var schema parsing. Extra named models not referenced by routes: pass via `models` option.

## References

- [Model kinds](./references/model-kinds.md)
- [API reference](./references/api-reference.md)
- [Security](./references/security.md)
- [Usage example](./references/usage-example.md)
- [Init guide](./references/init-guide.md)
- [Patterns & best practices](./references/patterns.md)
- [Writing guide](./references/writing-guide.md)
- [Source map](./references/source-map.md)
- [Config models](./references/config-models.md)
- [TS codegen: API reference](./references/ts-codegen/api-reference.md)
- [TS codegen: Usage example](./references/ts-codegen/usage-example.md)
- [TS codegen: Patterns](./references/ts-codegen/patterns.md)
- [TS codegen: Source map](./references/ts-codegen/source-map.md)
