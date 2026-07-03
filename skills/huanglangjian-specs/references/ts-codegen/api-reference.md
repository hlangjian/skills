# API reference

## `generateTsServer(options)` → `Record<string, string>`

Generates framework-agnostic server handler source files. Handlers use standard Web APIs (`Request` / `Response`).

```ts
interface TsServerOptions {
  routers: RouterModel[]
  identifier?: (id: string) => string       // default: pascalCase
  namespace?: string
  configuration?: RecordModel               // server config for env-var generation
  models?: Models[]                         // extra named models not referenced by any route
  validationLib?: "zod" | "valibot"         // default: "zod"
}
```

### Output files

| File | Content |
|---|---|
| `models.ts` | Validation schemas (Zod or Valibot) + TypeScript interfaces for all named models (including config) |
| `{group}/{id}.ts` | Per-operation: `XxxOperation` namespace (Request/Response/Handler types), schema validation, URLPattern |
| `index.ts` | `XxxHandlers` interfaces + `createXxxRouter()` factory functions per router group |
| `config.ts` | (if `configuration` provided) Schema-validated runtime config with env parameterization, union resolution |

### Handler signature

```
(request: Request, params?: Record<string, string>) => Promise<Response>
```

Satisfy this contract when wiring a generated `{ method, path, handler }` into a runtime. Pass `params` when your framework supplies path variables (e.g. Hono `c.req.param()`), or omit it to let the handler match them from the request URL. A handler with path variables returns `404` on a URL mismatch — it does not fall through. The handler validates request input and builds the `Response` internally; read the emitted file or `src/server.ts` for those specifics.

## `generateTsClient(options)` → `Record<string, string>`

Generates a zero-dependency TypeScript fetch-based client SDK.

```ts
interface TsClientOptions {
  routers: RouterModel[]
  identifier?: (id: string) => string       // default: pascalCase
  namespace?: string
  models?: Models[]
  validationLib?: "zod" | "valibot"         // default: "zod"
}
```

### Output files

| File | Content |
|---|---|
| `client.ts` | `Client` interface (`{ fetch }`), `ClientConfig` (`baseUrl`, `headers`, `fetch`), `createClient()` factory |
| `models.ts` | Validation schemas (Zod or Valibot) + TypeScript interfaces |
| `{group}/{id}.ts` | Per-operation: `XxxOperation` namespace (`Params`, `Request`, `Response` types), `getXxxUrl()` URL builder, async function taking `{ params, headers?, body?, query?, client? }` |
| `index.ts` | Re-exports operations + URL builders + `createClient`, `Client`, `ClientConfig` |

### `Client` design

`Client` has a single `fetch` method — `createClient` is a thin convenience factory. Replace or hand-write `{ fetch }` for custom behavior (retry, logging, etc.). The `client` parameter is per-request, not global state — SSR-safe and allows different clients per call.

### `createClient(config)` → `Client`

```ts
interface ClientConfig {
  baseUrl: string                                          // required
  headers?: Record<string, string>                         // static headers
           | (() => Record<string, string>                  // or dynamic (token refresh)
              | Promise<Record<string, string>>)
  fetch?: typeof globalThis.fetch                          // custom fetch implementation
}
```

The factory merges `baseUrl` + `headers` into each `fetch` call. `headers` can be a sync/async function for token refresh scenarios.

### `getXxxUrl()` naming

`get{PascalCaseOpName}Url` — e.g. `getWarehouse` → `getGetWarehouseUrl`. Usable standalone for cache keys, prefetch, batch URL construction. Path parameters are automatically `encodeURIComponent`-ed.

### `Params` type

Each operation exports a `Params` interface containing only path variables, distinct from `Request` which also carries `headers?`, `body?`, `query?`, and `client?`.

### Response discrimination

The async function returns a discriminated union named per response key. `switch (res.status)` handles all defined statuses with `as const` literals and schema-validated body, falling through to `throw new Error(...)` on undefined status codes.

### Query params

Array/set query params are serialized as repeated keys (`?k=a&k=b`).
