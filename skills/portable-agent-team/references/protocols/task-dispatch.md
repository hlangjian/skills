# Task Dispatch Protocol

## 目的

把任务创建、执行提交、独立验收和返工分开，避免“已经执行”被误当成“已经合格”。

## 1. 创建任务单

Secretary 独占 Agent 实例分配权。Coordinator 规划和记录 Task，在已分配的实例之间协调工作；需要新实例时向 Secretary 提交角色、任务和理由，不自行创建或改派 Agent。任务单中的 `assignee` 必须与 Secretary 的实际分配一致。

Coordinator 为每项 Task 记录：

```yaml
id: task-001
goal: 要回答的问题或要完成的工作
type: investigate
assignee: researcher-01
inputRefs:
  - artifact-000?version=1
deliverableSpec: 交付物形式和内容要求
evidenceRequirements: 必须提供的证据
acceptanceCriteria:
  - 可检查的验收条件
status: pending
resultArtifactIds: []
parentTaskId: null
triggerReviewId: null
createdAt: 时间
createdBy: coordinator
```

只提供 Executor 需要的上下文。任务目标、输入、证据和验收标准不清时，先由 Coordinator 澄清，不让 Executor 猜测项目意图。

## 2. 执行状态

使用以下状态：

- `pending → in_progress → done`；
- `in_progress → blocked → pending | in_progress`；
- 尚未完成的任务可以进入 `cancelled`。

状态只描述执行进度，不表示验收结论。

## 3. 提交结果

Executor 提交结果单和制品，并将 Task 提交为 `done`。结果单至少包含：

- 结果摘要；
- 制品与证据引用；
- 已执行的验证；
- 偏差；
- 剩余未知；
- 需要 Coordinator 处理的问题。

Executor 不直接修改全局项目状态。Coordinator 校验提交后，作为唯一写入者更新状态。

## 4. 关联评审

- 任务级评审使用可选的 `Review.targetTaskId` 直接指向对应 Task。
- `Task.resultArtifactIds` 指向本次提交制品。
- `Review.targetRefs` 指向实际评审的制品及版本。
- `targetTaskId` 与共同的制品引用一起明确执行、提交和评审关系；一个任务可以有多次评审。
- 项目级或跨任务评审可以不填写 `targetTaskId`，不能为了满足字段形式而错误归属到单个 Task。
- 验收结论以与具体提交制品关联的 Review 为准，不以 Executor 的自我声明为准。
- 不通过“最新文件”或“最后一次对话”猜测评审对象，必须使用明确版本引用。

## 5. 验收结论

- `pass`：通过；
- `conditional_pass`：有附加条件和责任人，未核实前不等于完全通过；
- `changes_required`：需要修改。

原 Review 不修改。需要复审时创建新 Review，并引用新制品版本。条件满足后需要转为最终通过时，以新的 Review 或设计明确要求的核实记录为准，不倒写历史。

## 6. 返工

原 Task 提交后保持 `done`。评审要求修改时，Coordinator 创建新的修正 Task：

```yaml
id: task-002
goal: 修正 review-001 指出的问题
type: correction
parentTaskId: task-001
triggerReviewId: review-001
inputRefs:
  - artifact-001?version=1
  - review-001
status: pending
```

正常迭代与因缺陷、误解或验收失败产生的修正 Task 必须区分。不要通过把原 Task 在 `done` 与 `in_progress` 之间反复切换来抹除历史。

## 7. 单写者与降级

- Native Multi-Agent：Coordinator 串行写入共享状态，Executor 和 Reviewer 只提交结果。
- Sequential Fallback：只有 Coordinator 角色阶段更新全局状态；其他阶段只生成结果记录。
- 出现多个实际写入进程时，先使用串行写入或版本检查；没有保护就不能声称支持并发状态更新。
