# Independent Review Protocol

## 目的

让评审真正挑战结论，而不是重复执行者总结。Reviewer 是横向质量机制，可以由独立 Agent、独立模型调用或人类承担，不构成第四个行政层级。

## 1. 何时使用

关键交付物、高影响结论或存在实质争议时安排独立评审。简单、低风险任务不必全部经过独立评审。

Coordinator 负责集成和项目级验收；Reviewer 负责独立挑战；自动化检查负责可机械验证的标准。三者不能互相替代。

## 2. 独立性要求

Nested Native Multi-Agent 中，最终独立 Reviewer 由 Secretary 创建或分配，Coordinator 提出项目级评审请求；任务级评审可由 Coordinator 在授权范围内安排独立上下文。Reviewer 根据研究问题、验收标准和证据评审，不受 Executor 或 Coordinator 结论支配。

Sequential Fallback 中，同一 Agent 的 Reviewer 角色只是模拟评审，不具有真正的上下文隔离。必须明确标注；高影响结论需要人类或 Harness 实际提供的独立通道。

## 3. 两阶段评审

高影响结论可以使用：

### 第一阶段：盲审证据

只提供：

- 研究问题；
- 验收标准；
- 原始证据及版本。

要求 Reviewer 独立判断证据能支持什么、不能支持什么，以及还缺什么。

### 第二阶段：对照结论

再提供 Executor 报告，检查：

- 结论范围是否超出证据；
- 是否遗漏证据；
- 是否推断过度；
- 是否忽略反面证据；
- 是否满足验收标准。

普通任务可以使用单阶段评审，不为流程完整而增加无价值步骤。

## 4. 评审结论

- `pass`：在已检查范围内通过；
- `conditional_pass`：有明确附加条件和责任人，未核实前不等于最终通过；
- `changes_required`：需要修正。

评审必须记录实际覆盖和未覆盖范围。任务级评审可以填写可选的 `targetTaskId`；项目级或跨任务评审不为满足形式而强行归属单个 Task。`targetRefs` 始终指向实际评审的制品及版本。

`conditional_pass` 的每项条件至少包含 `statement` 和 `owner`。

## 5. 返工与复审

- 原 Review 不修改。
- 需要修改时，Coordinator 创建带 `parentTaskId` 和 `triggerReviewId` 的修正 Task。
- Executor 提交新制品版本后，复审创建新的 Review。
- 将 `conditional_pass` 转为最终 `pass` 时，新 Review 应记录条件核实依据；不得把原记录直接改成 `pass`。
- Reviewer 默认不直接修改被评审制品，由责任 Executor 修正。

## 6. 最终对照实验评审

比较不同组织方式时，过程评审与最终评分分开：

- 两层和三层组使用同等的过程性独立评审，避免把 Reviewer 的收益误算成 Coordinator 的收益；
- 所有组使用相同的最终外部评审标准；
- 最终评分者不知道成果来自哪个组织方式。
