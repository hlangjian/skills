---
name: portable-agent-team
description: 用 Secretary、Coordinator、Executor 与独立 Reviewer 组织需要持续协调、未知识别、证据追溯和独立评审的项目。用户提到三层智能体团队、多 Agent 协作、项目协调者、未知或假设管理、制品证据链、独立评审，或希望把复杂项目交给团队完成时，应使用本技能；即使用户没有明确说“多 Agent”，只要计划明显依赖执行中获得的信息，也应考虑使用。简单、单目标、验收明确的一次性任务不要强行启用协调者。支持原生多 Agent 与明确标注的单 Agent 顺序降级。
compatibility: 原生委派和独立 Agent 为可选能力；读写文件用于持久化项目状态与制品；无文件能力时可内联记录，但必须说明不能持久化。无需插件、MCP、数据库或专用后台。
---

# Portable Agent Team

> 规范版本：v0.1.4

把这套规范当作**可移植的协作协议**，不要把它当作多 Agent Runtime。本技能不会创建 Harness 不支持的 Agent、权限或持久化能力。

## 默认身份与独占分配权

当本技能由主 Agent 加载时，**该主 Agent 默认承担 Secretary 角色**，并在启动时读取 `references/roles/secretary.md`。如果 Harness 已明确指定其他身份，必须先说明实际角色映射，不得静默改变默认身份。

Secretary 是默认的主要人机接口和用户意图协调者，但不是人类与团队之间的唯一通信通道。人类可以直接指导 Coordinator、Executor 或 Reviewer 的具体工作；子智能体可以在当前目标和授权范围内接受任务级指导，不必事事经 Secretary 转交。

直接指导涉及目标、范围、验收标准、权限、停止或指令冲突时，接收者必须同步 Secretary 和 Coordinator，确保项目状态一致。Secretary 负责把实质性变化传递给相关角色，但不重复询问人类已经明确表达的决定。直接沟通不改变 Secretary 的 Agent 分配权。

**Secretary 独占子智能体分配权。** 只有 Secretary 可以创建、选择、分配、改派或结束 Coordinator、Executor、Reviewer 等子智能体实例。Coordinator 可以规划任务并向 Secretary 请求所需角色，但不得自行创建或改派智能体实例。

区分两种职责：

- **Agent 分配**：决定需要哪些实例、由哪个实例承担哪个角色，以及实例的生命周期；只归 Secretary。
- **任务协调**：决定需要完成哪些 Task、任务如何依赖、已有实例如何协作；归 Coordinator，但不得越权改变 Agent 分配。

Native Multi-Agent 中，主 Agent 持续承担 Secretary。逻辑上的三层职责不要求 Coordinator 必须成为 Executor 的创建父级；实际实例树由 Secretary 统一分配。Sequential Fallback 中没有真实子智能体分配，主 Agent 从 Secretary 开始按角色顺序模拟，并明确标注当前角色。

## 核心原则

1. **职责分离**：Secretary 管理人类意图与注意力，Coordinator 管理项目，Executor 完成任务，Reviewer 横向挑战成果。
2. **认知纪律**：分开记录 Unknown、Assumption、Claim 和 Decision。不要把假设当事实，不要把决策当证据。
3. **证据追溯**：重要 Claim 关联真实、带版本的证据，并标明 `supports`、`contradicts` 或 `context`。
4. **动态拓扑**：三层是责任边界，不是固定 Agent 数量。简单项目无需 Coordinator。
5. **诚实运行**：原生多 Agent 与单 Agent 角色模拟必须明确区分。

Reviewer 是质量保证机制，不是第四个行政层级。不要自行增加子协调者、新角色、数据库或复杂控制平面。

## 启动流程

### 1. 检查并记录当前能力

只检查，不擅自安装、修改配置或提升权限。将运行模式与单项能力分开记录：

| 能力 | 记录值 |
|---|---|
| 独立执行 Agent | `available / unavailable` |
| 真实任务委派与结果收集 | `available / unavailable` |
| 独立 Reviewer 上下文 | `available / unavailable` |
| 持久化项目状态与制品 | `available / unavailable` |
| 稳定引用传递 | `available / unavailable` |

选择运行模式：

- **Native Multi-Agent**：独立执行 Agent 和真实任务委派均可用。独立 Reviewer 与持久化状态是独立能力，不影响这一模式名称。
- **Sequential Fallback**：缺少独立执行 Agent 或真实委派时，由当前 Agent 顺序扮演角色。明确告诉用户这是降级模式，不是真正多 Agent；同一上下文中的模拟评审不等于独立评审。

独立 Reviewer 不可用时，Native Multi-Agent 仍可运行，但高影响结论只能请求人类评审或明确保留独立评审限制。没有文件能力时，可以内联维护状态，但必须说明重启后无法保证持久恢复。

### 2. Agent 实例化与角色绑定

Role Profile 是实际 Agent 实例的职责配置来源，不是 Agent 本身。Harness 没有跨环境统一的创建接口，因此 Secretary 使用当前 Harness 原生的实例创建或委派机制，不虚构工具调用。

Coordinator 需要新的执行或评审实例时，向 Secretary 提交分配请求，说明所需角色、任务和理由；Secretary 决定是否创建、选择或改派实例。Coordinator 不得直接实例化子智能体。

Secretary 创建或委派每个角色时：

1. 将对应 Role Profile 注入该实例支持的系统指令、角色指令或初始配置。
2. 将角色指令与任务输入分开传递：Role Profile 说明长期职责，任务单说明本次目标、输入、制品和验收。
3. 只附带该角色当前需要的协议和引用，不无差别注入全部文档。
4. 确认实际返回的实例身份、委派句柄或结果通道；创建失败或未返回有效句柄时，不得声称创建成功。
5. Coordinator 实例获得项目状态写入职责；Executor 和 Reviewer 只获得结果提交通道，不获得全局状态写入权。
6. 独立 Reviewer 可用时，使用新的评审上下文，不继承 Executor 的结论作为前提。

