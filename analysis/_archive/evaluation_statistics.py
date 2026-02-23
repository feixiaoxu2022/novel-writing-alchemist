#!/usr/bin/env python3
"""
评测结果统计分析脚本
对比多个模型在Layer1（dimension_id）、Layer2（subcategory_id）、Checklist三个级别上的表现

用法:
    python evaluation_statistics.py                    # 默认使用check_result_v4.json
    python evaluation_statistics.py --version v3      # 使用check_result_v3.json
    python evaluation_statistics.py --version v4      # 使用check_result_v4.json
    python evaluation_statistics.py -v v3             # 简写形式
"""

import json
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict
import pandas as pd
import yaml
from typing import Dict, List, Any, Optional, Tuple
import re


def _check_id_sort_key(check_id: str):
    """check_id 排序辅助函数，兼容新旧两种格式。
    
    - 旧格式 "检查项26" → (0, 26, "")  按数字排序
    - 新格式 "逻辑硬伤"  → (1, 0, "逻辑硬伤")  按字符串排序，排在旧格式之后
    """
    m = re.match(r'^检查项(\d+)$', check_id)
    if m:
        return (0, int(m.group(1)), "")
    return (1, 0, check_id)


class EvaluationStatistics:
    """评测结果统计分析器"""

    # ================================================================
    # 元数据映射：从 check_capability_taxonomy.yaml 自动加载
    # 不再手动维护，新增/修改 check item 只需更新 taxonomy.yaml
    # ================================================================

    # 默认taxonomy路径（相对于本文件）
    _TAXONOMY_PATH = Path(__file__).parent.parent / 'check_capability_taxonomy.yaml'

    @classmethod
    def _load_taxonomy(cls, taxonomy_path: Optional[Path] = None) -> Tuple[dict, dict, dict]:
        """
        从 check_capability_taxonomy.yaml 加载三个映射：
        1. SUBCATEGORY_CN_NAMES: {subcategory_id: "人话描述"}
        2. SUBCATEGORY_CHECK_TYPE: {subcategory_id: "rule" | "semantic"}
        3. LAYER2_SORT_ORDER: {(dimension_id, subcategory_id): (major, minor)}
        """
        path = taxonomy_path or cls._TAXONOMY_PATH
        if not path.exists():
            raise FileNotFoundError(
                f"Taxonomy文件不存在: {path}\n"
                f"请确保 check_capability_taxonomy.yaml 在 check_definitions/ 目录下"
            )

        with open(path, 'r', encoding='utf-8') as f:
            taxonomy = yaml.safe_load(f)

        cn_names = {}
        check_types = {}
        sort_order = {}
        errors = []  # 收集所有缺失字段，一次性报错

        for dim in taxonomy.get('capability_dimensions', []):
            dim_id = dim['dimension_id']
            for subcat in dim.get('subcategories', []):
                sid = subcat['subcategory_id']

                # cn_name（人话描述）— 严格要求，缺失即报错
                cn_name = subcat.get('cn_name')
                if not cn_name:
                    errors.append(
                        f"[{dim_id}/{sid}] 缺少 cn_name（人话描述），"
                        f"请在 check_capability_taxonomy.yaml 中补充"
                    )
                else:
                    cn_names[sid] = cn_name

                # check_types 列表 — 严格要求，缺失即报错
                ctypes = subcat.get('check_types')
                if not ctypes or not isinstance(ctypes, list) or len(ctypes) == 0:
                    errors.append(
                        f"[{dim_id}/{sid}] 缺少 check_types 列表，"
                        f"请在 check_capability_taxonomy.yaml 中补充"
                    )
                else:
                    # 包含 semantic_check → semantic，否则 → rule
                    if 'semantic_check' in ctypes:
                        check_types[sid] = 'semantic'
                    else:
                        check_types[sid] = 'rule'

                # sort_order — 严格要求，缺失或格式错误即报错
                so = subcat.get('sort_order')
                if not so or not isinstance(so, list) or len(so) != 2:
                    errors.append(
                        f"[{dim_id}/{sid}] 缺少或格式错误的 sort_order（需要 [major, minor] 二元组），"
                        f"请在 check_capability_taxonomy.yaml 中补充"
                    )
                else:
                    sort_order[(dim_id, sid)] = tuple(so)

        # 有任何缺失字段则一次性报错，列出所有问题
        if errors:
            error_msg = (
                f"check_capability_taxonomy.yaml 元数据不完整，"
                f"共 {len(errors)} 处缺失：\n"
                + "\n".join(f"  - {e}" for e in errors)
            )
            raise ValueError(error_msg)

        return cn_names, check_types, sort_order

    # 类级别缓存（首次访问时加载）
    _cn_names_cache = None
    _check_types_cache = None
    _sort_order_cache = None

    @classmethod
    def _ensure_loaded(cls):
        """确保元数据已加载（懒加载 + 缓存）"""
        if cls._cn_names_cache is None:
            cls._cn_names_cache, cls._check_types_cache, cls._sort_order_cache = cls._load_taxonomy()

    @classmethod
    def get_cn_names(cls) -> dict:
        cls._ensure_loaded()
        assert cls._cn_names_cache is not None
        return cls._cn_names_cache

    @classmethod
    def get_check_types(cls) -> dict:
        cls._ensure_loaded()
        assert cls._check_types_cache is not None
        return cls._check_types_cache

    @classmethod
    def get_sort_order(cls) -> dict:
        cls._ensure_loaded()
        assert cls._sort_order_cache is not None
        return cls._sort_order_cache

    # ULTRA_SHORT 篇幅不适用的流程检查 subcategory（统计时视为 skip）
    ULTRA_SHORT_SKIP_SUBCATEGORIES = {
        "sop_compliance",
        "log_file_usage",
        "log_file_creation",
        "required_skill_reading",
    }

    def __init__(self, evaluation_outputs_dir: str, check_result_filename: str = 'check_result_v4.json',
                 batch_prefix: str = 'eval_dsv1'):
        self.evaluation_outputs_dir = Path(evaluation_outputs_dir)
        self.check_result_filename = check_result_filename
        self.batch_prefix = batch_prefix
        self.model_data = {}  # {model_name: [check_result_1, check_result_2, ...]}
        self.model_total_samples = {}  # {model_name: 总样本目录数}

    def load_all_results(self):
        """加载所有模型的评测结果"""
        eval_dirs = [d for d in self.evaluation_outputs_dir.iterdir()
                     if d.is_dir() and d.name.startswith(f'{self.batch_prefix}_')]

        print(f"样本批次前缀: {self.batch_prefix}_")
        print(f"使用check_result文件: {self.check_result_filename}")

        for eval_dir in eval_dirs:
            # 从目录名提取模型名称
            # eval_dsv1_20260205_132400_claude-opus-4-5-20251101 -> claude-opus-4-5-20251101
            # 前缀部分的下划线数 + 时间戳2段 = 跳过的段数
            prefix_parts = len(self.batch_prefix.split('_'))  # eval_dsv1 -> 2
            model_name = '_'.join(eval_dir.name.split('_')[prefix_parts + 2:])

            print(f"加载模型: {model_name}")

            # 统计所有样本目录（不管有没有check_result）
            all_env_dirs = [d for d in eval_dir.iterdir() if d.is_dir() and d.name.endswith('_env')]
            total_sample_count = len(all_env_dirs)

            # 查找所有样本的check_result文件
            sample_results = []
            for sample_dir in all_env_dirs:
                    # 使用参数化的文件名
                    check_result_file = sample_dir / self.check_result_filename

                    if check_result_file.exists():
                        with open(check_result_file, 'r', encoding='utf-8') as f:
                            result = json.load(f)
                            sample_results.append(result)

            self.model_data[model_name] = sample_results
            self.model_total_samples[model_name] = total_sample_count

            no_check_result = total_sample_count - len(sample_results)
            print(f"  总样本目录: {total_sample_count}")
            print(f"  有{self.check_result_filename}: {len(sample_results)}")
            if no_check_result > 0:
                print(f"  ⚠️  无{self.check_result_filename}: {no_check_result}")

        # 后处理：ULTRA_SHORT 样本中不适用的流程检查项标记为 skip
        # 同时修正 dimension_scores 和 overall_result 中的聚合值
        patched_count = 0
        for model_name, results in self.model_data.items():
            for result in results:
                sample_id = result.get("sample_id", "")
                if "ULTRA_SHORT" not in sample_id:
                    continue
                check_details = result.get("check_details", {})
                for check_id, info in check_details.items():
                    subcat = info.get("subcategory_id", "")
                    if subcat in self.ULTRA_SHORT_SKIP_SUBCATEGORIES and info.get("check_result") != "skip":
                        info["check_result"] = "skip"
                        info["reason"] = "ULTRA_SHORT篇幅不适用"
                        patched_count += 1

                # 从 check_details 重算 dimension_scores 和 overall_result
                dim_counts = defaultdict(lambda: {"passed": 0, "failed": 0, "total": 0})
                for check_id, info in check_details.items():
                    cr = info.get("check_result", "")
                    dim = info.get("dimension_id", "")
                    if cr == "skip" or not dim:
                        continue
                    dim_counts[dim]["total"] += 1
                    if cr == "pass":
                        dim_counts[dim]["passed"] += 1
                    else:
                        dim_counts[dim]["failed"] += 1

                ds = result.get("dimension_scores", {})
                for dim in ["format_compliance", "business_rule_compliance", "memory_management"]:
                    if dim in ds and dim in dim_counts:
                        c = dim_counts[dim]
                        ds[dim]["passed"] = c["passed"]
                        ds[dim]["total"] = c["total"]
                        ds[dim]["failed"] = c["failed"]
                        ds[dim]["pass_rate"] = c["passed"] / c["total"] if c["total"] > 0 else 0

                # 重算 overall_result 的 pass_rate/passed/total
                overall = result.get("overall_result", {})
                all_passed = sum(c["passed"] for c in dim_counts.values())
                all_total = sum(c["total"] for c in dim_counts.values())
                # content_quality 的 passed/total 也要从 check_details 重算
                cq_ds = ds.get("content_quality", {})
                if cq_ds:
                    # basic_layer 和 advanced_layer 的 passed/total 不受影响（无 skip 变更）
                    # 但 overall_result 的 pass_rate 需要包含 content_quality
                    bl = cq_ds.get("basic_layer", {})
                    al = cq_ds.get("advanced_layer", {})
                    gl = cq_ds.get("gate_layer", {})
                    cq_passed = gl.get("passed", 0) + bl.get("passed", 0) + al.get("passed", 0)
                    cq_total = gl.get("total", 0) + bl.get("total", 0) + al.get("total", 0)
                    all_passed += cq_passed
                    all_total += cq_total

                overall["passed_checks"] = all_passed
                overall["total_checks"] = all_total
                overall["pass_rate"] = all_passed / all_total if all_total > 0 else 0

                # 重算流程规范分
                proc_rates = []
                for dim in ["format_compliance", "business_rule_compliance", "memory_management"]:
                    if dim in ds and ds[dim].get("total", 0) > 0:
                        proc_rates.append(ds[dim]["passed"] / ds[dim]["total"])
                if proc_rates:
                    overall["process_score"] = sum(proc_rates) / len(proc_rates) * 100

        if patched_count > 0:
            print(f"\n[篇幅自适应] ULTRA_SHORT 样本中 {patched_count} 个不适用检查项已标记为 skip")

        print(f"\n总共加载了 {len(self.model_data)} 个模型的数据")

    def compute_layer1_statistics(self) -> pd.DataFrame:
        """
        统计Layer1级别（dimension_id）的表现
        统计所有有check_result的样本
        返回DataFrame: columns=[dimension_id, model1_pass_rate, model1_passed, model1_total, ...]
        
        注意：skip状态的检查项不计入分母（total），只统计pass和fail
        """
        layer1_stats = defaultdict(lambda: defaultdict(list))

        for model_name, results in self.model_data.items():
            for result in results:
                dimension_scores = result.get('dimension_scores', {})

                # 处理普通维度（format_compliance, business_rule_compliance, memory_management）
                for dim_id in ['format_compliance', 'business_rule_compliance', 'memory_management']:
                    if dim_id in dimension_scores:
                        dim_data = dimension_scores[dim_id]
                        layer1_stats[dim_id][f'{model_name}_pass_rate'].append(dim_data.get('pass_rate', 0))
                        layer1_stats[dim_id][f'{model_name}_passed'].append(dim_data.get('passed', 0))
                        layer1_stats[dim_id][f'{model_name}_total'].append(dim_data.get('total', 0))

                # 处理content_quality（特殊结构）
                if 'content_quality' in dimension_scores:
                    cq_data = dimension_scores['content_quality']
                    basic_layer = cq_data.get('basic_layer', {})
                    layer1_stats['content_quality'][f'{model_name}_pass_rate'].append(basic_layer.get('pass_rate', 0))
                    layer1_stats['content_quality'][f'{model_name}_passed'].append(basic_layer.get('passed', 0))
                    layer1_stats['content_quality'][f'{model_name}_total'].append(basic_layer.get('total', 0))

        # 计算平均值和总计
        rows = []
        for dim_id, model_stats in layer1_stats.items():
            row = {'dimension_id': dim_id}
            for metric, values in model_stats.items():
                if 'passed' in metric or 'total' in metric:
                    # passed和total求和
                    row[metric] = sum(values) if values else 0
                else:
                    # pass_rate求平均
                    row[metric] = sum(values) / len(values) if values else 0
            rows.append(row)

        df = pd.DataFrame(rows)
        # 重新排列列的顺序，只包含有数据的模型
        if not df.empty:
            cols = ['dimension_id']
            # 只选择有数据的模型
            model_names = sorted([name for name, results in self.model_data.items() if len(results) > 0])
            for model_name in model_names:
                pass_rate_col = f'{model_name}_pass_rate'
                passed_col = f'{model_name}_passed'
                total_col = f'{model_name}_total'
                if all(col in df.columns for col in [pass_rate_col, passed_col, total_col]):
                    cols.extend([pass_rate_col, passed_col, total_col])
            df = pd.DataFrame(df[cols])

        return df

    def compute_layer2_statistics(self) -> pd.DataFrame:
        """
        统计Layer2级别（subcategory_id）的表现
        统计所有有check_result的样本
        返回DataFrame: columns=[dimension_id, subcategory_id, model1_pass_rate, model2_pass_rate, ...]
        
        注意：skip状态的检查项不计入分母（total），只统计pass和fail
        """
        layer2_stats = defaultdict(lambda: defaultdict(lambda: {'passed': 0, 'total': 0, 'skipped': 0}))

        for model_name, results in self.model_data.items():
            for result in results:
                check_details = result.get('check_details', {})

                for check_id, check_info in check_details.items():
                    dimension_id = check_info.get('dimension_id')
                    subcategory_id = check_info.get('subcategory_id')
                    check_result = check_info.get('check_result')

                    if dimension_id and subcategory_id:
                        key = (dimension_id, subcategory_id)
                        # skip状态的检查项不计入分母，只记录skip数量
                        if check_result == 'skip':
                            layer2_stats[key][model_name]['skipped'] += 1
                        else:
                            # 只有pass和fail才计入统计
                            layer2_stats[key][model_name]['total'] += 1
                            if check_result == 'pass':
                                layer2_stats[key][model_name]['passed'] += 1

        # 按自定义顺序排序：同dimension内按逻辑分组 + 由浅入深递进
        def layer2_sort_key(item):
            key = item[0]  # (dim_id, subcat_id)
            return self.get_sort_order().get(key, (99, 99))

        rows = []
        for (dim_id, subcat_id), model_stats in sorted(layer2_stats.items(), key=layer2_sort_key):
            row = {
                'dimension_id': dim_id,
                'subcategory_id': subcat_id
            }
            for model_name in sorted(self.model_data.keys()):
                stats = model_stats[model_name]
                pass_rate = stats['passed'] / stats['total'] if stats['total'] > 0 else 0
                row[f'{model_name}_pass_rate'] = pass_rate
                row[f'{model_name}_passed'] = stats['passed']
                row[f'{model_name}_total'] = stats['total']
            rows.append(row)

        df = pd.DataFrame(rows)
        return df

    def compute_checklist_statistics(self) -> pd.DataFrame:
        """
        统计Checklist级别（具体检查项）的表现
        统计所有有check_result的样本
        返回DataFrame: columns=[check_id, description, dimension_id, subcategory_id, model1_pass_rate, ...]
        
        注意：skip状态的检查项不计入分母（total），只统计pass和fail
        """
        checklist_stats = defaultdict(lambda: defaultdict(lambda: {'passed': 0, 'total': 0, 'skipped': 0}))
        check_metadata = {}  # 存储检查项的元数据

        for model_name, results in self.model_data.items():
            for result in results:
                check_details = result.get('check_details', {})

                for check_id, check_info in check_details.items():
                    # 收集元数据
                    if check_id not in check_metadata:
                        check_metadata[check_id] = {
                            'description': check_info.get('description', ''),
                            'dimension_id': check_info.get('dimension_id', ''),
                            'subcategory_id': check_info.get('subcategory_id', ''),
                            'is_critical': check_info.get('is_critical', False)
                        }

                    # 统计通过情况
                    check_result = check_info.get('check_result')
                    # skip状态的检查项不计入分母，只记录skip数量
                    if check_result == 'skip':
                        checklist_stats[check_id][model_name]['skipped'] += 1
                    else:
                        # 只有pass和fail才计入统计
                        checklist_stats[check_id][model_name]['total'] += 1
                        if check_result == 'pass':
                            checklist_stats[check_id][model_name]['passed'] += 1

        # 计算通过率
        rows = []
        for check_id in sorted(checklist_stats.keys(), key=lambda x: _check_id_sort_key(x)):
            metadata = check_metadata[check_id]
            row = {
                'check_id': check_id,
                'description': metadata['description'],
                'dimension_id': metadata['dimension_id'],
                'subcategory_id': metadata['subcategory_id'],
                'is_critical': metadata['is_critical']
            }

            for model_name in sorted(self.model_data.keys()):
                stats = checklist_stats[check_id][model_name]
                pass_rate = stats['passed'] / stats['total'] if stats['total'] > 0 else 0
                row[f'{model_name}_pass_rate'] = pass_rate
                row[f'{model_name}_passed'] = stats['passed']
                row[f'{model_name}_total'] = stats['total']

            rows.append(row)

        df = pd.DataFrame(rows)
        return df

    def generate_summary_report(self) -> Dict[str, Any]:
        """生成汇总报告"""
        summary = {}

        for model_name, results in self.model_data.items():
            total_sample_dirs = self.model_total_samples.get(model_name, 0)
            has_check_result = len(results)
            no_check_result = total_sample_dirs - has_check_result

            model_summary = {
                'total_sample_dirs': total_sample_dirs,
                'has_check_result': has_check_result,
                'no_check_result': no_check_result,
                'avg_pass_rate': 0,
                'avg_total_score': 0,
                'avg_content_score': 0,
                'avg_process_score': 0,
                'status_distribution': defaultdict(int),
                'good_or_fair_count': 0,
                'poor_count': 0
            }

            pass_rates = []
            total_scores = []
            content_scores = []
            process_scores = []

            for result in results:
                overall = result.get('overall_result', {})

                pass_rates.append(overall.get('pass_rate', 0))
                total_scores.append(overall.get('total_score', 0))
                content_scores.append(overall.get('content_score', 0))
                process_scores.append(overall.get('process_score', 0))
                status = overall.get('status', 'Unknown')
                model_summary['status_distribution'][status] += 1

                if status in ['Good', 'Fair']:
                    model_summary['good_or_fair_count'] += 1
                elif status == 'Poor':
                    model_summary['poor_count'] += 1

            model_summary['avg_pass_rate'] = sum(pass_rates) / len(pass_rates) if pass_rates else 0
            model_summary['avg_total_score'] = sum(total_scores) / len(total_scores) if total_scores else 0
            model_summary['avg_content_score'] = sum(content_scores) / len(content_scores) if content_scores else 0
            model_summary['avg_process_score'] = sum(process_scores) / len(process_scores) if process_scores else 0

            summary[model_name] = model_summary

        return summary

    def compute_logic_flaw_analysis(self) -> Dict[str, Any]:
        """
        从 check_result 的 flaws 结构化字段提取逻辑硬伤细分数据。
        
        返回: {model_name: {
            'fail_count': int,          # 逻辑硬伤 fail 的样本数
            'structured_count': int,    # 其中有 flaws 结构化数据的数量
            'total_flaws': int,         # 硬伤总数
            'avg_flaws_per_fail': float,# 平均每个 fail 样本的硬伤数
            'type_distribution': {type: count},
            'severity_distribution': {severity: count}
        }}
        
        如果所有模型都没有 flaws 数据，返回空 dict。
        """
        analysis = {}
        has_any_flaws = False

        for model_name, results in self.model_data.items():
            fail_count = 0
            structured_count = 0
            total_flaws = 0
            type_dist: Dict[str, int] = defaultdict(int)
            severity_dist: Dict[str, int] = defaultdict(int)

            for result in results:
                check_details = result.get('check_details', {})
                for check_id, check_info in check_details.items():
                    if check_info.get('subcategory_id') != 'logical_contradiction':
                        continue
                    if check_info.get('check_result') != 'fail':
                        continue

                    fail_count += 1
                    flaws = check_info.get('flaws')
                    if flaws and isinstance(flaws, list):
                        structured_count += 1
                        has_any_flaws = True
                        total_flaws += len(flaws)
                        for flaw in flaws:
                            if isinstance(flaw, dict):
                                ftype = flaw.get('type', 'unknown')
                                severity = flaw.get('severity', 'unknown')
                                type_dist[ftype] += 1
                                severity_dist[severity] += 1

            if fail_count > 0:
                analysis[model_name] = {
                    'fail_count': fail_count,
                    'structured_count': structured_count,
                    'total_flaws': total_flaws,
                    'avg_flaws_per_fail': total_flaws / structured_count if structured_count > 0 else 0,
                    'type_distribution': dict(type_dist),
                    'severity_distribution': dict(severity_dist)
                }

        # 如果没有任何模型有 flaws 结构化数据，返回空 dict（不生成 section）
        if not has_any_flaws:
            return {}

        return analysis

    # ================================================================
    # 诊断分析方法：因果归因
    # ================================================================

    # Gate 检查项的 subcategory_id
    GATE_SUBCATEGORIES = {"chapter_cloning", "alternating_repetition", "chapter_completion"}

    def _get_length_tier(self, sample_id: str) -> str:
        """从 sample_id 提取篇幅标签"""
        if "ULTRA_SHORT" in sample_id:
            return "ULTRA_SHORT"
        elif "MEDIUM" in sample_id:
            return "MEDIUM"
        elif "SHORT" in sample_id:
            return "SHORT"
        return "OTHER"

    def _compute_sample_score_parts(self, result: dict) -> dict:
        """
        计算单个样本的分数拆解（与打分公式完全一致）。
        返回: {
            'content_score': float, 'gate_penalty': float,
            'basic_deduction': float, 'advanced_bonus': float,
            'gate_failed_subcats': list, 'basic_failed_subcats': list,
            'advanced_passed_subcats': list, 'advanced_failed_subcats': list,
            'gate_triggered': bool, 'process_score': float, 'total_score': float,
        }
        """
        cq = result.get('dimension_scores', {}).get('content_quality', {})
        gate = cq.get('gate_layer', {})
        basic = cq.get('basic_layer', {})
        adv = cq.get('advanced_layer', {})

        g_penalty = gate.get('failed', 0) * 20.0
        b_total = basic.get('total', 0)
        b_per_item = 60.0 / b_total if b_total > 0 else 0
        b_deduction = basic.get('failed', 0) * b_per_item
        a_total = adv.get('total', 0)
        a_per_item = 40.0 / a_total if a_total > 0 else 0
        a_bonus = adv.get('passed', 0) * a_per_item

        content_score = max(0, min(100, 60.0 - g_penalty - b_deduction + a_bonus))

        # 流程规范分
        ds = result.get('dimension_scores', {})
        proc_rates = []
        for dim in ["format_compliance", "business_rule_compliance", "memory_management"]:
            d = ds.get(dim, {})
            if d.get("total", 0) > 0:
                proc_rates.append(d["passed"] / d["total"])
        process_score = (sum(proc_rates) / len(proc_rates) * 100) if proc_rates else 0
        total_score = content_score * 0.7 + process_score * 0.3

        # 按 subcategory 聚合 fail/pass 项
        check_details = result.get('check_details', {})
        gate_failed_subcats = []
        basic_failed_subcats = []
        adv_passed_subcats = []
        adv_failed_subcats = []

        # 统计每个 subcategory 的 fail/pass（去重，一个 subcategory 可能有多个 check）
        subcat_results = defaultdict(lambda: {'passed': 0, 'failed': 0, 'total': 0})
        for check_id, info in check_details.items():
            if info.get('dimension_id') != 'content_quality':
                continue
            if info.get('check_result') == 'skip':
                continue
            subcat = info.get('subcategory_id', '')
            tier = info.get('quality_tier', '')
            subcat_results[(subcat, tier)]['total'] += 1
            if info.get('check_result') == 'pass':
                subcat_results[(subcat, tier)]['passed'] += 1
            else:
                subcat_results[(subcat, tier)]['failed'] += 1

        for (subcat, tier), counts in subcat_results.items():
            if subcat in self.GATE_SUBCATEGORIES:
                if counts['failed'] > 0:
                    gate_failed_subcats.append(subcat)
            elif tier == 'basic':
                if counts['failed'] > 0:
                    basic_failed_subcats.append(subcat)
            elif tier == 'advanced':
                if counts['failed'] > 0:
                    adv_failed_subcats.append(subcat)
                if counts['passed'] > 0:
                    adv_passed_subcats.append(subcat)

        return {
            'content_score': content_score,
            'gate_penalty': g_penalty,
            'basic_deduction': b_deduction,
            'advanced_bonus': a_bonus,
            'gate_failed_subcats': gate_failed_subcats,
            'basic_failed_subcats': basic_failed_subcats,
            'advanced_passed_subcats': adv_passed_subcats,
            'advanced_failed_subcats': adv_failed_subcats,
            'gate_triggered': gate.get('failed', 0) > 0,
            'process_score': process_score,
            'total_score': total_score,
            'b_per_item': b_per_item,
            'a_per_item': a_per_item,
        }

    def compute_deduction_attribution(self) -> Dict[str, Any]:
        """
        扣分归因表：按 subcategory 拆解每个模型的平均扣分贡献。
        
        返回: {model_name: {
            'avg_content_score': float,
            'subcategory_deductions': {subcategory_id: {'avg_deduction': float, 'fail_count': int, 'total_samples': int}},
            'subcategory_bonuses': {subcategory_id: {'avg_bonus': float, 'pass_count': int, 'total_samples': int}},
        }}
        """
        cn_names = self.get_cn_names()
        result_map = {}

        for model_name, results in self.model_data.items():
            if not results:
                continue

            n = len(results)
            # subcategory -> [deduction_per_sample, ...]
            subcat_deductions = defaultdict(list)  # basic+gate 失败的扣分
            subcat_bonuses = defaultdict(list)  # advanced 通过的加分
            content_scores = []

            for result in results:
                parts = self._compute_sample_score_parts(result)
                content_scores.append(parts['content_score'])
                b_per = parts['b_per_item']
                a_per = parts['a_per_item']

                # Gate 失败：每项扣 20 分
                all_gate_subcats = {"chapter_cloning", "alternating_repetition", "chapter_completion"}
                for gs in all_gate_subcats:
                    if gs in parts['gate_failed_subcats']:
                        subcat_deductions[gs].append(20.0)
                    else:
                        subcat_deductions[gs].append(0.0)

                # Basic 失败：每项扣 b_per 分
                # 需要收集所有 basic subcategory，不只是 fail 的
                check_details = result.get('check_details', {})
                basic_subcats_in_sample = set()
                basic_subcat_failed = defaultdict(int)
                for check_id, info in check_details.items():
                    if info.get('dimension_id') != 'content_quality':
                        continue
                    if info.get('check_result') == 'skip':
                        continue
                    subcat = info.get('subcategory_id', '')
                    tier = info.get('quality_tier', '')
                    if tier == 'basic' and subcat not in self.GATE_SUBCATEGORIES:
                        basic_subcats_in_sample.add(subcat)
                        if info.get('check_result') == 'fail':
                            basic_subcat_failed[subcat] += 1

                for bs in basic_subcats_in_sample:
                    fail_n = basic_subcat_failed.get(bs, 0)
                    subcat_deductions[bs].append(fail_n * b_per)

                # Advanced 通过/失败
                adv_subcats_in_sample = set()
                adv_subcat_passed = defaultdict(int)
                for check_id, info in check_details.items():
                    if info.get('dimension_id') != 'content_quality':
                        continue
                    if info.get('check_result') == 'skip':
                        continue
                    if info.get('quality_tier') == 'advanced':
                        subcat = info.get('subcategory_id', '')
                        adv_subcats_in_sample.add(subcat)
                        if info.get('check_result') == 'pass':
                            adv_subcat_passed[subcat] += 1

                for a_s in adv_subcats_in_sample:
                    pass_n = adv_subcat_passed.get(a_s, 0)
                    subcat_bonuses[a_s].append(pass_n * a_per)

            # 聚合
            subcat_ded_summary = {}
            for subcat, deductions in subcat_deductions.items():
                avg_ded = sum(deductions) / n
                fail_count = sum(1 for d in deductions if d > 0)
                if avg_ded > 0.01:  # 只保留有实际扣分的
                    subcat_ded_summary[subcat] = {
                        'avg_deduction': avg_ded,
                        'fail_count': fail_count,
                        'total_samples': n,
                    }

            subcat_bon_summary = {}
            for subcat, bonuses in subcat_bonuses.items():
                avg_bon = sum(bonuses) / n
                pass_count = sum(1 for b in bonuses if b > 0)
                subcat_bon_summary[subcat] = {
                    'avg_bonus': avg_bon,
                    'pass_count': pass_count,
                    'total_samples': n,
                }

            result_map[model_name] = {
                'avg_content_score': sum(content_scores) / n,
                'subcategory_deductions': subcat_ded_summary,
                'subcategory_bonuses': subcat_bon_summary,
            }

        return result_map

    def compute_cascade_analysis(self) -> Dict[str, Any]:
        """
        连锁失败分析：区分 Gate 触发样本中的连锁 fail 和独立 fail。
        
        逻辑：如果一个样本的 Gate 层有 fail（如章节克隆/未完成），
        那么该样本的 basic/advanced 层 fail 中，有多少是因为 Gate 问题导致的连锁后果。
        
        判定规则：Gate fail 样本中以下 subcategory 的 fail 视为连锁后果：
        - chapter_cloning/alternating_repetition → paragraph_repetition, semantic_redundancy, 
          chapter_length_stability 都是连锁后果
        - chapter_completion → outline_execution_fidelity, theme_consistency, 
          character_trait_consistency 是连锁后果
        
        返回: {model_name: {
            'gate_triggered_samples': int,
            'total_samples': int,
            'cascade_fails': int,      # Gate 样本中属于连锁的 fail 数
            'independent_fails': int,  # Gate 样本中独立的 fail 数
            'non_gate_fails': int,     # 非 Gate 样本的 fail 总数
            'per_sample': [{sample_id, gate_fails, cascade_subcats, independent_subcats}, ...]
        }}
        """
        # 连锁依赖关系定义
        CASCADE_MAP = {
            "chapter_cloning": {
                "paragraph_repetition", "semantic_redundancy", "chapter_length_stability",
                "character_trait_consistency", "theme_consistency", "main_character_consistency",
                "plot_progression", "full_narrative_content",
            },
            "alternating_repetition": {
                "paragraph_repetition", "semantic_redundancy", "chapter_length_stability",
                "character_trait_consistency", "plot_progression",
            },
            "chapter_completion": {
                "outline_execution_fidelity", "theme_consistency", "character_trait_consistency",
                "main_character_consistency", "plot_progression", "repeated_endings",
                "late_stage_digression", "chapter_length_stability",
            },
        }

        analysis = {}

        for model_name, results in self.model_data.items():
            if not results:
                continue

            gate_triggered_samples = 0
            cascade_fails_total = 0
            independent_fails_total = 0
            non_gate_fails_total = 0
            per_sample = []

            for result in results:
                sample_id = result.get('sample_id', 'unknown')
                parts = self._compute_sample_score_parts(result)
                gate_fails = parts['gate_failed_subcats']

                if not gate_fails:
                    # 非 Gate 样本，所有 fail 都是独立的
                    all_basic_fails = parts['basic_failed_subcats']
                    all_adv_fails = parts['advanced_failed_subcats']
                    non_gate_fails_total += len(all_basic_fails) + len(all_adv_fails)
                    continue

                gate_triggered_samples += 1

                # 确定连锁集合（所有被 gate fail 项覆盖的 subcategory）
                cascade_set = set()
                for gf in gate_fails:
                    cascade_set |= CASCADE_MAP.get(gf, set())

                # 分类 basic 层 fail
                cascade_subcats = []
                independent_subcats = []
                for bf in parts['basic_failed_subcats']:
                    if bf in cascade_set:
                        cascade_subcats.append(bf)
                    else:
                        independent_subcats.append(bf)

                # advanced 层 fail 在 gate 样本中全部视为连锁（Gate 样本质量太差，advanced 判定无意义）
                cascade_subcats.extend(parts['advanced_failed_subcats'])

                cascade_fails_total += len(cascade_subcats)
                independent_fails_total += len(independent_subcats)

                per_sample.append({
                    'sample_id': sample_id,
                    'gate_fails': gate_fails,
                    'cascade_subcats': cascade_subcats,
                    'independent_subcats': independent_subcats,
                })

            analysis[model_name] = {
                'gate_triggered_samples': gate_triggered_samples,
                'total_samples': len(results),
                'cascade_fails': cascade_fails_total,
                'independent_fails': independent_fails_total,
                'non_gate_fails': non_gate_fails_total,
                'per_sample': per_sample,
            }

        return analysis

    def compute_tier_failure_patterns(self) -> Dict[str, Any]:
        """
        篇幅失败模式分析：不同篇幅下的 fail subcategory 分布差异。
        
        返回: {model_name: {
            tier: {
                'n_samples': int,
                'avg_content_score': float,
                'gate_trigger_rate': float,
                'top_fail_subcats': [(subcategory_id, fail_rate, cn_name), ...],  # 按 fail 率降序
            }
        }}
        """
        cn_names = self.get_cn_names()
        analysis = {}

        for model_name, results in self.model_data.items():
            if not results:
                continue

            # 按篇幅分组
            tier_groups = defaultdict(list)
            for result in results:
                sample_id = result.get('sample_id', '')
                tier = self._get_length_tier(sample_id)
                tier_groups[tier].append(result)

            model_tiers = {}
            for tier, tier_results in tier_groups.items():
                n = len(tier_results)
                content_scores = []
                gate_triggers = 0
                # subcategory -> {fail: int, total: int}
                subcat_stats = defaultdict(lambda: {'fail': 0, 'total': 0})

                for result in tier_results:
                    parts = self._compute_sample_score_parts(result)
                    content_scores.append(parts['content_score'])
                    if parts['gate_triggered']:
                        gate_triggers += 1

                    # 统计 content_quality 维度每个 subcategory 的 fail/total
                    check_details = result.get('check_details', {})
                    seen_subcats = defaultdict(lambda: {'pass': 0, 'fail': 0})
                    for check_id, info in check_details.items():
                        if info.get('dimension_id') != 'content_quality':
                            continue
                        if info.get('check_result') == 'skip':
                            continue
                        subcat = info.get('subcategory_id', '')
                        if info.get('check_result') == 'fail':
                            seen_subcats[subcat]['fail'] += 1
                        else:
                            seen_subcats[subcat]['pass'] += 1

                    for subcat, counts in seen_subcats.items():
                        subcat_stats[subcat]['total'] += 1  # 每个样本算一次
                        if counts['fail'] > 0:
                            subcat_stats[subcat]['fail'] += 1

                # 计算 fail_rate 并按降序排列
                top_fails = []
                for subcat, counts in subcat_stats.items():
                    if counts['total'] > 0:
                        fail_rate = counts['fail'] / counts['total']
                        if fail_rate > 0:
                            top_fails.append((
                                subcat,
                                fail_rate,
                                cn_names.get(subcat, subcat),
                            ))
                top_fails.sort(key=lambda x: x[1], reverse=True)

                model_tiers[tier] = {
                    'n_samples': n,
                    'avg_content_score': sum(content_scores) / n if n > 0 else 0,
                    'gate_trigger_rate': gate_triggers / n if n > 0 else 0,
                    'top_fail_subcats': top_fails[:15],  # 只保留 top 15
                }

            analysis[model_name] = model_tiers

        return analysis

    def compute_model_diagnosis(self) -> Dict[str, dict]:
        """
        模型诊断画像：生成每个模型的结构化归因叙述。
        
        综合扣分归因、连锁分析、篇幅模式，生成：
        {model_name: {
            'rank': int,
            'total_score': float,
            'content_score': float,
            'process_score': float,
            'core_problems': [str, ...],       # 核心问题列表
            'strengths': [str, ...],            # 优势列表
            'gate_summary': str or None,        # Gate 问题摘要
            'tier_insight': str or None,        # 篇幅差异洞察
            'cascade_summary': str or None,     # 连锁分析摘要
        }}
        """
        cn_names = self.get_cn_names()
        deduction_data = self.compute_deduction_attribution()
        cascade_data = self.compute_cascade_analysis()
        tier_data = self.compute_tier_failure_patterns()

        # 先排名
        model_scores = []
        for model_name, results in self.model_data.items():
            if not results:
                continue
            parts_list = [self._compute_sample_score_parts(r) for r in results]
            avg_total = sum(p['total_score'] for p in parts_list) / len(parts_list)
            avg_content = sum(p['content_score'] for p in parts_list) / len(parts_list)
            avg_process = sum(p['process_score'] for p in parts_list) / len(parts_list)
            model_scores.append((model_name, avg_total, avg_content, avg_process))
        model_scores.sort(key=lambda x: x[1], reverse=True)

        diagnosis = {}
        for rank, (model_name, avg_total, avg_content, avg_process) in enumerate(model_scores, 1):
            ded = deduction_data.get(model_name, {})
            cas = cascade_data.get(model_name, {})
            tiers = tier_data.get(model_name, {})

            # === 核心问题 ===
            core_problems = []

            # 1. Gate 问题
            gate_summary = None
            if cas.get('gate_triggered_samples', 0) > 0:
                gt = cas['gate_triggered_samples']
                total = cas['total_samples']
                # 找出哪些 Gate 项 fail 了
                gate_subcats_all = defaultdict(int)
                for ps in cas.get('per_sample', []):
                    for gf in ps['gate_fails']:
                        gate_subcats_all[gf] += 1
                gate_details = ", ".join(
                    f"{cn_names.get(g, g)}({c}/{gt}样本)"
                    for g, c in sorted(gate_subcats_all.items(), key=lambda x: -x[1])
                )
                gate_summary = f"Gate触发 {gt}/{total} 样本: {gate_details}"
                core_problems.append(f"**致命缺陷(Gate)**: {gate_summary}。这些样本的后续{cas['cascade_fails']}处fail为连锁后果，独立问题仅{cas['independent_fails']}处")

            # 2. 扣分最大的 basic subcategory（排除 Gate）
            subcat_deds = ded.get('subcategory_deductions', {})
            basic_deds = [(s, d) for s, d in subcat_deds.items() if s not in self.GATE_SUBCATEGORIES]
            basic_deds.sort(key=lambda x: -x[1]['avg_deduction'])
            if basic_deds:
                top3 = basic_deds[:3]
                ded_strs = []
                for s, d in top3:
                    if d['avg_deduction'] >= 1.0:  # 至少平均扣 1 分才报告
                        ded_strs.append(
                            f"{cn_names.get(s, s)}(平均扣{d['avg_deduction']:.1f}分, fail {d['fail_count']}/{d['total_samples']}样本)"
                        )
                if ded_strs:
                    core_problems.append(f"**Basic层主要扣分项**: {'; '.join(ded_strs)}")

            # 3. Advanced 层未拿到的加分
            subcat_bons = ded.get('subcategory_bonuses', {})
            missed_adv = [(s, b) for s, b in subcat_bons.items()
                          if b['pass_count'] < b['total_samples']]
            missed_adv.sort(key=lambda x: (x[1]['total_samples'] - x[1]['pass_count']), reverse=True)
            if missed_adv:
                top3_missed = missed_adv[:3]
                miss_strs = []
                for s, b in top3_missed:
                    fail_n = b['total_samples'] - b['pass_count']
                    if fail_n >= 2:  # 至少 2 个样本 fail 才报告
                        miss_strs.append(
                            f"{cn_names.get(s, s)}(未通过{fail_n}/{b['total_samples']}样本)"
                        )
                if miss_strs:
                    core_problems.append(f"**Advanced层薄弱项**: {'; '.join(miss_strs)}")

            # === 优势 ===
            strengths = []
            # Advanced 全过的 subcategory
            full_pass_adv = [(s, b) for s, b in subcat_bons.items()
                             if b['pass_count'] == b['total_samples'] and b['total_samples'] > 0]
            if full_pass_adv:
                strs = [cn_names.get(s, s) for s, _ in full_pass_adv]
                strengths.append(f"Advanced全满分: {', '.join(strs)}")

            # 流程分高的
            if avg_process >= 90:
                strengths.append(f"流程规范分优秀({avg_process:.1f})")

            # === 篇幅差异洞察 ===
            tier_insight = None
            tier_scores = {t: d['avg_content_score'] for t, d in tiers.items() if d['n_samples'] >= 2}
            if len(tier_scores) >= 2:
                best_tier = max(tier_scores, key=lambda t: tier_scores[t])
                worst_tier = min(tier_scores, key=lambda t: tier_scores[t])
                diff = tier_scores[best_tier] - tier_scores[worst_tier]
                if diff >= 15:  # 差距超过 15 分才报告
                    # 找出 worst_tier 特有的高频 fail subcategory
                    worst_fails = tiers.get(worst_tier, {}).get('top_fail_subcats', [])
                    best_fails_set = set(f[0] for f in tiers.get(best_tier, {}).get('top_fail_subcats', [])
                                         if f[1] >= 0.5)  # best tier 中也有高频 fail 的
                    unique_worst = [f for f in worst_fails if f[0] not in best_fails_set and f[1] >= 0.5]
                    unique_strs = [f"{f[2]}({f[1]:.0%})" for f in unique_worst[:3]]
                    worst_gate = tiers.get(worst_tier, {}).get('gate_trigger_rate', 0)

                    insight_parts = [f"{worst_tier}({tier_scores[worst_tier]:.1f}分)显著弱于{best_tier}({tier_scores[best_tier]:.1f}分)"]
                    if worst_gate > 0:
                        insight_parts.append(f"Gate触发率{worst_gate:.0%}")
                    if unique_strs:
                        insight_parts.append(f"主要差异: {', '.join(unique_strs)}")
                    tier_insight = "，".join(insight_parts)

            # === 连锁分析摘要 ===
            cascade_summary = None
            if cas.get('gate_triggered_samples', 0) > 0:
                total_fails_in_gate = cas['cascade_fails'] + cas['independent_fails']
                if total_fails_in_gate > 0:
                    cascade_pct = cas['cascade_fails'] / total_fails_in_gate * 100
                    cascade_summary = (
                        f"Gate样本中 {cas['cascade_fails']}/{total_fails_in_gate} 处fail({cascade_pct:.0f}%)为连锁后果，"
                        f"实际独立问题仅 {cas['independent_fails']} 处"
                    )

            diagnosis[model_name] = {
                'rank': rank,
                'total_score': avg_total,
                'content_score': avg_content,
                'process_score': avg_process,
                'core_problems': core_problems,
                'strengths': strengths,
                'gate_summary': gate_summary,
                'tier_insight': tier_insight,
                'cascade_summary': cascade_summary,
            }

        return diagnosis

    def save_to_markdown(self, output_file: str):
        """保存所有统计结果到Markdown文件"""
        layer1_df = self.compute_layer1_statistics()
        layer2_df = self.compute_layer2_statistics()
        checklist_df = self.compute_checklist_statistics()
        summary = self.generate_summary_report()

        # 从 layer1_df 提取每个模型的 content_quality pass_rate
        content_quality_rates = {}
        if not layer1_df.empty:
            cq_row = layer1_df[layer1_df['dimension_id'] == 'content_quality']
            if not cq_row.empty:
                for model_name in summary.keys():
                    pr_col = f'{model_name}_pass_rate'
                    if pr_col in cq_row.columns:
                        content_quality_rates[model_name] = cq_row.iloc[0][pr_col]

        # 用新公式（基准60分）从 dimension_scores 反算每个模型的内容分
        # 新公式: 内容分 = clamp(0, 100, 60 - gate_failed*20 - basic_failed*(60/basic_total) + adv_passed*(40/adv_total))
        # 总分 = 内容分*0.7 + 流程规范分*0.3
        model_new_content_scores = {}
        model_new_total_scores = {}
        for model_name, results in self.model_data.items():
            if not results:
                continue
            content_scores = []
            for result in results:
                cq = result.get('dimension_scores', {}).get('content_quality', {})
                gate = cq.get('gate_layer', {})
                basic = cq.get('basic_layer', {})
                adv = cq.get('advanced_layer', {})

                g_penalty = gate.get('failed', 0) * 20.0
                b_total = basic.get('total', 0)
                b_deduction = basic.get('failed', 0) * (60.0 / b_total if b_total > 0 else 0)
                a_total = adv.get('total', 0)
                a_bonus = adv.get('passed', 0) * (40.0 / a_total if a_total > 0 else 0)
                score = max(0, min(100, 60.0 - g_penalty - b_deduction + a_bonus))
                content_scores.append(score)

            avg_cs = sum(content_scores) / len(content_scores) if content_scores else 0
            model_new_content_scores[model_name] = avg_cs
            # 流程规范分沿用 summary 中的值（未变）
            process_score = summary[model_name]['avg_process_score']
            model_new_total_scores[model_name] = avg_cs * 0.7 + process_score * 0.3

        # 创建排名表DataFrame，按avg_pass_rate降序
        ranked_rows = []
        for model_name, stats in summary.items():
            ranked_rows.append({
                'model_name': model_name,
                'samples': stats['has_check_result'],
                'avg_pass_rate': stats['avg_pass_rate'],
                'content_quality': content_quality_rates.get(model_name, 0),
                'total_score': model_new_total_scores.get(model_name, 0),
                'content_score': model_new_content_scores.get(model_name, 0),
                'process_score': stats['avg_process_score'],
            })
        # 按avg_pass_rate降序排序
        ranked_rows.sort(key=lambda x: x['avg_pass_rate'], reverse=True)

        # 添加排名并格式化
        summary_rows = []
        for rank, row in enumerate(ranked_rows, 1):
            summary_rows.append({
                '排名': rank,
                '模型': row['model_name'],
                '样本数': row['samples'],
                'avg_pass_rate': f"{row['avg_pass_rate']:.1%}",
                'content_quality': f"{row['content_quality']:.1%}",
                '总分': f"{row['total_score']:.1f}",
                '内容分': f"{row['content_score']:.1f}",
                '流程规范分': f"{row['process_score']:.1f}",
            })
        summary_df = pd.DataFrame(summary_rows)

        # 生成Markdown内容
        md_content = []
        md_content.append("# 模型评测对比统计报告\n")
        md_content.append(f"生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md_content.append(f"使用check_result文件: **{self.check_result_filename}**\n")

        # Summary - 排名表
        md_content.append("## 1. 模型整体表现排名\n")
        md_content.append("**字段说明**：\n")
        md_content.append("- `avg_pass_rate`: 所有检查项的平均通过率（排序依据），每项权重相等\n")
        md_content.append("- `content_quality`: 内容质量维度的检查项通过率\n")
        md_content.append("- `总分`: 总分 = 内容分×0.7 + 流程规范分×0.3（满分100）\n")
        md_content.append("- `内容分`: 内容质量得分（基准60分 - Gate惩罚 - Basic扣分 + Advanced加分，详见拆解表）\n")
        md_content.append("- `流程规范分`: format_compliance / business_rule_compliance / memory_management 三维度pass_rate均值×100\n\n")
        md_content.append(summary_df.to_markdown(index=False))
        md_content.append("\n")

        # 1.1 内容分拆解表
        md_content.append("### 1.1 内容分拆解\n")
        md_content.append("**公式**: 内容分 = 60（基准）- Gate惩罚 - Basic扣分 + Advanced加分，clamp到[0,100]\n")
        md_content.append("- Gate fail: 每项 -20分（3项致命检查：章节克隆/交替重复/完成度）\n")
        md_content.append("- Basic fail: 每项 -(60÷basic总数)分（约-3.3分/项）\n")
        md_content.append("- Advanced pass: 每项 +(40÷adv总数)分（约+4.4分/项）\n\n")

        # 从每个样本的 dimension_scores.content_quality 中提取 gate/basic/advanced 层数据
        # 按新公式反算分数拆解，按模型聚合取平均
        breakdown_rows = []
        for model_name in sorted(self.model_data.keys()):
            results = self.model_data[model_name]
            if not results:
                continue

            gate_penalties = []
            basic_deductions = []
            adv_bonuses = []
            content_scores = []
            gate_fail_samples = 0

            for result in results:
                cq = result.get('dimension_scores', {}).get('content_quality', {})
                gate = cq.get('gate_layer', {})
                basic = cq.get('basic_layer', {})
                adv = cq.get('advanced_layer', {})

                # 按新公式计算
                g_penalty = gate.get('failed', 0) * 20.0
                b_total = basic.get('total', 0)
                b_per_item = 60.0 / b_total if b_total > 0 else 0
                b_deduction = basic.get('failed', 0) * b_per_item
                a_total = adv.get('total', 0)
                a_per_item = 40.0 / a_total if a_total > 0 else 0
                a_bonus = adv.get('passed', 0) * a_per_item

                score = max(0, min(100, 60.0 - g_penalty - b_deduction + a_bonus))

                gate_penalties.append(g_penalty)
                basic_deductions.append(b_deduction)
                adv_bonuses.append(a_bonus)
                content_scores.append(score)
                if gate.get('failed', 0) > 0:
                    gate_fail_samples += 1

            n = len(results)
            avg_gate = sum(gate_penalties) / n
            avg_basic = sum(basic_deductions) / n
            avg_adv = sum(adv_bonuses) / n
            avg_score = sum(content_scores) / n

            breakdown_rows.append({
                '模型': model_name,
                '基准': '60',
                'Gate惩罚': f"-{avg_gate:.1f}" if avg_gate > 0 else "0",
                'Basic扣分': f"-{avg_basic:.1f}" if avg_basic > 0 else "0",
                'Adv加分': f"+{avg_adv:.1f}" if avg_adv > 0 else "0",
                '= 内容分': f"{avg_score:.1f}",
                'Gate触发': f"{gate_fail_samples}/{n}样本" if gate_fail_samples > 0 else "-",
            })

        # 按内容分降序排序
        breakdown_rows.sort(key=lambda x: float(x['= 内容分']), reverse=True)
        breakdown_df = pd.DataFrame(breakdown_rows)
        md_content.append(breakdown_df.to_markdown(index=False))
        md_content.append("\n")

        # 1.2 分篇幅得分对比
        md_content.append("### 1.2 分篇幅得分对比\n")
        md_content.append("按样本名中的篇幅标签（ULTRA_SHORT / SHORT / MEDIUM）分组统计。\n\n")

        def get_length_tier(sample_id):
            if "ULTRA_SHORT" in sample_id:
                return "ULTRA_SHORT"
            elif "MEDIUM" in sample_id:
                return "MEDIUM"
            elif "SHORT" in sample_id:
                return "SHORT"
            return "OTHER"

        # 收集: model -> tier -> [content_score, process_score, total_score]
        tier_data = defaultdict(lambda: defaultdict(lambda: {"content": [], "process": [], "total": []}))

        for model_name, results in self.model_data.items():
            for result in results:
                sample_id = result.get("sample_id", "")
                tier = get_length_tier(sample_id)

                cq = result.get("dimension_scores", {}).get("content_quality", {})
                gate = cq.get("gate_layer", {})
                basic = cq.get("basic_layer", {})
                adv = cq.get("advanced_layer", {})

                g_pen = gate.get("failed", 0) * 20.0
                b_total = basic.get("total", 0)
                b_ded = basic.get("failed", 0) * (60.0 / b_total if b_total > 0 else 0)
                a_total = adv.get("total", 0)
                a_bon = adv.get("passed", 0) * (40.0 / a_total if a_total > 0 else 0)
                cs = max(0, min(100, 60.0 - g_pen - b_ded + a_bon))

                ds = result.get("dimension_scores", {})
                proc_rates = []
                for dim in ["format_compliance", "business_rule_compliance", "memory_management"]:
                    d = ds.get(dim, {})
                    if d.get("total", 0) > 0:
                        proc_rates.append(d["passed"] / d["total"])
                ps = (sum(proc_rates) / len(proc_rates) * 100) if proc_rates else 0
                ts = cs * 0.7 + ps * 0.3

                tier_data[model_name][tier]["content"].append(cs)
                tier_data[model_name][tier]["process"].append(ps)
                tier_data[model_name][tier]["total"].append(ts)

        # 构建表格，按总分降序
        tiers = ["ULTRA_SHORT", "SHORT", "MEDIUM"]
        tier_rows = []
        for model_name in tier_data:
            row = {"模型": model_name}
            total_all = []
            for tier in tiers:
                bucket = tier_data[model_name][tier]
                n = len(bucket["total"])
                if n > 0:
                    avg_cs = sum(bucket["content"]) / n
                    avg_ps = sum(bucket["process"]) / n
                    avg_ts = sum(bucket["total"]) / n
                    row[f"{tier}_N"] = n
                    row[f"{tier}_内容"] = round(avg_cs, 1)
                    row[f"{tier}_流程"] = round(avg_ps, 1)
                    row[f"{tier}_总分"] = round(avg_ts, 1)
                    total_all.append(avg_ts)
                else:
                    row[f"{tier}_N"] = 0
                    row[f"{tier}_内容"] = "-"
                    row[f"{tier}_流程"] = "-"
                    row[f"{tier}_总分"] = "-"
            row["_sort"] = sum(total_all) / len(total_all) if total_all else 0
            tier_rows.append(row)

        tier_rows.sort(key=lambda x: x["_sort"], reverse=True)

        # 格式化为紧凑的 markdown 表格
        tier_table_rows = []
        for row in tier_rows:
            fmt_row = {"模型": row["模型"]}
            for tier in tiers:
                n = row[f"{tier}_N"]
                if n > 0:
                    fmt_row[tier] = f"{row[f'{tier}_内容']}/{row[f'{tier}_流程']}/{row[f'{tier}_总分']} (N={n})"
                else:
                    fmt_row[tier] = "-"
            tier_table_rows.append(fmt_row)

        tier_df = pd.DataFrame(tier_table_rows)
        md_content.append("格式: `内容分/流程规范分/总分 (N=样本数)`\n\n")
        md_content.append(tier_df.to_markdown(index=False))
        md_content.append("\n")

        # Layer1
        md_content.append("## 2. Layer1 维度对比 (dimension_id)\n")
        # 只显示pass_rate列（格式化为"xx.x% (passed/total)"），不显示score列
        layer1_display = pd.DataFrame()
        layer1_display['dimension_id'] = layer1_df['dimension_id']

        model_names = sorted([name for name, results in self.model_data.items() if len(results) > 0])
        for model_name in model_names:
            pass_rate_col = f'{model_name}_pass_rate'
            passed_col = f'{model_name}_passed'
            total_col = f'{model_name}_total'

            if all(col in layer1_df.columns for col in [pass_rate_col, passed_col, total_col]):
                # 只保留pass_rate列，格式化为 "xx.x% (passed/total)"
                layer1_display[pass_rate_col] = layer1_df.apply(
                    lambda row: f"{row[pass_rate_col]:.1%} ({int(row[passed_col])}/{int(row[total_col])})",
                    axis=1
                )

        md_content.append(layer1_display.to_markdown(index=False))
        md_content.append("\n")

        # Layer2
        md_content.append("## 3. Layer2 子类别对比 (subcategory_id)\n")
        # 格式化pass_rate为"xx.x% (passed/total)"，并添加中文名称和check_type
        layer2_display = pd.DataFrame()
        layer2_display['dimension_id'] = layer2_df['dimension_id']
        layer2_display['subcategory_id'] = layer2_df['subcategory_id']
        # 添加中文名称列
        layer2_display['中文名称'] = layer2_df['subcategory_id'].apply(
            lambda x: self.get_cn_names().get(x, x)
        )
        # 添加check_type列（rule/semantic）
        layer2_display['check_type'] = layer2_df['subcategory_id'].apply(
            lambda x: self.get_check_types().get(x, '-')
        )

        for model_name in sorted(self.model_data.keys()):
            pass_rate_col = f'{model_name}_pass_rate'
            passed_col = f'{model_name}_passed'
            total_col = f'{model_name}_total'

            if all(col in layer2_df.columns for col in [pass_rate_col, passed_col, total_col]):
                layer2_display[pass_rate_col] = layer2_df.apply(
                    lambda row: f"{row[pass_rate_col]:.1%} ({int(row[passed_col])}/{int(row[total_col])})",
                    axis=1
                )

        md_content.append(layer2_display.to_markdown(index=False))
        md_content.append("\n")

        # Checklist
        md_content.append("## 4. Checklist 检查项对比\n")
        # 格式化pass_rate为"xx.x% (passed/total)"
        checklist_display = pd.DataFrame()
        checklist_display['check_id'] = checklist_df['check_id']
        checklist_display['description'] = checklist_df['description']
        checklist_display['dimension_id'] = checklist_df['dimension_id']
        checklist_display['subcategory_id'] = checklist_df['subcategory_id']

        for model_name in sorted(self.model_data.keys()):
            pass_rate_col = f'{model_name}_pass_rate'
            passed_col = f'{model_name}_passed'
            total_col = f'{model_name}_total'

            if all(col in checklist_df.columns for col in [pass_rate_col, passed_col, total_col]):
                checklist_display[pass_rate_col] = checklist_df.apply(
                    lambda row: f"{row[pass_rate_col]:.1%} ({int(row[passed_col])}/{int(row[total_col])})",
                    axis=1
                )

        md_content.append(checklist_display.to_markdown(index=False))
        md_content.append("\n")

        # Section 5: 逻辑硬伤细分分析（如果有 flaws 结构化数据）
        logic_flaw_analysis = self.compute_logic_flaw_analysis()
        if logic_flaw_analysis:
            md_content.append("## 5. 逻辑硬伤细分分析 (logical_contradiction)\n")
            md_content.append("**说明**：从 check_result 的 `flaws` 结构化字段提取。需要使用新版 judge prompt + checker 的评测数据才有此数据。\n")

            # 5.1 各模型硬伤总览
            md_content.append("### 5.1 各模型逻辑硬伤总览\n")
            overview_rows = []
            for model_name in sorted(logic_flaw_analysis.keys()):
                stats_data = logic_flaw_analysis[model_name]
                overview_rows.append({
                    'model': model_name,
                    'fail_samples': stats_data['fail_count'],
                    'total_flaws': stats_data['total_flaws'],
                    'avg_flaws_per_fail': f"{stats_data['avg_flaws_per_fail']:.1f}",
                    'has_structured_data': f"{stats_data['structured_count']}/{stats_data['fail_count']}"
                })
            if overview_rows:
                overview_df = pd.DataFrame(overview_rows)
                md_content.append(overview_df.to_markdown(index=False))
                md_content.append("\n")

            # 5.2 硬伤类型分布
            md_content.append("### 5.2 硬伤类型分布\n")
            type_rows = []
            flaw_type_labels = {
                'factual_consistency': '客观事实矛盾',
                'worldbuilding_coherence': '世界观不自洽',
                'spatiotemporal_continuity': '时空转换断链'
            }
            for model_name in sorted(logic_flaw_analysis.keys()):
                stats_data = logic_flaw_analysis[model_name]
                type_dist = stats_data.get('type_distribution', {})
                total = stats_data['total_flaws']
                row = {'model': model_name}
                for ftype, label in flaw_type_labels.items():
                    count = type_dist.get(ftype, 0)
                    pct = f"{count/total:.0%}" if total > 0 else "-"
                    row[label] = f"{count} ({pct})"
                # 未识别类型
                known = sum(type_dist.get(ft, 0) for ft in flaw_type_labels)
                unknown = total - known
                if unknown > 0:
                    row['其他'] = str(unknown)
                type_rows.append(row)
            if type_rows:
                type_df = pd.DataFrame(type_rows)
                md_content.append(type_df.to_markdown(index=False))
                md_content.append("\n")

            # 5.3 严重程度分布
            md_content.append("### 5.3 严重程度分布\n")
            severity_rows = []
            severity_labels = {
                'critical': '致命(critical)',
                'major': '严重(major)',
                'minor': '轻微(minor)'
            }
            for model_name in sorted(logic_flaw_analysis.keys()):
                stats_data = logic_flaw_analysis[model_name]
                sev_dist = stats_data.get('severity_distribution', {})
                total = stats_data['total_flaws']
                row = {'model': model_name}
                for sev, label in severity_labels.items():
                    count = sev_dist.get(sev, 0)
                    pct = f"{count/total:.0%}" if total > 0 else "-"
                    row[label] = f"{count} ({pct})"
                severity_rows.append(row)
            if severity_rows:
                sev_df = pd.DataFrame(severity_rows)
                md_content.append(sev_df.to_markdown(index=False))
                md_content.append("\n")

        # ================================================================
        # 诊断报告部分（Section 6-9）
        # ================================================================
        md_content.append("\n---\n")
        md_content.append("# 诊断报告：因果归因分析\n")
        md_content.append("> 以下章节从「为什么分数是这样」的角度，拆解每个模型的扣分来源、连锁失败、篇幅差异和核心问题。\n")

        # Section 6: 模型诊断画像
        print("  生成诊断画像...")
        diagnosis = self.compute_model_diagnosis()
        cn_names = self.get_cn_names()

        md_content.append("## 6. 模型诊断画像\n")
        md_content.append("每个模型一段结构化归因：核心问题 → 证据 → 影响。按总分降序排列。\n")

        for model_name in sorted(diagnosis.keys(), key=lambda m: diagnosis[m]['rank']):
            diag = diagnosis[model_name]
            md_content.append(f"\n### #{diag['rank']} {model_name}\n")
            md_content.append(f"**总分 {diag['total_score']:.1f}** (内容 {diag['content_score']:.1f} / 流程 {diag['process_score']:.1f})\n")

            if diag['core_problems']:
                for prob in diag['core_problems']:
                    md_content.append(f"- {prob}\n")
            else:
                md_content.append("- 无显著问题\n")

            if diag['tier_insight']:
                md_content.append(f"- **篇幅差异**: {diag['tier_insight']}\n")

            if diag['strengths']:
                md_content.append(f"- **优势**: {'; '.join(diag['strengths'])}\n")

            md_content.append("")

        # Section 7: 扣分归因表
        print("  生成扣分归因表...")
        deduction_data = self.compute_deduction_attribution()

        md_content.append("## 7. 内容分扣分归因表\n")
        md_content.append("按 subcategory 拆解每个模型的平均扣分贡献。回答「17.5分扣在哪里」。\n")
        md_content.append("只展示平均扣分≥1.0的项。Gate项(每项-20分)、Basic项(每项约-3.3分)分别列出。\n\n")

        # 收集所有出现过的 subcategory（按平均扣分排序）
        all_subcats_ded = set()
        for model_name, data in deduction_data.items():
            for s in data.get('subcategory_deductions', {}):
                all_subcats_ded.add(s)

        # 构建 subcategory 列表，按最大扣分排序
        subcat_max_ded = {}
        for s in all_subcats_ded:
            max_d = 0
            for model_name, data in deduction_data.items():
                d = data.get('subcategory_deductions', {}).get(s, {}).get('avg_deduction', 0)
                max_d = max(max_d, d)
            subcat_max_ded[s] = max_d

        sorted_subcats = sorted(all_subcats_ded, key=lambda s: -subcat_max_ded.get(s, 0))
        # 过滤：只保留至少有一个模型扣分≥1.0的
        sorted_subcats = [s for s in sorted_subcats if subcat_max_ded.get(s, 0) >= 1.0]

        if sorted_subcats:
            # 按总分排序模型
            sorted_models = sorted(deduction_data.keys(),
                                   key=lambda m: deduction_data[m].get('avg_content_score', 0),
                                   reverse=True)

            ded_table_rows = []
            for s in sorted_subcats:
                is_gate = s in self.GATE_SUBCATEGORIES
                row = {
                    '检查项': cn_names.get(s, s),
                    '层级': 'Gate' if is_gate else 'Basic',
                }
                for model_name in sorted_models:
                    d = deduction_data[model_name].get('subcategory_deductions', {}).get(s, {})
                    avg_d = d.get('avg_deduction', 0)
                    fail_c = d.get('fail_count', 0)
                    total_s = d.get('total_samples', 0)
                    if avg_d >= 0.5:
                        row[model_name] = f"-{avg_d:.1f} ({fail_c}/{total_s})"
                    else:
                        row[model_name] = "-"
                ded_table_rows.append(row)

            ded_df = pd.DataFrame(ded_table_rows)
            md_content.append(ded_df.to_markdown(index=False))
            md_content.append("\n")
            md_content.append("*格式: `-平均扣分 (fail样本数/总样本数)`*\n")

            # Advanced 加分表
            md_content.append("\n### 7.1 Advanced层加分分布\n")
            md_content.append("Advanced检查项通过即加分(每项约+4.4分)，未通过=错失加分机会。\n\n")

            all_subcats_bon = set()
            for model_name, data in deduction_data.items():
                for s in data.get('subcategory_bonuses', {}):
                    all_subcats_bon.add(s)

            if all_subcats_bon:
                bon_table_rows = []
                for s in sorted(all_subcats_bon):
                    row = {'检查项': cn_names.get(s, s)}
                    for model_name in sorted_models:
                        b = deduction_data[model_name].get('subcategory_bonuses', {}).get(s, {})
                        pass_c = b.get('pass_count', 0)
                        total_s = b.get('total_samples', 0)
                        if total_s > 0:
                            rate = pass_c / total_s
                            row[model_name] = f"{rate:.0%} ({pass_c}/{total_s})"
                        else:
                            row[model_name] = "-"
                    bon_table_rows.append(row)
                bon_df = pd.DataFrame(bon_table_rows)
                md_content.append(bon_df.to_markdown(index=False))
                md_content.append("\n")
                md_content.append("*格式: `通过率 (pass样本数/总样本数)`*\n")

        # Section 8: 连锁失败分析
        print("  生成连锁失败分析...")
        cascade_data = self.compute_cascade_analysis()

        # 只有有 Gate 触发的模型才需要此 section
        has_cascade = any(v.get('gate_triggered_samples', 0) > 0 for v in cascade_data.values())
        if has_cascade:
            md_content.append("\n## 8. 连锁失败分析\n")
            md_content.append("Gate触发（章节克隆/交替重复/未完成）后，后续检查项的fail很多是连锁后果。")
            md_content.append("本节区分「连锁fail」和「独立fail」，避免重复归因。\n\n")

            cascade_overview_rows = []
            for model_name in sorted(cascade_data.keys()):
                cas = cascade_data[model_name]
                if cas['gate_triggered_samples'] == 0:
                    continue
                total_gate_fails = cas['cascade_fails'] + cas['independent_fails']
                cascade_pct = cas['cascade_fails'] / total_gate_fails * 100 if total_gate_fails > 0 else 0
                cascade_overview_rows.append({
                    '模型': model_name,
                    'Gate样本': f"{cas['gate_triggered_samples']}/{cas['total_samples']}",
                    '连锁fail': cas['cascade_fails'],
                    '独立fail': cas['independent_fails'],
                    '连锁占比': f"{cascade_pct:.0f}%",
                    '非Gate样本fail': cas['non_gate_fails'],
                })
            if cascade_overview_rows:
                cas_df = pd.DataFrame(cascade_overview_rows)
                md_content.append(cas_df.to_markdown(index=False))
                md_content.append("\n")

            # 逐样本明细（只展示 Gate 样本数 ≥ 2 的模型）
            md_content.append("### 8.1 Gate样本逐例明细\n")
            for model_name in sorted(cascade_data.keys()):
                cas = cascade_data[model_name]
                if cas['gate_triggered_samples'] < 1:
                    continue
                md_content.append(f"\n**{model_name}** ({cas['gate_triggered_samples']}个Gate样本):\n")
                for ps in cas.get('per_sample', []):
                    gate_str = ", ".join(cn_names.get(g, g) for g in ps['gate_fails'])
                    cascade_str = ", ".join(cn_names.get(c, c) for c in ps['cascade_subcats'][:5]) if ps['cascade_subcats'] else "无"
                    independent_str = ", ".join(cn_names.get(i, i) for i in ps['independent_subcats']) if ps['independent_subcats'] else "无"
                    md_content.append(f"- `{ps['sample_id']}`: Gate={gate_str} → 连锁={cascade_str} / 独立={independent_str}\n")

        # Section 9: 篇幅失败模式分析
        print("  生成篇幅失败模式分析...")
        tier_patterns = self.compute_tier_failure_patterns()

        md_content.append("\n## 9. 篇幅失败模式分析\n")
        md_content.append("不同篇幅下的失败原因差异——回答「MEDIUM比SHORT差在哪里」。\n")
        md_content.append("只展示fail率≥50%的subcategory（该篇幅下超过半数样本fail）。\n\n")

        # 按模型排名顺序展示
        for model_name in sorted(tier_patterns.keys(),
                                  key=lambda m: diagnosis.get(m, {}).get('rank', 99)):
            tiers_data = tier_patterns[model_name]
            if not tiers_data:
                continue

            md_content.append(f"### {model_name}\n")

            tier_summary_rows = []
            for tier in ["ULTRA_SHORT", "SHORT", "MEDIUM"]:
                td = tiers_data.get(tier, {})
                if td.get('n_samples', 0) == 0:
                    continue
                # 高频 fail subcats (≥50%)
                high_freq = [f for f in td.get('top_fail_subcats', []) if f[1] >= 0.5]
                fail_strs = [f"{f[2]}({f[1]:.0%})" for f in high_freq[:5]]

                tier_summary_rows.append({
                    '篇幅': tier,
                    'N': td['n_samples'],
                    '内容分': f"{td['avg_content_score']:.1f}",
                    'Gate率': f"{td['gate_trigger_rate']:.0%}" if td['gate_trigger_rate'] > 0 else "-",
                    '高频fail项(≥50%)': ", ".join(fail_strs) if fail_strs else "无",
                })

            if tier_summary_rows:
                tier_sum_df = pd.DataFrame(tier_summary_rows)
                md_content.append(tier_sum_df.to_markdown(index=False))
                md_content.append("\n")

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))

        print(f"\n✅ 统计结果已保存到: {output_file}")

        # 打印摘要
        print("\n" + "="*100)
        print("模型对比摘要")
        print("="*100)
        print(summary_df.to_string(index=False))

        print("\n" + "="*100)
        print("Layer1维度对比 (dimension_id)")
        print("="*100)
        print(layer1_display.to_string(index=False))


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='模型评测对比统计 — 读取各模型的check_result文件，生成排名表和维度对比报告',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
    # 用 rev006 的检查结果，统计 dsv1 批次（默认）的所有模型
    python evaluation_statistics.py check_result_rev006.json

    # 用 rev006 的检查结果，统计 dsv2 批次的所有模型
    python evaluation_statistics.py check_result_rev006.json --batch eval_dsv2

