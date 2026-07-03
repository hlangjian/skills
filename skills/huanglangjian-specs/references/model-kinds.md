# Model kinds

Every model is a plain object with a `kind` discriminator. All models support optional `title`, `description`, `examples`, and `schema` (a [StandardSchema](https://standardschema.dev/) validator for runtime type inference).

Use the factory (left column). The right column shows generated output — do not write it directly.

| Kind | Factory | OpenAPI / JSON Schema mapping |
|---|---|---|
| `int32` | `int32(opts?)` | `type: "integer", format: "int32"` |
| `float32` | `float32(opts?)` | `type: "number", format: "float"` |
| `float64` | `float64(opts?)` | `type: "number", format: "float"` |
| `boolean` | `boolean(opts?)` | `type: "boolean"` |
| `string` | `string(opts?)` | `type: "string"` |
| `datetime` | `datetime(opts?)` | `type: "string", format: "date-time"` |
| `date` | `date(opts?)` | `type: "string", format: "date"` |
| `duration` | `duration(opts?)` | `type: "string", format: "duration"` |
| `uuid` | `uuid(opts?)` | `type: "string", format: "uuid"` |
| `literal` | `literal(value)` | `const: value` |
| `null` | `nullLike()` | `type: "null"` |
| `array` | `array({ base: T, ... })` | `type: "array", items: T` |
| `set` | `set({ base: T, ... })` | `type: "array", uniqueItems: true` |
| `map` | `map({ base: T, ... })` | `type: "object", additionalProperties: T` |
| `record` | `record({ id, properties, optional?, ... })` | `type: "object"` with `$ref` to named schema |
| `enums` | `enums({ id, variants: {...}, ... })` | `type: "string", enum: [...]` |
| `union` | `union({ id, discriminator?, variants, ... })` | `oneOf` with discriminator auto-injected into variant schemas |
| `rpc` | `rpc({ parameters, results })` | (service definition only, used by codegen) |
| `unknown` | `unknown(opts?)` | `{}` (matches any value) |

## Key rules

- `record`, `enums`, `union` **require an `id`** — they become named schemas.
- `union` uses `discriminator` (defaults to `"type"`, optional) to specify which field acts as the discriminator. The `literal(value)` matching each variant key is auto-injected at type/JSON Schema/codegen layers — variants only declare business fields. If `discriminator` conflicts with an existing variant property, a runtime error is thrown.
- `set` generates `uniqueItems: true` in JSON Schema.
