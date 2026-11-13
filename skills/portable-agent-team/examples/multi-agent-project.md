# 示例：复杂调研项目与降级运行

## 用户请求

> 评估我们是否应该进入一个新的企业软件市场。现有数据互相矛盾，请先检查关键前提，再给出市场进入建议和一份可追溯证据的报告。

## Native Multi-Agent 模式

### 1. Secretary

确认交付物为“进入建议＋研究报告＋证据引用”，验收时要求区分市场事实、暂时假设和未解决问题。由于数据矛盾、计划依赖调查结果，创建 Coordinator。

Secretary 先展示 Harness 实际允许的模型与思考强度，建议 Coordinator 和最终 Reviewer 使用较强推理配置，Researcher 按研究难度选择，普通 Executor 使用高效配置。用户选择“采用推荐组合”后，将策略记录到 `modelPolicy`，不在每个任务重复询问。

### 2. Coordinator 初始化状态

复制 `references/schemas/project-state.yaml`，由 Coordinator 独占写入。

示例 Unknown：

```yaml
- id: unknown-market-size
  question: 目标市场的有效规模是多少？
  decisionImpact: 规模不足时不进入；规模足够时继续评估进入方式
  status: open
```

示例 Assumption：

```yaml
- id: assumption-icp
  statement: 暂时把 200—1000 人企业视为理想客户
  basis: 现有产品能力初步匹配
  validationMethod: 客户访谈与替代方案调查
  invalidationCondition: 目标访谈群体显示需求显著不足
  status: active
```

### 3. 分派与提交

Coordinator 规划市场数据 Task 和客户研究 Task，并在授权范围内分配 Researcher 调查关键未知、分配 Executor 完成报告整合。两类角色都向 Coordinator 提交制品、证据、验证和剩余未知，不直接修改共享状态。Secretary 不逐条转发执行结果。

示例 Claim：

```yaml
- id: claim-subscription
  statement: 三个被调查竞争对手采用订阅收费
  status: supported
  scope: 仅限本次调查的三家竞争对手
  evidenceRefs:
    - ref: artifact-competitors?version=1#table=pricing
      relation: supports
      note: 三家公司的公开价格页均列出订阅方案
```

该 Claim 不能直接证明“我们的目标客户愿意购买订阅服务”。

### 4. 独立评审

高影响进入建议采用两阶段评审：

1. Reviewer 先阅读研究问题、验收标准和原始证据，独立判断证据边界。
2. 再阅读 Executor 报告，检查推断过度、证据遗漏和反面证据。

若结论为 `changes_required`，Coordinator 创建带 `parentTaskId` 和 `triggerReviewId` 的修正 Task。原 Task 保持 `done`，原 Review 不改写。

### 5. 完成

Coordinator 整合新制品、复审和最终 Decision。Secretary 只向用户呈现建议、关键依据、残余未知和制品入口，不倾倒全部角色对话。

## Sequential Fallback 模式

如果当前环境没有子 Agent 或委派工具，开头必须说明：

```text
运行模式：Sequential Fallback。
当前由单个 Agent 顺序模拟角色，不是真正多 Agent；模拟评审不具备独立上下文。
```

随后按以下顺序执行：

1. Secretary 确认目标与验收；
2. Coordinator 建立并独占更新项目状态；
3. Executor 角色提交任务结果；
4. Reviewer 角色进行模拟评审，并明确独立性限制；
5. Coordinator 整合结果；
6. Secretary 呈现交付物。

高影响结论需要真正独立评审时，请求人类复核或使用实际存在的独立评审通道。不能把同一 Agent 的角色切换描述成“独立 Reviewer 已验证”。
