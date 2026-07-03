# Usage example

## Generation

```ts
import { generateTsServer, generateTsClient } from "@huanglangjian/specs-ts-codegen"
import { router } from "@huanglangjian/specs"
import type { RouterModel } from "@huanglangjian/specs"

const routers: RouterModel[] = [
  router({ id: "Warehouses", routes: { ... } }),
]

// Server
const serverFiles = generateTsServer({
  routers,
  configuration: ServerConfig,
})
// → { "models.ts": "...", "client.ts": "...", "warehouses/getWarehouse.ts": "...", "index.ts": "...", "config.ts": "..." }

// Client
const clientFiles = generateTsClient({ routers })
// → { "models.ts": "...", "client.ts": "...", "warehouses/getWarehouse.ts": "...", "index.ts": "..." }
```

## Server wiring

```ts
import { getWarehouse } from "./generated/warehouses/getWarehouse"
import { createWarehousesRouter } from "./generated"

const router = createWarehousesRouter({ getWarehouse: async ({ params }) => ({ status: 200, body: {...} }) })
// → Array<{ method, path, handler }>, wire into any framework:
// Hono: app.on(def.method, def.path, (c) => def.handler(c.req.raw, c.req.param()))
// Bun:  serve({ fetch: (req) => def.handler(req) })
```

## Client usage patterns

```ts
import { createClient, getWarehouse, getGetWarehouseUrl } from "./generated"

// 1. Minimal — no client (raw fetch + relative URL)
const r1 = await getWarehouse({ params: { id: 1 } })

// 2. Factory client (recommended)
const api = createClient({
  baseUrl: "https://api.example.com",
  headers: () => ({ Authorization: `Bearer ${getToken()}` }),
})
const r2 = await getWarehouse({ params: { id: 1 }, client: api })

// 3. Custom Client — hand-write { fetch } for retry/logging
const api: Client = { fetch: (url, init) => myRetryFetch(`${BASE}${url}`, init) }
const r3 = await getWarehouse({ params: { id: 1 }, client: api })

// 4. URL builder standalone (React Query cache key, prefetch, etc.)
const url = getGetWarehouseUrl({ id: 1 })  // → "/warehouses/1"
```