说明:
    脚本会扫描 evaluation_outputs/ 下所有 "eval_dsv1_*" (或指定批次) 目录，
    在每个样本的 _env/ 子目录中查找指定的 check_result 文件，汇总生成统计报告。
        '''
    )
    parser.add_argument(
        'filename',
        type=str,
        help='要统计的check_result文件名，如 check_result_rev006.json'
    )
    parser.add_argument(
        '--batch',
        type=str,
        default='eval_dsv1',
        help='筛选哪个批次的评测目录（默认 eval_dsv1）。eval_dsv1=设计v1的14样本，eval_dsv2=设计v2的样本'
    )
    args = parser.parse_args()

    # 评测结果目录
    evaluation_outputs_dir = '/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs'

    # 输出文件（区分批次）
    output_file = f'/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/analysis/model_comparison_statistics_{args.batch}.md'

    # 创建统计分析器
    stats = EvaluationStatistics(evaluation_outputs_dir, check_result_filename=args.filename,
                                 batch_prefix=args.batch)

    # 加载数据
    print("开始加载评测结果...")
    stats.load_all_results()

    # 检查是否加载到数据
    total_results = sum(len(results) for results in stats.model_data.values())
    if total_results == 0:
        print(f"\n❌ 错误：未找到任何 {args.filename} 文件！")
        print("请检查：")
        print(f"  1. 文件名是否正确：{args.filename}")
        print(f"  2. 评测目录是否存在该文件")
        sys.exit(1)

    # 生成并保存统计结果
    print("\n开始生成统计报告...")
    stats.save_to_markdown(output_file)

    print("\n✅ 统计分析完成！")


if __name__ == '__main__':
    main()
