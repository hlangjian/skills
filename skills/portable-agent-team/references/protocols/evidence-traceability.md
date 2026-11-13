# Evidence Traceability Protocol

## 目的

让重要结论能够追溯到真实证据，让重要决策能够追溯到当时的信息，同时避免把假设、背景和推断误当成直接事实。

## 1. 分开四类认知对象

- **Unknown**：尚未解决、且可能影响行动的问题。
- **Assumption**：为了继续工作而暂时采用的未验证前提。
- **Claim**：可以判断真假、带有证据状态和适用范围的结论。
- **Decision**：基于当时信息作出的行动选择。

Unknown 不是 Claim；Assumption 被反复使用不会自动成为 Claim；Decision 的正确性需要单独评估。

## 2. 调查优先级

优先调查“不同答案会导致不同行动”的 Unknown。无论答案是什么都不改变行动的问题，通常不应优先调查。

无法解决的 Unknown 可以保留为 `deferred`，但必须记录理由和残余影响。

## 3. Claim 与证据

使用：

```yaml
id: claim-001
statement: 一个可以判断真假的结论
status: supported
scope: 结论适用范围
evidenceRefs:
  - ref: artifact-001?version=1#section=2
    relation: supports
    note: 证据具体支持了什么
  - ref: artifact-002?version=3#table=1
    relation: context
    note: 仅提供行业背景，不直接证明结论
createdAt: 时间
createdBy: researcher-01
```

`relation` 只使用：

- `supports`：支持结论；
- `contradicts`：反驳或限制结论；
- `context`：提供背景，不直接证明结论。

`Claim.status` 使用：

- `unverified`；
- `supported`；
- `disputed`；
- `refuted`；
- `superseded`。

`supported` 表示当前证据支持，不表示独立证实或永久成立。证据变化时更新状态或创建替代 Claim，保留历史。

### 推断距离示例

“三家竞争对手采用订阅收费”可以支持“该行业存在订阅模式实践”，但不能直接证明“我们的目标客户愿意购买订阅服务”。后一个 Claim 需要与目标客户相关的证据，不能把行业背景当成直接证明。

## 4. 引用要求

- 指向真实存在的 Artifact 和明确版本；
- 必要时定位章节、页码、段落、单元格或原文片段；
- 不编造引用地址、页码、行号或证据内容；
- 证据位置无法确认时，只引用能够确认的层级，并说明限制；
- 修改制品时创建新版本，避免旧 Claim 和 Decision 指向变化后的内容。

## 5. Assumption 规则

每项重要 Assumption 记录：内容、依据、影响范围、验证方式、失效条件、状态，以及使用它的 Decision。

状态为：

- `active`；
- `supported`；
- `invalidated`；
- `retired`。

`supported` 不表示已经成为事实。获得支持后，另行形成或更新带证据的 Claim。假设失效时，重新评估所有引用它的 Decision。

## 6. Decision 规则

Decision 至少记录：

```yaml
id: decision-001
choice: 作出的选择
rationale: 理由摘要
basedOn:
  claimIds: []
  assumptionIds: []
  unknownIds: []
  artifactRefs: []
revisitWhen: 会触发重新评估的新信息
status: active
supersedes: null
createdAt: 时间
createdBy: coordinator
```

`unknownIds` 表示决策时已知的残余信息缺口，不是支持决策的证据。

- `superseded`：新 Decision 替代旧 Decision，新记录的 `supersedes` 指向旧 ID。
- `reversed`：撤销原 Decision，不要求存在替代 Decision。

不得通过改写旧 Decision，让历史看起来像从未发生。
