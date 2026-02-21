#!/usr/bin/env python3
"""
小说创作场景评测统计分析脚本
=================================

功能：
1. 读取evaluation_outputs目录下的评测结果
2. 聚合 check_result_revXXX.json（位于 {sample_id}_env/check_result_revXXX.json）
3. 多层级统计分析（总览/维度/子类/内容质量层级）
4. 生成JSON和Markdown格式的报告

使用（本地模式 - 直接读取目录）：
python scripts/analysis/generate_statistics.py \
    --eval-dir evaluation_outputs/eval_dsv1_20260214_014809_claude-opus-4-6 \
    --output-dir evaluation_outputs/eval_dsv1_20260214_014809_claude-opus-4-6/analysis

使用（远程模式 - 通过HTTP API读取）：
python scripts/analysis/generate_statistics.py \
    --remote-url http://10.25.70.163:9090 \
    --eval-dir eval_dsv1_20260214_014809_claude-opus-4-6 \
    --output-dir ./analysis_opus

指定revision版本：
python scripts/analysis/generate_statistics.py \
    --eval-dir evaluation_outputs/eval_dsv1_20260214_014809_claude-opus-4-6 \
    --revision rev008 \
    --output-dir ./analysis_opus
"""

import json
import argparse
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime

try:
    import urllib.request
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


