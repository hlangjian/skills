"""仅校验技能结构，不验证 Agent 行为。开发依赖见 requirements-dev.txt。"""

from pathlib import Path
import json
import re
import sys

try:
    import yaml
except ImportError:
    print("缺少开发校验依赖 PyYAML；请按 scripts/requirements-dev.txt 安装。")
    sys.exit(2)


root = Path(__file__).resolve().parents[1]
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


skill_path = root / "SKILL.md"
text = skill_path.read_text(encoding="utf-8")
frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
check(frontmatter is not None, "SKILL.md 缺少有效 YAML frontmatter")
if frontmatter:
    metadata = yaml.safe_load(frontmatter.group(1))
    check(metadata.get("name") == "portable-agent-team", "技能名称不匹配")
    check(bool(metadata.get("description")), "缺少 description")
    check(bool(metadata.get("compatibility")), "缺少 compatibility")

check(len(text.splitlines()) < 500, "SKILL.md 超过 500 行")
check(text.count("```") % 2 == 0, "SKILL.md 代码围栏未闭合")
check("Agent 实例化与角色绑定" in text, "缺少 Agent 实例化与角色绑定规则")
check("独立 Reviewer 上下文" in text, "缺少独立评审能力标记")
check("该主 Agent 默认承担 Secretary 角色" in text, "缺少主 Agent 的 Secretary 身份绑定")
check("Secretary 独占子智能体分配权" in text, "缺少 Secretary 独占分配权规则")
check("不是人类与团队之间的唯一通信通道" in text, "缺少允许人类直接指导角色的规则")
check("人类只与 Secretary 沟通" not in text, "仍存在过度严格的人类沟通限制")
check("不构成真实的信息隔离、遗忘或认知独立性" in text, "降级模式的信息隔离说明不完整")

secretary_text = (root / "references" / "roles" / "secretary.md").read_text(encoding="utf-8")
coordinator_text = (root / "references" / "roles" / "coordinator.md").read_text(encoding="utf-8")
check("只有 Secretary 可以创建、选择、分配、改派或结束" in secretary_text, "Secretary Profile 未明确独占实例分配")
check("不自行创建、选择、改派或结束子智能体实例" in coordinator_text, "Coordinator Profile 未限制实例分配权")

references = set(re.findall(r"`((?:references|examples)/[^`]+)`", text))
for relative in sorted(references):
    check((root / relative).is_file(), f"SKILL.md 引用了不存在的文件：{relative}")

clean_path = root / "references" / "schemas" / "project-state.yaml"
clean = yaml.safe_load(clean_path.read_text(encoding="utf-8"))
required_collections = {
    "unknowns",
    "assumptions",
    "claims",
    "decisions",
    "tasks",
    "artifacts",
    "reviews",
}
check("goal" in clean, "干净模板缺少 goal")
check(required_collections.issubset(clean), "干净模板缺少必要对象")
check(clean.get("goal") is None, "干净模板的 goal 应初始化为 null")
for collection in sorted(required_collections):
    check(clean.get(collection) == [], f"干净模板的 {collection} 应为空数组")

sample_path = root / "examples" / "sample-project-state.yaml"
sample = yaml.safe_load(sample_path.read_text(encoding="utf-8"))
check(sample["tasks"][0]["status"] == "done", "完整示例 Task 应展示提交状态 done")
check(sample["reviews"][0]["verdict"] == "conditional_pass", "完整示例应展示 conditional_pass")
check(
    sample["reviews"][0]["targetTaskId"] == sample["tasks"][0]["id"],
    "完整示例的 Review.targetTaskId 与 Task 不匹配",
)
check(
    {item["relation"] for item in sample["claims"][0]["evidenceRefs"]}
    <= {"supports", "contradicts", "context"},
    "Claim 包含不支持的证据关系",
)

simple_example = (root / "examples" / "simple-task.md").read_text(encoding="utf-8")
check("11 月" not in simple_example, "简单任务示例仍可能包含虚构日期")

evals_path = root / "evals" / "evals.json"
evals = json.loads(evals_path.read_text(encoding="utf-8"))
check(evals.get("skill_name") == "portable-agent-team", "evals.json 技能名称不匹配")
check(len(evals.get("evals", [])) >= 3, "至少需要三个测试用例")

if errors:
    print("STRUCTURE VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("STRUCTURE VALIDATION PASSED")
print("仅表示文件、引用和模板结构通过，不表示 Agent 行为已经验证。")
print(f"- SKILL.md：{len(text.splitlines())} 行")
print(f"- 资源引用：{len(references)} 个，全部存在")
print("- 干净模板：goal 为 null，七个集合为空")
print("- 完整示例：YAML 解析通过，Task、Claim 与 Review 关系有效")
print(f"- 测试用例：{len(evals['evals'])} 个，JSON 解析通过")