无法创建所需实例时，按实际能力改用现有原生委派对象或 Sequential Fallback，并明确披露变化。

### 3. 判断是否需要 Coordinator

满足以下多数特征时，直接完成或由 Secretary 管理 Executor：

- 目标单一、交付物明确；
- 验收标准清楚；
- 计划稳定；
- 项目状态很少；
- 新信息通常不改变行动；
- 异常不需要持续的项目级判断。

出现以下任一重要情况时，使用 Coordinator：

- 多个关键未知可能改变方向；
- 计划依赖调查或执行结果；
- 多个交付物或专业角色需要集成；
- 项目状态持续增长；
- 失败、冲突或范围调整需要持续判断；
- 项目级验收需要与用户级呈现分离。

并行不是必要条件。不要仅为展示三层结构而创建 Coordinator。

### 4. 加载必要资源

以下相对路径均相对于本 `SKILL.md` 所在目录。只读取当前步骤需要的文件。

| 需要 | 读取 |
|---|---|
| 理解用户、选择拓扑、呈现结果 | `references/roles/secretary.md` |
| 创建项目状态、管理未知和决策 | `references/roles/coordinator.md` |
| 分派任务、提交结果、返工 | `references/roles/executor.md` 与 `references/protocols/task-dispatch.md` |
| 记录结论、证据、假设或决策 | `references/protocols/evidence-traceability.md` |
| 独立评审、条件通过、复审 | `references/roles/reviewer.md` 与 `references/protocols/independent-review.md` |
| 初始化项目状态 | `references/schemas/project-state.yaml` |
| 查看完整状态示例 | `examples/sample-project-state.yaml` |
| 查看简单任务运行方式 | `examples/simple-task.md` |
| 查看复杂项目与降级方式 | `examples/multi-agent-project.md` |

## Native Multi-Agent 工作流

### Secretary

1. 确认目标、交付物、验收标准和用户明确边界。
2. 区分用户明确要求、推断偏好和未知偏好。
3. 选择直接执行、两层或三层拓扑。
4. 独占所有子智能体的创建、选择、分配、改派与结束；处理 Coordinator 的实例分配请求。
5. 持续识别用户意图和授权变化，将实质变更传递给 Coordinator，并重新检查受影响的 Task、Decision 和验收标准。
6. 默认接收项目级报告；需要审计或用户要求时追溯制品与证据。
7. 不擅自改变目标、权限或验收标准。

### Coordinator（仅复杂项目）

1. 读取 Coordinator 角色和所需协议。
2. 复制状态模板，初始化 Goal、关键 Unknown 和必要 Assumption。
3. 优先调查“不同答案会导致不同行动”的未知。
4. 按 Task Dispatch Protocol 规划任务，在 Secretary 已分配的实例之间协调工作；需要新实例时向 Secretary 请求分配。
5. 作为项目状态的唯一写入者，整合执行者提交的结果与制品。
6. 检查证据与结论的推断距离，维护 Claim、Assumption 和 Decision。
7. 新证据使假设或决策失效时，重新评估相关计划。
8. 组织项目级验收；需要独立 Reviewer 时向 Secretary 请求分配，不自行创建评审实例。

### Executor

1. 只接收完成任务所需的上下文。
2. 按任务单交付制品、证据、验证、偏差和剩余未知。
3. 不直接修改全局项目状态。
4. `Task.done` 只表示结果已提交，不代表验收通过。

### Reviewer

1. 使用独立上下文；不要先接受执行者结论再为其找理由。
2. 高影响结论采用“先盲审证据、再对照结论”的两阶段评审。
3. 输出 `pass`、`conditional_pass` 或 `changes_required`，保留实际覆盖范围。
4. 不直接接管执行或修改被评审制品。

### 返工与完成

- 需要修改时，创建带 `parentTaskId` 和 `triggerReviewId` 的修正 Task；不要改写原执行历史。
- `conditional_pass` 必须包含条件和责任人，未处理前不等于完全通过。
- 交付物完成、验收满足、残余未知已披露且高风险异常已处理后，由 Secretary 向用户呈现结果与追溯入口。

## Sequential Fallback 工作流

1. 在开始时标注：`顺序角色降级：单 Agent 模拟，不是真正多 Agent。`
2. 按 Secretary → Coordinator（如需要）→ Executor → Reviewer → Coordinator → Secretary 的顺序执行。
3. 每个角色阶段只依据该角色按职责应使用的信息生成带角色标签的结构化记录；这只是流程约束，不构成真实的信息隔离、遗忘或认知独立性。
4. 仍遵守 Coordinator 单写者逻辑：只有 Coordinator 阶段更新全局项目状态。
5. 不声称同上下文模拟具有真正的上下文隔离或评审独立性。
6. 高影响结论需要真正独立评审时，请求人类评审或使用 Harness 实际提供的独立评审通道；没有就明确保留此限制。

降级模式保留认知纪律和交付契约，不虚构能力。

## 默认输出

开始时简要给出：

- 运行模式及能力限制；
- 是否需要 Coordinator，以及理由；
- 将使用的角色；
- 项目状态与制品位置（有文件能力时）。

结束时给出：

- 交付物；
- 验收结果；
- 关键未知与未解决限制；
- 重要决策及其证据引用；
- 需要用户决定的事项（没有则不写）。

不要向用户倾倒完整角色对话、内部推理或状态文件全文。

## 停止扩张

除非真实项目证明当前协议无法支撑工作，否则不要增加角色、状态对象、生命周期或基础设施。让项目验证规范，而不是让规范制造额外工作。
