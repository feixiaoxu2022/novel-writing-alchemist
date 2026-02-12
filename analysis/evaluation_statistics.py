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

    def __init__(self, evaluation_outputs_dir: str, check_result_filename: str = 'check_result_v4.json'):
        self.evaluation_outputs_dir = Path(evaluation_outputs_dir)
        self.check_result_filename = check_result_filename
        self.model_data = {}  # {model_name: [check_result_1, check_result_2, ...]}
        self.model_total_samples = {}  # {model_name: 总样本目录数}

    def load_all_results(self):
        """加载所有模型的评测结果"""
        # 只处理eval_v2开头的目录
        eval_dirs = [d for d in self.evaluation_outputs_dir.iterdir()
                     if d.is_dir() and d.name.startswith('eval_dsv1_')]

        print(f"使用check_result文件: {self.check_result_filename}")

        for eval_dir in eval_dirs:
            # 从目录名提取模型名称
            # eval_v2_20260205_132400_claude-opus-4-5-20251101 -> claude-opus-4-5-20251101
            model_name = '_'.join(eval_dir.name.split('_')[4:])

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
        for check_id in sorted(checklist_stats.keys(), key=lambda x: int(x.replace('检查项', ''))):
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
                'status_distribution': defaultdict(int),
                'good_or_fair_count': 0,
                'poor_count': 0
            }

            pass_rates = []

            for result in results:
                overall = result.get('overall_result', {})

                pass_rates.append(overall.get('pass_rate', 0))
                status = overall.get('status', 'Unknown')
                model_summary['status_distribution'][status] += 1

                if status in ['Good', 'Fair']:
                    model_summary['good_or_fair_count'] += 1
                elif status == 'Poor':
                    model_summary['poor_count'] += 1

            model_summary['avg_pass_rate'] = sum(pass_rates) / len(pass_rates) if pass_rates else 0

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

    def save_to_markdown(self, output_file: str):
        """保存所有统计结果到Markdown文件"""
        layer1_df = self.compute_layer1_statistics()
        layer2_df = self.compute_layer2_statistics()
        checklist_df = self.compute_checklist_statistics()
        summary = self.generate_summary_report()

        # 创建summary的DataFrame
        summary_rows = []
        for model_name, stats in summary.items():
            total = stats['total_sample_dirs']
            has_check = stats['has_check_result']
            no_check = stats['no_check_result']
            good_fair = stats['good_or_fair_count']
            poor = stats['poor_count']

            row = {
                'model_name': model_name,
                'total_sample_dirs': total,
                'has_check_result': f"{has_check} ({has_check/total:.1%}, {has_check}/{total})" if total > 0 else "0",
                'no_check_result': f"{no_check} ({no_check/total:.1%}, {no_check}/{total})" if total > 0 else "0",
                'good_or_fair': f"{good_fair} ({good_fair/has_check:.1%}, {good_fair}/{has_check})" if has_check > 0 else "0",
                'poor': f"{poor} ({poor/has_check:.1%}, {poor}/{has_check})" if has_check > 0 else "0",
                'avg_pass_rate': f"{stats['avg_pass_rate']:.2%}"
            }
            summary_rows.append(row)
        summary_df = pd.DataFrame(summary_rows)

        # 生成Markdown内容
        md_content = []
        md_content.append("# 模型评测对比统计报告\n")
        md_content.append(f"生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md_content.append(f"使用check_result文件: **{self.check_result_filename}**\n")

        # Summary
        md_content.append("## 1. 模型整体表现摘要\n")
        md_content.append("**字段说明**：\n")
        md_content.append("- `total_sample_dirs`: 总样本目录数\n")
        md_content.append("- `has_check_result`: 有check_result文件的样本数（完成评测）\n")
        md_content.append("- `no_check_result`: 完全无check_result文件的样本数（Agent崩溃/超时）\n")
        md_content.append("- `good_or_fair`: Good或Fair质量的样本数\n")
        md_content.append("- `poor`: Poor质量的样本数\n\n")
        md_content.append(summary_df.to_markdown(index=False))
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
        description='评测结果统计分析脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
    python evaluation_statistics.py check_result_rev003.json     # 使用指定文件名
    python evaluation_statistics.py check_result_v4.json         # 使用check_result_v4.json
        '''
    )
    parser.add_argument(
        'filename',
        type=str,
        help='check_result文件名（必填，如 check_result_rev003.json）'
    )
    args = parser.parse_args()

    # 评测结果目录
    evaluation_outputs_dir = '/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs'

    # 输出文件
    output_file = '/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/analysis/model_comparison_statistics.md'

    # 创建统计分析器（传入文件名）
    stats = EvaluationStatistics(evaluation_outputs_dir, check_result_filename=args.filename)

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