class RemoteReader:
    """通过HTTP API读取远程服务器文件"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def list_dir(self, path: str) -> List[Dict]:
        """列出目录内容"""
        url = f"{self.base_url}/api/ls/{path}"
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("entries", [])
        except Exception as e:
            print(f"  警告: 无法列出目录 {path}: {e}")
            return []

    def read_json(self, path: str) -> Optional[Dict]:
        """读取JSON文件"""
        url = f"{self.base_url}/api/file/{path}"
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data.get("content", "")
                return json.loads(content)
        except Exception as e:
            print(f"  警告: 无法读取文件 {path}: {e}")
            return None


class LocalReader:
    """读取本地文件系统"""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def list_dir(self, path: str) -> List[Dict]:
        """列出目录内容"""
        full_path = self.base_dir / path
        if not full_path.exists():
            return []
        entries = []
        for entry in full_path.iterdir():
            entries.append({
                "name": entry.name,
                "type": "dir" if entry.is_dir() else "file",
                "size": entry.stat().st_size if entry.is_file() else 0
            })
        return entries

    def read_json(self, path: str) -> Optional[Dict]:
        """读取JSON文件"""
        full_path = self.base_dir / path
        if not full_path.exists():
            return None
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  警告: 无法读取文件 {full_path}: {e}")
            return None


class NWStatisticsAnalyzer:
    """NW (Novel Writing Alchemist) 评测统计分析器"""

    # NW 的 4 个能力维度（固定顺序）
    DIMENSIONS = [
        "format_compliance",
        "business_rule_compliance",
        "memory_management",
        "content_quality"
    ]

    DIMENSION_NAMES = {
        "format_compliance": "格式规范遵循",
        "business_rule_compliance": "业务规则遵循",
        "memory_management": "记忆管理",
        "content_quality": "内容创作质量"
    }

    def __init__(self, reader, eval_dir: str, revision: str = None):
        self.reader = reader
        self.eval_dir = eval_dir
        self.revision = revision  # e.g. "rev008", None = auto-detect latest
        self.model_name = self._extract_model_name()

        # 数据容器
        self.check_results: Dict[str, Dict] = {}  # sample_id -> check_result.json
        self.sample_statuses: Dict[str, str] = {}  # sample_id -> execution_status
        self.check_revision_used: Dict[str, str] = {}  # sample_id -> actual revision used

    def _extract_model_name(self) -> str:
        """从目录名提取模型名称"""
        dir_name = self.eval_dir.split("/")[-1] if "/" in self.eval_dir else self.eval_dir
        # 格式: eval_dsv{N}_YYYYMMDD_HHMMSS_model-name
        # e.g. eval_dsv1_20260214_014809_claude-opus-4-6
        parts = dir_name.split("_")
        # eval_dsv1_20260214_014809_claude-opus-4-6
        # 0    1    2        3      4...
        if len(parts) >= 5:
            return "_".join(parts[4:])
        return "unknown"

    def _find_latest_check_result(self, env_entries: List[Dict]) -> Optional[str]:
        """从env目录的文件列表中找到最新的check_result文件名"""
        # 匹配 check_result_revXXX.json 或 check_result.json
        check_files = []
        for entry in env_entries:
            name = entry["name"]
            if name.startswith("check_result") and name.endswith(".json"):
                check_files.append(name)

        if not check_files:
            return None

        # 如果指定了revision，直接返回
        if self.revision:
            target = f"check_result_{self.revision}.json"
            if target in check_files:
                return target
            # fallback: 也尝试无revision的
            if "check_result.json" in check_files and self.revision is None:
                return "check_result.json"
            return None

        # 自动选最新的revision
        # 排序：check_result_rev008.json > check_result_rev007.json > check_result.json
        def sort_key(name):
            m = re.search(r"rev(\d+)", name)
            if m:
                return int(m.group(1))
            return -1  # check_result.json 排最后

        check_files.sort(key=sort_key, reverse=True)
        return check_files[0]

    def load_data(self):
        """加载所有样本的check_result"""
        eval_path = f"evaluation_outputs/{self.eval_dir}" if not self.eval_dir.startswith("evaluation_outputs") else self.eval_dir
        print(f"正在加载评测结果: {eval_path}")
        if self.revision:
            print(f"  指定revision: {self.revision}")
        else:
            print(f"  自动选择最新revision")

        entries = self.reader.list_dir(eval_path)
        if not entries:
            print(f"  错误: 目录为空或不存在: {eval_path}")
            return

        # 找到所有 _env 目录（包含 check_result*.json）
        env_dirs = [e["name"] for e in entries if e["type"] == "dir" and e["name"].endswith("_env") and not e["name"].startswith("env_")]
        sample_jsons = [e["name"] for e in entries if e["type"] == "file" and e["name"].endswith(".json") and e["name"] != "execution_report.json"]

        print(f"  找到 {len(sample_jsons)} 个样本JSON, {len(env_dirs)} 个env目录")

        # 确定样本ID列表
        sample_ids = set()
        for name in sample_jsons:
            sample_id = name.replace(".json", "")
            sample_ids.add(sample_id)

        for sample_id in sorted(sample_ids):
            # 检查 execution_status
            sample_json = self.reader.read_json(f"{eval_path}/{sample_id}.json")
            if sample_json is None:
                continue

            status = sample_json.get("execution_status", "unknown")
            self.sample_statuses[sample_id] = status

            if status != "success":
                print(f"  跳过 {sample_id}: execution_status={status}")
                continue

            # 读取 check_result*.json（revision模式）
            env_dir = f"{sample_id}_env"
            env_entries = self.reader.list_dir(f"{eval_path}/{env_dir}")

            check_filename = self._find_latest_check_result(env_entries)
            if check_filename is None:
                print(f"  警告: {sample_id} 没有 check_result (checker未运行?)")
                continue

            check_result_path = f"{eval_path}/{env_dir}/{check_filename}"
            check_result = self.reader.read_json(check_result_path)

            if check_result is None:
                print(f"  警告: {sample_id} 无法读取 {check_filename}")
                continue

            self.check_results[sample_id] = check_result
            self.check_revision_used[sample_id] = check_filename

            total_score = check_result.get("overall_result", {}).get("total_score", "N/A")
            print(f"  + {sample_id}: total_score={total_score} ({check_filename})")

        print(f"\n+ 加载了 {len(self.check_results)} 个有效check结果 (共 {len(sample_ids)} 个样本)")

    def analyze_overview(self) -> Dict:
        """总览统计"""
        total_samples = len(self.sample_statuses)
        success_samples = sum(1 for s in self.sample_statuses.values() if s == "success")
        error_samples = sum(1 for s in self.sample_statuses.values() if s != "success")
        checked_samples = len(self.check_results)

        # 聚合总分
        scores = []
        content_scores = []
        process_scores = []

        for sample_id, cr in self.check_results.items():
            overall = cr.get("overall_result", {})
            total_score = overall.get("total_score")
            content_score = overall.get("content_score")
            process_score = overall.get("process_score")

            if total_score is not None:
                scores.append(total_score)
            if content_score is not None:
                content_scores.append(content_score)
            if process_score is not None:
                process_scores.append(process_score)

        # 质量等级分布
        quality_levels = defaultdict(int)
        for cr in self.check_results.values():
            dim_scores = cr.get("dimension_scores", {})
            cq = dim_scores.get("content_quality", {})
            level = cq.get("quality_level", "unknown")
            quality_levels[level] += 1

        return {
            "total_samples": total_samples,
            "success_samples": success_samples,
            "error_samples": error_samples,
            "checked_samples": checked_samples,
            "scores": {
                "total": self._calc_stats(scores),
                "content": self._calc_stats(content_scores),
                "process": self._calc_stats(process_scores)
            },
            "quality_distribution": dict(quality_levels)
        }

    def analyze_dimensions(self) -> Dict:
        """按维度聚合统计"""
        dim_stats = {}

        for dim_id in self.DIMENSIONS:
            if dim_id == "content_quality":
                dim_stats[dim_id] = self._analyze_content_quality()
            else:
                dim_stats[dim_id] = self._analyze_process_dimension(dim_id)

        return dim_stats

    def _analyze_process_dimension(self, dim_id: str) -> Dict:
        """分析过程维度（format/business_rule/memory_management）"""
        total = 0
        passed = 0
        failed = 0
        skipped = 0
        pass_rates = []
        failed_samples = []

        for sample_id, cr in self.check_results.items():
            dim_scores = cr.get("dimension_scores", {})
            dim = dim_scores.get(dim_id, {})

            t = dim.get("total", 0)
            p = dim.get("passed", 0)
            f = dim.get("failed", 0)
            s = dim.get("skipped", 0)

            total += t
            passed += p
            failed += f
            skipped += s

            if t > 0:
                pr = p / t
                pass_rates.append(pr)
                if f > 0:
                    failed_items = dim.get("failed_items", [])
                    failed_samples.append({
                        "sample_id": sample_id,
                        "pass_rate": round(pr, 3),
                        "failed_count": f,
                        "failed_items": failed_items
                    })

        return {
            "dimension_name": self.DIMENSION_NAMES.get(dim_id, dim_id),
            "aggregate": {
                "total_checks": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "pass_rate": round(passed / total, 4) if total > 0 else 0
            },
            "per_sample_pass_rate": self._calc_stats(pass_rates),
            "failed_samples": sorted(failed_samples, key=lambda x: x["pass_rate"])
        }

    def _analyze_content_quality(self) -> Dict:
        """分析内容创作质量维度"""
        overall_scores = []
        gate_stats = {"total": 0, "passed": 0, "failed": 0, "triggered_count": 0}
        basic_stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
        advanced_stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}

        quality_levels = defaultdict(int)
        failed_samples = []

        for sample_id, cr in self.check_results.items():
            dim_scores = cr.get("dimension_scores", {})
            cq = dim_scores.get("content_quality", {})

            score = cq.get("overall_score")
            if score is not None:
                overall_scores.append(score)

            level = cq.get("quality_level", "unknown")
            quality_levels[level] += 1

            # Gate
            gate = cq.get("gate_layer", {})
            gate_stats["total"] += gate.get("total", 0)
            gate_stats["passed"] += gate.get("passed", 0)
            gate_stats["failed"] += gate.get("failed", 0)
            if cq.get("gate_triggered", False):
                gate_stats["triggered_count"] += 1

            # Basic
            basic = cq.get("basic_layer", {})
            basic_stats["total"] += basic.get("total", 0)
            basic_stats["passed"] += basic.get("passed", 0)
            basic_stats["failed"] += basic.get("failed", 0)
            basic_stats["skipped"] += basic.get("skipped", 0)

            # Advanced
            advanced = cq.get("advanced_layer", {})
            advanced_stats["total"] += advanced.get("total", 0)
            advanced_stats["passed"] += advanced.get("passed", 0)
            advanced_stats["failed"] += advanced.get("failed", 0)
            advanced_stats["skipped"] += advanced.get("skipped", 0)

            # 记录不合格样本
            if level in ["unqualified", "不合格"]:
                basic_failed_items = basic.get("failed_items", [])
                failed_samples.append({
                    "sample_id": sample_id,
                    "score": score,
                    "quality_level": level,
                    "gate_triggered": cq.get("gate_triggered", False),
                    "basic_failed_items": basic_failed_items
                })

        return {
            "dimension_name": "内容创作质量",
            "overall_score": self._calc_stats(overall_scores),
            "quality_distribution": dict(quality_levels),
            "gate_layer": {
                **gate_stats,
                "pass_rate": round(gate_stats["passed"] / gate_stats["total"], 4) if gate_stats["total"] > 0 else 1.0,
                "triggered_rate": round(gate_stats["triggered_count"] / len(self.check_results), 4) if self.check_results else 0
            },
            "basic_layer": {
                **basic_stats,
                "pass_rate": round(basic_stats["passed"] / basic_stats["total"], 4) if basic_stats["total"] > 0 else 0
            },
            "advanced_layer": {
                **advanced_stats,
                "pass_rate": round(advanced_stats["passed"] / advanced_stats["total"], 4) if advanced_stats["total"] > 0 else 0
            },
            "failed_samples": sorted(failed_samples, key=lambda x: x.get("score", 0))
        }

    def analyze_subcategories(self) -> Dict:
        """按子类聚合统计"""
        sub_stats = defaultdict(lambda: {
            "dimension_id": "",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "failed_samples": []
        })

        for sample_id, cr in self.check_results.items():
            check_details = cr.get("check_details", {})
            for check_name, detail in check_details.items():
                dim_id = detail.get("dimension_id", "unknown")
                sub_id = detail.get("subcategory_id", "unknown")
                result = detail.get("check_result", "skip")

                sub_stats[sub_id]["dimension_id"] = dim_id
                sub_stats[sub_id]["total"] += 1

                if result == "pass":
                    sub_stats[sub_id]["passed"] += 1
                elif result == "fail":
                    sub_stats[sub_id]["failed"] += 1
                    sub_stats[sub_id]["failed_samples"].append({
                        "sample_id": sample_id,
                        "check_name": check_name,
                        "reason": detail.get("reason", "")[:200]
                    })
                else:
                    sub_stats[sub_id]["skipped"] += 1

        # 计算通过率
        result = {}
        for sub_id, stats in sub_stats.items():
            effective = stats["passed"] + stats["failed"]
            stats["pass_rate"] = round(stats["passed"] / effective, 4) if effective > 0 else 0
            # 按维度分组
            dim_id = stats["dimension_id"]
            if dim_id not in result:
                result[dim_id] = {}
            result[dim_id][sub_id] = stats

        return result

    def analyze_by_writing_params(self) -> Dict:
        """按写作参数维度（模式/篇幅/基调）聚合统计"""
        # 按创作模式
        by_mode = defaultdict(list)
        # 按篇幅
        by_length = defaultdict(list)
        # 按基调/题材
        by_tone = defaultdict(list)

        for sample_id, cr in self.check_results.items():
            overall = cr.get("overall_result", {})
            ts = overall.get("total_score", 0)

            parts = self._parse_sample_id(sample_id)
            if parts.get("mode"):
                by_mode[parts["mode"]].append(ts)
            if parts.get("length"):
                by_length[parts["length"]].append(ts)
            if parts.get("tone"):
                by_tone[parts["tone"]].append(ts)

        length_order = {"ULTRA_SHORT": 0, "SHORT": 1, "MEDIUM": 2, "LONG": 3}

        return {
            "by_mode": {k: self._calc_stats(v) for k, v in sorted(by_mode.items())},
            "by_length": {k: self._calc_stats(v) for k, v in sorted(by_length.items(), key=lambda x: length_order.get(x[0], 99))},
            "by_tone": {k: self._calc_stats(v) for k, v in sorted(by_tone.items())}
        }

    def extract_failure_details(self, max_per_dimension: int = 5) -> Dict:
        """提取各维度的典型失败案例"""
        failures_by_dim = defaultdict(list)

        for sample_id, cr in self.check_results.items():
            check_details = cr.get("check_details", {})
            for check_name, detail in check_details.items():
                if detail.get("check_result") != "fail":
                    continue

                dim_id = detail.get("dimension_id", "unknown")
                sub_id = detail.get("subcategory_id", "unknown")

                failures_by_dim[dim_id].append({
                    "sample_id": sample_id,
                    "check_name": check_name,
                    "description": detail.get("description", ""),
                    "dimension_id": dim_id,
                    "subcategory_id": sub_id,
                    "quality_tier": detail.get("quality_tier", ""),
                    "reason": detail.get("reason", ""),
                    "details_preview": str(detail.get("details", ""))[:300]
                })

        # 每个维度只取前N个
        result = {}
        for dim_id, cases in failures_by_dim.items():
            result[dim_id] = cases[:max_per_dimension]

        return result

    # -- 辅助方法 -------------------------------------------------------

    def _parse_sample_id(self, sample_id: str) -> Dict:
        """解析sample_id中的各维度信息
        
        NW sample ID 格式:
        NW_CLEAR_SHORT_ANGSTY_001
        NW_CLEAR_MEDIUM_SUSPENSE_001
        NW_IP_MEDIUM_NEUTRAL_001
        NW_ULTRA_SHORT_ANGSTY_001
        """
        result = {}
        parts = sample_id.upper().split("_")

        # 跳过 NW 前缀
        if len(parts) < 2:
            return result

        # 处理 ULTRA_SHORT 的特殊情况：NW_ULTRA_SHORT_ANGSTY_001
        # 此时没有 mode 字段，ULTRA_SHORT 是篇幅
        remaining = parts[1:]  # 去掉 NW

        if remaining and remaining[0] == "ULTRA" and len(remaining) > 1 and remaining[1] == "SHORT":
            # NW_ULTRA_SHORT_xxx_NNN — 没有 mode 字段
            result["length"] = "ULTRA_SHORT"
            remaining = remaining[2:]
        elif remaining and remaining[0] in ("CLEAR", "IP", "VAGUE"):
            # NW_CLEAR_SHORT_xxx_NNN / NW_IP_MEDIUM_xxx_NNN / NW_VAGUE_MEDIUM_xxx_NNN
            result["mode"] = remaining[0]
            remaining = remaining[1:]
            # 篇幅
            if remaining and remaining[0] in ("SHORT", "MEDIUM", "LONG"):
                result["length"] = remaining[0]
                remaining = remaining[1:]
        elif remaining and remaining[0] in ("SHORT", "MEDIUM", "LONG"):
            # NW_SHORT_xxx_NNN — 没有 mode 字段
            result["length"] = remaining[0]
            remaining = remaining[1:]

        # 基调/题材: ANGSTY / SWEET / SUSPENSE / NEUTRAL / ADVENTURE / etc.
        if remaining:
            # 最后一个是序号（如 001），倒数第二个（或多个词）是基调
            # 但可能是 BRAINY_ACTION_001 / SWEET_DRAMA_001 这种多词基调
            if remaining[-1].isdigit() or (len(remaining[-1]) == 3 and remaining[-1].isdigit()):
                tone_parts = remaining[:-1]
            else:
                tone_parts = remaining
            if tone_parts:
                result["tone"] = "_".join(tone_parts)

        return result

    def _calc_stats(self, values: List[float]) -> Dict:
        """计算统计量"""
        if not values:
            return {"mean": 0, "min": 0, "max": 0, "count": 0}

        return {
            "mean": round(sum(values) / len(values), 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "count": len(values)
        }

    # -- 报告生成 -------------------------------------------------------

    def generate_json_report(self, output_file: Path) -> Dict:
        """生成JSON格式报告"""
        print("\n正在生成统计报告...")

        overview = self.analyze_overview()
        dimensions = self.analyze_dimensions()
        subcategories = self.analyze_subcategories()
        by_writing_params = self.analyze_by_writing_params()
        failure_details = self.extract_failure_details()

        # 确定使用了哪些revision
        revisions_used = set(self.check_revision_used.values())

        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "model": self.model_name,
                "eval_dir": self.eval_dir,
                "scenario": "novel_writing_alchemist",
                "revision_filter": self.revision or "latest",
                "revisions_used": sorted(revisions_used)
            },
            "overview": overview,
            "dimensions": dimensions,
            "subcategories": subcategories,
            "by_writing_params": by_writing_params,
            "failure_details": failure_details
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"+ JSON报告已生成: {output_file}")
        return report

    def generate_markdown_report(self, output_file: Path, report: Dict):
        """生成Markdown格式报告"""
        lines = []
        meta = report["metadata"]
        ov = report["overview"]
        dims = report["dimensions"]

        lines.append(f"# Novel Writing Alchemist 评测统计报告")
        lines.append(f"")
        lines.append(f"- **模型**: `{meta['model']}`")
        lines.append(f"- **生成时间**: {meta['generated_at']}")
        lines.append(f"- **评测目录**: `{meta['eval_dir']}`")
        lines.append(f"- **Revision**: `{meta['revision_filter']}` (实际: {', '.join(meta['revisions_used'])})")
        lines.append(f"")

        # -- 总览 --
        lines.append(f"## 1. 总览")
        lines.append(f"")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 总样本数 | {ov['total_samples']} |")
        lines.append(f"| 成功执行 | {ov['success_samples']} |")
        lines.append(f"| 执行错误 | {ov['error_samples']} |")
        lines.append(f"| 有checker结果 | {ov['checked_samples']} |")
        lines.append(f"")

        scores = ov["scores"]
        lines.append(f"### 1.1 总分统计")
        lines.append(f"")
        lines.append(f"| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |")
        lines.append(f"|----------|--------|--------|--------|--------|")
        for score_type, label in [("total", "加权总分"), ("content", "内容分(x0.7)"), ("process", "过程分(x0.3)")]:
            s = scores[score_type]
            lines.append(f"| {label} | {s['mean']:.2f} | {s['min']:.2f} | {s['max']:.2f} | {s['count']} |")
        lines.append(f"")

        # 质量分布
        qd = ov.get("quality_distribution", {})
        if qd:
            lines.append(f"### 1.2 质量等级分布")
            lines.append(f"")
            lines.append(f"| 等级 | 数量 | 占比 |")
            lines.append(f"|------|------|------|")
            total_q = sum(qd.values())
            for level in ["excellent", "qualified", "unqualified", "Good", "Fair", "Poor", "unknown"]:
                if level in qd:
                    pct = qd[level] / total_q * 100 if total_q > 0 else 0
                    lines.append(f"| {level} | {qd[level]} | {pct:.1f}% |")
            lines.append(f"")

        # -- 维度统计 --
        lines.append(f"## 2. 能力维度统计")
        lines.append(f"")

        # 过程维度
        lines.append(f"### 2.1 过程维度")
        lines.append(f"")
        lines.append(f"| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |")
        lines.append(f"|------|----------|------|------|------|--------|")
        for dim_id in ["format_compliance", "business_rule_compliance", "memory_management"]:
            d = dims.get(dim_id, {})
            agg = d.get("aggregate", {})
            name = d.get("dimension_name", dim_id)
            pr = agg.get("pass_rate", 0) * 100
            lines.append(f"| {name} | {agg.get('total_checks', 0)} | {agg.get('passed', 0)} | {agg.get('failed', 0)} | {agg.get('skipped', 0)} | {pr:.1f}% |")
        lines.append(f"")

        # 内容质量维度
        cq = dims.get("content_quality", {})
        if cq:
            lines.append(f"### 2.2 内容创作质量")
            lines.append(f"")
            cq_score = cq.get("overall_score", {})
            lines.append(f"- **平均内容分**: {cq_score.get('mean', 0):.2f} (范围: {cq_score.get('min', 0):.2f} ~ {cq_score.get('max', 0):.2f})")
            lines.append(f"")

            lines.append(f"#### 质量层级通过率")
            lines.append(f"")
            lines.append(f"| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |")
            lines.append(f"|------|----------|------|------|------|--------|")
            for tier, label in [("gate_layer", "Gate(门控)"), ("basic_layer", "Basic(基础)"), ("advanced_layer", "Advanced(优秀)")]:
                t = cq.get(tier, {})
                pr = t.get("pass_rate", 0) * 100
                lines.append(f"| {label} | {t.get('total', 0)} | {t.get('passed', 0)} | {t.get('failed', 0)} | {t.get('skipped', 0)} | {pr:.1f}% |")
            lines.append(f"")

            # gate触发情况
            gate = cq.get("gate_layer", {})
            lines.append(f"- **Gate触发率**: {gate.get('triggered_rate', 0)*100:.1f}% ({gate.get('triggered_count', 0)}/{len(self.check_results)})")
            lines.append(f"")

        # -- 子类统计 --
        sub = report.get("subcategories", {})
        if sub:
            lines.append(f"## 3. 子类维度统计")
            lines.append(f"")
            for dim_id in self.DIMENSIONS:
                dim_subs = sub.get(dim_id, {})
                if not dim_subs:
                    continue
                dim_name = self.DIMENSION_NAMES.get(dim_id, dim_id)
                lines.append(f"### {dim_name}")
                lines.append(f"")
                lines.append(f"| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |")
                lines.append(f"|------|--------|------|------|------|--------|")
                for sub_id, stats in sorted(dim_subs.items(), key=lambda x: x[1].get("pass_rate", 0)):
                    pr = stats.get("pass_rate", 0) * 100
                    lines.append(f"| {sub_id} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['skipped']} | {pr:.1f}% |")
                lines.append(f"")

        # -- 按写作参数统计 --
        by_wp = report.get("by_writing_params", {})
        if by_wp:
            lines.append(f"## 4. 按写作参数统计")
            lines.append(f"")

            for dim_key, dim_label in [("by_mode", "创作模式"), ("by_length", "篇幅"), ("by_tone", "基调/题材")]:
                dim_data = by_wp.get(dim_key, {})
                if not dim_data:
                    continue
                lines.append(f"### {dim_label}")
                lines.append(f"")
                lines.append(f"| {dim_label} | 样本数 | 平均总分 | 最低分 | 最高分 |")
                lines.append(f"|------|--------|----------|--------|--------|")
                for k, v in dim_data.items():
                    lines.append(f"| {k} | {v['count']} | {v['mean']:.2f} | {v['min']:.2f} | {v['max']:.2f} |")
                lines.append(f"")

        # -- 失败案例索引 --
        failures = report.get("failure_details", {})
        if failures:
            lines.append(f"## 5. 失败案例索引")
            lines.append(f"")
            for dim_id, cases in failures.items():
                dim_name = self.DIMENSION_NAMES.get(dim_id, dim_id)
                lines.append(f"### {dim_name} ({len(cases)}个失败检查)")
                lines.append(f"")
                for case in cases:
                    lines.append(f"- **{case['sample_id']}** / `{case['check_name']}`")
                    lines.append(f"  - 子类: {case['subcategory_id']}, 层级: {case.get('quality_tier', 'N/A')}")
                    lines.append(f"  - 原因: {case['reason'][:150]}")
                    lines.append(f"")

        # 写入文件
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"+ Markdown报告已生成: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Novel Writing Alchemist 评测统计分析")
    parser.add_argument("--eval-dir", required=True, help="评测结果目录名")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--remote-url", default=None, help="远程HTTP API地址 (如 http://10.25.70.163:9090)")
    parser.add_argument("--revision", default=None, help="指定check_result的revision版本 (如 rev008)，默认自动选最新")
    args = parser.parse_args()

    # 选择reader
    if args.remote_url:
        print(f"使用远程模式: {args.remote_url}")
        reader = RemoteReader(args.remote_url)
    else:
        # 本地模式：eval_dir的父目录作为base
        eval_path = Path(args.eval_dir)
        if eval_path.is_absolute():
            base_dir = eval_path.parent.parent  # evaluation_outputs的父目录
            reader = LocalReader(str(base_dir))
        else:
            reader = LocalReader(".")
        print(f"使用本地模式")

    # 创建分析器
    analyzer = NWStatisticsAnalyzer(reader, args.eval_dir, revision=args.revision)
    analyzer.load_data()

    if not analyzer.check_results:
        print("\n--- 没有找到任何有效的check结果，请检查：")
        print("  1. eval-dir 是否正确")
        print("  2. checker 是否已运行")
        print("  3. check_result*.json 是否存在于 _env 目录中")
        if args.revision:
            print(f"  4. 指定的 revision '{args.revision}' 是否存在")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成JSON报告
    json_file = output_dir / "statistics.json"
    report = analyzer.generate_json_report(json_file)

    # 生成Markdown报告
    md_file = output_dir / "statistics.md"
    analyzer.generate_markdown_report(md_file, report)

    print(f"\n=== 统计报告生成完成!")
    print(f"  JSON: {json_file}")
    print(f"  Markdown: {md_file}")


if __name__ == "__main__":
    main()
