#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_video_creator — 样本生成器

特点：
  1. Query 直接从 unified_scenario_design.yaml 的 user_need_templates 获取
  2. 源材料按 topic 过滤匹配（eval_framework / creative_methodology / checker_tech / sample_design）
  3. 通用 check_list + 模板特定参数替换
  4. 公共 environment（skills + schemas + judge_criteria）自动扫描
  5. source_materials/*.md 作为样本特有环境文件

使用方式：
  cd scripts/sample_generator
  python main.py                             # 生成所有样本
  python main.py --output samples/eval.jsonl # 指定输出路径
  python main.py --export-check-revision check_revisions/rev_001  # 仅导出检查方案
"""

import argparse
import base64
import json
import sys
from copy import deepcopy
from pathlib import Path

import yaml


# topic → source_materials 文件名映射
TOPIC_TO_SOURCE_FILES = {
    "creative_scenario": ["creative_scenario_construction.md"],
    "query_construction": ["query_construction_methodology.md"],
    "agent_eval": ["agent_eval_demystified.md"],
    "eval_skills_guide": ["agent-evaluation-skills-guide.md"],
    "long_running_agents": ["effective_harnesses_long_running_agents.md"],
}


class KnowledgeVideoCreatorSampleGenerator:
    """knowledge_video_creator 场景样本生成器"""

    # 自动扫描的文件后缀
    TEXT_EXTENSIONS = {".md", ".json", ".yaml", ".yml", ".txt", ".csv"}
    BINARY_EXTENSIONS = {".xlsx", ".xls", ".png", ".jpg", ".jpeg", ".gif", ".pdf"}

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()

        # ── 加载配置文件 ──
        print("Loading configuration files...")
        with open(self.base_dir / "unified_scenario_design.yaml", "r", encoding="utf-8") as f:
            self.scenario = yaml.safe_load(f)

        with open(self.base_dir / "BusinessRules.md", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        # ── 加载能力体系 ──
        print("Loading capability taxonomy...")
        taxonomy_path = self.base_dir / "check_capability_taxonomy.yaml"
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            self.capability_taxonomy = yaml.safe_load(f)
        self._build_capability_lookup()

        # ── 加载检查项 ──
        check_def_dir = self.base_dir / "check_definitions"

        # 通用检查项
        common_path = check_def_dir / "common_check_list.yaml"
        with open(common_path, "r", encoding="utf-8") as f:
            common_data = yaml.safe_load(f)
        self.common_checks = common_data.get("common_checks", [])
        print(f"Loaded {len(self.common_checks)} common check items")

        # ── 构建公共环境 ──
        print("Building common environment...")
        self.common_environment = self._build_common_environment()
        print(f"Common environment: {len(self.common_environment)} files")

        # ── 扫描源材料 ──
        self.source_materials = self._scan_source_materials()
        print(f"Found {len(self.source_materials)} source material topics")

    def _build_capability_lookup(self):
        """构建能力体系查找结构"""
        self.valid_dimensions = set()
        self.subcategory_to_dimension = {}

        for dimension in self.capability_taxonomy.get("capability_dimensions", []):
            dim_id = dimension["dimension_id"]
            self.valid_dimensions.add(dim_id)
            for sub in dimension.get("subcategories", []):
                self.subcategory_to_dimension[sub["subcategory_id"]] = dim_id

        print(f"Loaded {len(self.valid_dimensions)} capability dimensions, "
              f"{len(self.subcategory_to_dimension)} subcategories")

    def _build_common_environment(self):
        """扫描公共环境文件（skills + schemas + judge_criteria）

        注意：source_materials 不进入公共环境 — 各样本按 topic 单独注入。
        """
        env = []
        scan_dirs = ["data_pools/skills", "data_pools/schemas", "check_definitions/judge_criteria"]

        for dir_name in scan_dirs:
            scan_dir = self.base_dir / dir_name
            if not scan_dir.exists():
                print(f"  Warning: {dir_name}/ not found")
                continue

            for filepath in sorted(scan_dir.rglob("*")):
                if not filepath.is_file():
                    continue
                if filepath.name.startswith(".") or filepath.name.startswith("~$"):
                    continue

                relative_path = filepath.relative_to(self.base_dir)
                suffix = filepath.suffix.lower()

                if suffix in self.TEXT_EXTENSIONS:
                    with open(filepath, "r", encoding="utf-8") as f:
                        env.append({
                            "path": str(relative_path),
                            "type": "file",
                            "content": f.read()
                        })
                elif suffix in self.BINARY_EXTENSIONS:
                    with open(filepath, "rb") as f:
                        env.append({
                            "path": str(relative_path),
                            "type": "binary",
                            "content": base64.b64encode(f.read()).decode("ascii")
                        })

        return env

    def _scan_source_materials(self):
        """扫描 data_pools/source_materials/ 目录下的源材料

        Returns:
            {topic: [{filename, content, char_count}]}
        """
        materials = {}
        mat_dir = self.base_dir / "data_pools" / "source_materials"
        if not mat_dir.exists():
            print(f"  Warning: data_pools/source_materials/ not found")
            return materials

        for filepath in sorted(mat_dir.glob("*.md")):
            filename = filepath.name
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 从 TOPIC_TO_SOURCE_FILES 反查 topic
            topic = None
            for t, file_list in TOPIC_TO_SOURCE_FILES.items():
                if filename in file_list:
                    topic = t
                    break

            if topic is None:
                # 尝试从文件名推断
                stem = filepath.stem.lower()
                for t in TOPIC_TO_SOURCE_FILES.keys():
                    if t in stem:
                        topic = t
                        break

            if topic is None:
                topic = filepath.stem  # 兜底

            if topic not in materials:
                materials[topic] = []

            materials[topic].append({
                "filename": filename,
                "content": content,
                "char_count": len(content)
            })
            print(f"  Loaded source material: {filename} -> topic={topic} ({len(content)} chars)")

        return materials

    def _match_source_materials(self, template):
        """根据模板的 entity_filters.source_materials.topic 匹配源材料"""
        filters = template.get("entity_filters", {}).get("source_materials", {})
        topic = filters.get("topic", "")

        if topic and topic in self.source_materials:
            return self.source_materials[topic]

        # 无匹配，返回空
        return []

    def _convert_checklist(self, template):
        """构建样本的 check_list"""
        converted = []
        server_name = self.scenario.get("mcp_service_config", {}).get("service_name", "")

        def process_check_item(item):
            """将单个检查项转为样本格式"""
            check_item = {
                "check_type": item["check_type"],
                "params": deepcopy(item.get("params", {}))
            }

            # tool_called_with_params 的工具名加 server 前缀
            if item["check_type"] == "tool_called_with_params" and server_name:
                params = check_item["params"]
                if "tool_name" in params:
                    tool_name = params["tool_name"]
                    if "__" not in tool_name:
                        params["tool_name"] = f"{server_name}__{tool_name}"
                # ordered_calls / required_sequence 中的工具名也要加前缀
                for key in ("ordered_calls", "required_sequence"):
                    if key in params:
                        for call in params[key]:
                            if "tool_name" in call and "__" not in call["tool_name"]:
                                call["tool_name"] = f"{server_name}__{call['tool_name']}"

            # description
            if "check_name" in item:
                check_item["description"] = item["check_name"]
            elif "description" in item:
                check_item["description"] = item["description"]

            # 保留元数据字段
            for field in ["dimension_id", "subcategory_id", "quality_tier",
                          "weight", "is_critical", "is_gate"]:
                if field in item:
                    check_item[field] = item[field]

            # 保留语义化 check_id
            if "check_id" in item:
                check_item["check_id"] = item["check_id"]

            return check_item

        # 通用检查项
        for item in self.common_checks:
            converted.append(process_check_item(item))

        # 为没有 check_id 的项生成兜底编号
        for idx, check_item in enumerate(converted, 1):
            if "check_id" not in check_item:
                check_item["check_id"] = f"check_{idx:02d}"

        return converted

    def generate_samples(self):
        """生成所有样本"""
        samples = []

        for template in self.scenario["user_need_templates"]:
            template_id = template["need_template_id"]
            print(f"\nProcessing template: {template_id}")

            # 构建 query
            query_text = template.get("user_need_description", "").strip()
            if not query_text:
                print(f"  Warning: No user_need_description, skipping")
                continue

            # 匹配源材料
            matched_materials = self._match_source_materials(template)
            if not matched_materials:
                topic = template.get("entity_filters", {}).get("source_materials", {}).get("topic", "?")
                print(f"  Warning: No matching source materials for topic={topic}, using placeholder")
                matched_materials = [{"filename": "placeholder.md", "content": "【占位符】请提供源技术文档。", "char_count": 0}]

            # 构建 environment（公共 + 样本特有的 source_materials/）
            environment = deepcopy(self.common_environment)

            for mat in matched_materials:
                environment.append({
                    "path": f"workspace/source_materials/{mat['filename']}",
                    "type": "file",
                    "content": mat["content"]
                })

            # 构建 check_list
            check_list = self._convert_checklist(template)

            # 构建 user_simulator_prompt
            user_sim = template.get("user_simulator_prompt", "").strip()

            # 数据ID
            data_id = f"{template_id}_001"

            # system prompt 追加
            system_additions = template.get("system_prompt_additions", "").strip()
            full_system = self.system_prompt
            if system_additions:
                full_system += "\n\n" + system_additions

            sample = {
                "data_id": data_id,
                "query": query_text,
                "system": full_system,
                "servers": ["knowledge_video_creator_service"],
                "environment": environment,
                "check_list": check_list,
                "user_simulator_prompt": user_sim,
                "extension": {
                    "template_id": template_id,
                    "description": template.get("description", ""),
                    "creation_params": template.get("creation_params", {}),
                    "entity_filters": template.get("entity_filters", {}),
                    "test_type": template.get("test_type", "positive"),
                }
            }

            samples.append(sample)
            total_chars = sum(mat["char_count"] for mat in matched_materials)
            print(f"  Generated sample: {data_id} "
                  f"({len(check_list)} checks, "
                  f"{len(matched_materials)} source files, "
                  f"{total_chars} chars)")

        return samples

    def validate_samples(self, samples):
        """验证样本格式"""
        print("\nValidating samples...")
        required_fields = ["data_id", "query", "system", "servers", "environment", "check_list"]
        errors = []

        for idx, sample in enumerate(samples, 1):
            for field in required_fields:
                if field not in sample:
                    errors.append(f"Sample {idx}: Missing field '{field}'")

            if not isinstance(sample.get("environment"), list) or len(sample["environment"]) == 0:
                errors.append(f"Sample {idx}: Invalid environment")

            if not isinstance(sample.get("check_list"), list) or len(sample["check_list"]) == 0:
                errors.append(f"Sample {idx}: Invalid check_list")

            # 检查 check_list 中的字段
            for ci, check in enumerate(sample.get("check_list", []), 1):
                if "check_type" not in check:
                    errors.append(f"Sample {idx}, check {ci}: Missing 'check_type'")
                if "params" not in check:
                    errors.append(f"Sample {idx}, check {ci}: Missing 'params'")
                if "check_id" not in check:
                    errors.append(f"Sample {idx}, check {ci}: Missing 'check_id'")

            # 检查 source_materials 是否注入
            has_source = any("source_materials/" in e.get("path", "") for e in sample.get("environment", []))
            if not has_source:
                errors.append(f"Sample {idx}: No source materials in environment")

        if errors:
            print(f"\n  Found {len(errors)} validation errors:")
            for err in errors:
                print(f"    - {err}")
            return False

        print(f"  All {len(samples)} samples validated successfully")
        return True

    def save_samples(self, samples, output_path):
        """保存样本为 JSONL 格式"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # JSONL（用于评测）
        with open(output_file, "w", encoding="utf-8") as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
        print(f"\nGenerated {len(samples)} samples -> {output_file}")

        # 可读版本
        readable_file = output_file.parent / (output_file.stem + "_readable.json")
        with open(readable_file, "w", encoding="utf-8") as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        print(f"Generated readable version -> {readable_file}")

        # 统计
        print(f"\nSamples summary:")
        for sample in samples:
            ext = sample.get("extension", {})
            params = ext.get("creation_params", {})
            filters = ext.get("entity_filters", {})
            topic = filters.get("source_materials", {}).get("topic", "?")
            print(f"  {sample['data_id']}: "
                  f"topic={topic}, "
                  f"source_chars={sum(len(f.get('content','')) for f in sample.get('environment',[]) if 'source_materials' in f.get('path',''))}, "
                  f"{len(sample['check_list'])} checks")

    def export_check_revision(self, samples, revision_dir):
        """仅导出评测方案（checklist + judge_criteria）"""
        import shutil

        revision_path = Path(revision_dir)
        revision_path.mkdir(parents=True, exist_ok=True)

        # checklist.jsonl
        checklist_file = revision_path / "checklist.jsonl"
        with open(checklist_file, "w", encoding="utf-8") as f:
            for sample in samples:
                entry = {
                    "data_id": sample["data_id"],
                    "check_list": sample["check_list"]
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"\nExported {len(samples)} checklists -> {checklist_file}")

        # 统计
        if samples:
            check_count = len(samples[0]["check_list"])
            dims = {}
            for c in samples[0]["check_list"]:
                dim = c.get("dimension_id", "unknown")
                dims[dim] = dims.get(dim, 0) + 1
            print(f"  Check items per sample: {check_count}")
            for d, n in sorted(dims.items()):
                print(f"    {d}: {n}")

        # 复制 judge_criteria
        src_criteria = self.base_dir / "check_definitions" / "judge_criteria"
        dst_criteria = revision_path / "judge_criteria"
        if src_criteria.exists():
            if dst_criteria.exists():
                shutil.rmtree(dst_criteria)
            shutil.copytree(src_criteria, dst_criteria)
            count = len(list(dst_criteria.rglob("*")))
            print(f"Copied judge_criteria ({count} files) -> {dst_criteria}")

        # 元数据
        from datetime import datetime
        meta = {
            "generated_at": datetime.now().isoformat(),
            "sample_count": len(samples),
            "check_count_per_sample": len(samples[0]["check_list"]) if samples else 0,
            "data_ids": [s["data_id"] for s in samples],
            "source_design_dir": str(self.base_dir),
        }
        meta_file = revision_path / "meta.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"Written revision metadata -> {meta_file}")


def main():
    parser = argparse.ArgumentParser(description="knowledge_video_creator 场景样本生成器")
    parser.add_argument("--output", "-o", default="samples/eval_kvc.jsonl",
                        help="输出文件路径 (默认: samples/eval_kvc.jsonl)")
    parser.add_argument("--base-dir", default=None,
                        help="场景根目录（默认为 scripts/sample_generator 的祖父目录）")
    parser.add_argument("--export-check-revision", metavar="DIR",
                        help="仅导出评测方案到指定 revision 目录")
    args = parser.parse_args()

    # 确定 base_dir
    if args.base_dir:
        base_dir = args.base_dir
    else:
        # 默认：从 scripts/sample_generator/main.py 向上2层到场景根目录
        base_dir = str(Path(__file__).resolve().parents[2])

    print(f"Base directory: {base_dir}")

    generator = KnowledgeVideoCreatorSampleGenerator(base_dir)
    samples = generator.generate_samples()

    if not generator.validate_samples(samples):
        print("\nSample validation failed!")
        return 1

    if args.export_check_revision:
        generator.export_check_revision(samples, args.export_check_revision)
    else:
        output_path = Path(base_dir) / args.output
        generator.save_samples(samples, output_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
