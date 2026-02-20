#!/usr/bin/env python3
"""
小说创作场景样本生成器

特点：
1. 无task级别environment，所有样本共享公共技能文件
2. 从query_pools.yaml抽取queries
3. 基于unified_scenario_design.yaml的need_templates生成样本
"""

import json
import yaml
from pathlib import Path
from copy import deepcopy


class NovelSampleGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir).resolve()  # 转换为绝对路径

        # 加载配置文件
        print("Loading configuration files...")
        with open(self.base_dir / "unified_scenario_design.yaml", 'r', encoding='utf-8') as f:
            self.scenario = yaml.safe_load(f)

        with open(self.base_dir / "query_pools.yaml", 'r', encoding='utf-8') as f:
            self.query_pools = yaml.safe_load(f)['query_pools']

        with open(self.base_dir / "BusinessRules_dsv1.md", 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()

        # 加载能力体系定义
        print("Loading capability taxonomy...")
        taxonomy_path = self.base_dir.parent / "check_capability_taxonomy.yaml"
        with open(taxonomy_path, 'r', encoding='utf-8') as f:
            self.capability_taxonomy = yaml.safe_load(f)
        self._build_capability_lookup()

        # 加载样本格式规范（包含checker_params_spec）
        print("Loading sample format specification...")
        # 从 design_v1/scripts/sample_generator/main.py 向上5层到项目根目录
        # 路径: main.py → sample_generator/ → scripts/ → design_v1/ → novel_writing_alchemist/ → tmp_scenarios/ → universal_scenario_framework/
        spec_path = Path(__file__).resolve().parents[5] / ".claude/skills/sample_authoring/references/sample_format_spec.json"
        with open(spec_path, 'r', encoding='utf-8') as f:
            self.sample_format_spec = json.load(f)
        self.checker_params_spec = self.sample_format_spec.get('checker_params_spec', {})
        print(f"Loaded checker_params_spec for {len(self.checker_params_spec)} check types")

        # 加载通用检查项（优先从独立的check_definitions目录读取）
        check_def_dir = self.base_dir.parent / "check_definitions"
        if (check_def_dir / "common_check_list.yaml").exists():
            with open(check_def_dir / "common_check_list.yaml", 'r', encoding='utf-8') as f:
                common_check_data = yaml.safe_load(f)
            self.common_checks = common_check_data.get('checks', [])
            self.check_definitions_dir = check_def_dir
            print(f"Loaded {len(self.common_checks)} common check items from check_definitions/")
        else:
            # 回退：从unified_scenario_design.yaml读取（兼容旧结构）
            self.common_checks = self.scenario.get('common_check_list', {}).get('checks', [])
            self.check_definitions_dir = None
            print(f"Loaded {len(self.common_checks)} common check items from unified_scenario_design.yaml")
        
        # 加载模板特有检查项（如果使用check_definitions目录）
        self.template_checks = {}
        if self.check_definitions_dir:
            template_checks_dir = self.check_definitions_dir / "template_checks"
            if template_checks_dir.exists():
                for yaml_file in template_checks_dir.glob("*.yaml"):
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        template_data = yaml.safe_load(f)
                    template_id = template_data.get('template_id', yaml_file.stem)
                    self.template_checks[template_id] = template_data.get('checks', [])
                print(f"Loaded template checks for {len(self.template_checks)} templates from check_definitions/")

        # 构建公共environment
        print("Building common environment...")
        self.environment = self._build_common_environment()

        # 校验checklist schema
        print("Validating checklist schemas...")
        self.validate_checklist_schemas()

    def _build_capability_lookup(self):
        """从能力体系YAML构建查找结构"""
        self.valid_dimensions = set()
        self.dimension_to_subcategories = {}
        self.subcategory_to_check_types = {}
        self.subcategory_to_dimension = {}

        # 遍历所有能力维度
        for dimension in self.capability_taxonomy.get('capability_dimensions', []):
            dimension_id = dimension['dimension_id']
            self.valid_dimensions.add(dimension_id)
            self.dimension_to_subcategories[dimension_id] = []

            # 遍历该维度下的所有子类别
            for subcategory in dimension.get('subcategories', []):
                subcategory_id = subcategory['subcategory_id']
                self.dimension_to_subcategories[dimension_id].append(subcategory_id)
                self.subcategory_to_dimension[subcategory_id] = dimension_id

                # 记录该子类别支持的check_types
                check_types = subcategory.get('check_types', [])
                self.subcategory_to_check_types[subcategory_id] = check_types

        print(f"Loaded {len(self.valid_dimensions)} capability dimensions")
        print(f"Loaded {len(self.subcategory_to_dimension)} subcategories")

    # 文本文件后缀（作为text类型加入environment）
    TEXT_EXTENSIONS = {'.md', '.json', '.yaml', '.yml', '.txt', '.csv'}
    # 二进制文件后缀（base64编码后加入environment）
    BINARY_EXTENSIONS = {'.xlsx', '.xls', '.png', '.jpg', '.jpeg', '.gif', '.pdf'}

    def _build_common_environment(self):
        """构建公共环境（所有样本共享的技能文件和checker criteria文件）

        自动扫描以下目录，按文件后缀自动分类为text或binary类型：
        - data_pools/: 技能文件、schema、素材（Agent运行时使用）
        - judge_criteria/: LLM judge评估标准文件（Checker运行时使用）
        新增文件时无需修改代码。
        """
        import base64
        env = []

        # 需要扫描的目录列表
        scan_dirs = ["data_pools", "judge_criteria"]

        for dir_name in scan_dirs:
            scan_dir = self.base_dir / dir_name
            if not scan_dir.exists():
                print(f"  Warning: {dir_name}/ directory not found")
                continue

            # 递归扫描目录下所有文件
            for filepath in sorted(scan_dir.rglob("*")):
                if not filepath.is_file():
                    continue

                # 跳过隐藏文件和临时文件
                if filepath.name.startswith('.') or filepath.name.startswith('~$'):
                    continue

                relative_path = filepath.relative_to(self.base_dir)
                suffix = filepath.suffix.lower()

                if suffix in self.TEXT_EXTENSIONS:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        env.append({
                            "path": str(relative_path),
                            "type": "file",
                            "content": f.read()
                        })
                elif suffix in self.BINARY_EXTENSIONS:
                    with open(filepath, 'rb') as f:
                        env.append({
                            "path": str(relative_path),
                            "type": "binary",
                            "content": base64.b64encode(f.read()).decode('ascii')
                        })
                else:
                    print(f"  Warning: skipping unknown file type: {relative_path}")

        return env

    def _validate_params_format(self, context, check_id, check_type, params, errors):
        """严格校验params格式是否符合sample_format_spec.json规范

        Args:
            context: 上下文标识
            check_id: 检查项ID
            check_type: 检查类型
            params: 参数字典
            errors: 错误列表
        """
        if check_type not in self.checker_params_spec:
            # 未知的check_type，跳过params校验（由check_type枚举校验捕获）
            return

        spec = self.checker_params_spec[check_type]
        params_spec = spec.get('params', {})

        # 校验必需参数
        for param_name, param_spec in params_spec.items():
            is_required = param_spec.get('required', False)

            if is_required and param_name not in params:
                errors.append(
                    f"[{context}] {check_id}: Missing required param '{param_name}' "
                    f"for check_type '{check_type}'"
                )

        # 校验参数值格式
        for param_name, param_value in params.items():
            if param_name not in params_spec:
                # 允许额外的参数（可能是扩展字段）
                continue

            param_spec = params_spec[param_name]
            expected_type = param_spec.get('type')

            # 类型校验
            if expected_type == 'string' and not isinstance(param_value, str):
                errors.append(
                    f"[{context}] {check_id}: param '{param_name}' must be string, "
                    f"got {type(param_value).__name__}"
                )
            elif expected_type == 'array' and not isinstance(param_value, list):
                errors.append(
                    f"[{context}] {check_id}: param '{param_name}' must be array, "
                    f"got {type(param_value).__name__}"
                )
            elif expected_type == 'object' and not isinstance(param_value, dict):
                errors.append(
                    f"[{context}] {check_id}: param '{param_name}' must be object, "
                    f"got {type(param_value).__name__}"
                )

            # 特殊校验：entity_attribute_equals
            if check_type == 'entity_attribute_equals':
                if param_name == 'entity_type' and param_value != 'file':
                    errors.append(
                        f"[{context}] {check_id}: entity_type must be 'file', "
                        f"got '{param_value}'"
                    )
                if param_name == 'target_id' and isinstance(param_value, str):
                    if not param_value.startswith('workspace/'):
                        errors.append(
                            f"[{context}] {check_id}: target_id must start with 'workspace/', "
                            f"got '{param_value}'"
                        )
                if param_name == 'expected_value':
                    # expected_value可以是简单值或约束对象
                    if isinstance(param_value, dict):
                        # 如果是约束对象，检查是否有有效的约束类型
                        valid_constraints = ['regex', 'array_min_length', 'array_max_length',
                                           'array_item_type', 'min', 'max', 'enum', 'contains_value']
                        has_valid = any(k in param_value for k in valid_constraints)
                        if not has_valid:
                            errors.append(
                                f"[{context}] {check_id}: expected_value constraint object must "
                                f"contain at least one of {valid_constraints}, got keys: {list(param_value.keys())}"
                            )

            # 特殊校验：json_schema
            if check_type == 'json_schema':
                if param_name == 'file_pattern' and isinstance(param_value, str):
                    if not param_value.startswith('workspace/'):
                        errors.append(
                            f"[{context}] {check_id}: file_pattern must start with 'workspace/', "
                            f"got '{param_value}'"
                        )

            # 特殊校验：semantic_check
            if check_type == 'semantic_check':
                if param_name == 'validation_rules' and isinstance(param_value, list):
                    for idx, rule in enumerate(param_value):
                        if not isinstance(rule, dict):
                            errors.append(
                                f"[{context}] {check_id}: validation_rules[{idx}] must be object"
                            )
                            continue

                        # 检查必需字段
                        if 'rule_id' not in rule:
                            errors.append(
                                f"[{context}] {check_id}: validation_rules[{idx}] missing 'rule_id'"
                            )
                        if 'validation_method' not in rule:
                            errors.append(
                                f"[{context}] {check_id}: validation_rules[{idx}] missing 'validation_method'"
                            )
                        else:
                            method = rule['validation_method']
                            # P1-P5 程序化检查方法（在checker_execute.py中实现，零LLM成本）
                            PROGRAMMATIC_METHODS = {
                                'chapter_cloning_detection',
                                'alternating_repetition_detection',
                                'chapter_completion_ratio',
                                'chapter_length_stability',
                                'paragraph_repetition_detection',
                            }
                            VALID_METHODS = {'llm_semantic_analysis', 'word_count_range'} | PROGRAMMATIC_METHODS
                            if method not in VALID_METHODS:
                                errors.append(
                                    f"[{context}] {check_id}: validation_rules[{idx}] invalid "
                                    f"validation_method '{method}', must be one of {sorted(VALID_METHODS)}"
                                )

                            # 根据方法检查对应参数
                            if method == 'word_count_range' and 'expected_range' not in rule:
                                errors.append(
                                    f"[{context}] {check_id}: validation_rules[{idx}] with "
                                    f"validation_method='word_count_range' requires 'expected_range'"
                                )
                            if method == 'llm_semantic_analysis' and 'evaluation_criteria' not in rule:
                                # 允许使用外部criteria文件（llm_judge_criteria_file在params层级）替代inline evaluation_criteria
                                if 'llm_judge_criteria_file' not in params:
                                    errors.append(
                                        f"[{context}] {check_id}: validation_rules[{idx}] with "
                                        f"validation_method='llm_semantic_analysis' requires 'evaluation_criteria' "
                                        f"in rule or 'llm_judge_criteria_file' in params"
                                    )

    def _validate_single_check(self, context, check_id, check_item, valid_quality_tiers, errors, warnings):
        """校验单个check项的合法性

        Args:
            context: 上下文标识（如template_id或'[common_check_list]'）
            check_id: 检查项ID
            check_item: 检查项配置
            valid_quality_tiers: 有效的质量层级
            errors: 错误列表
            warnings: 警告列表
        """
        # 1. 必需字段检查
        if 'check_type' not in check_item:
            errors.append(f"[{context}] {check_id}: Missing required field 'check_type'")

        if 'params' not in check_item:
            errors.append(f"[{context}] {check_id}: Missing required field 'params'")
        elif not isinstance(check_item['params'], dict):
            errors.append(f"[{context}] {check_id}: 'params' must be a dict, got {type(check_item['params']).__name__}")

        if 'check_name' not in check_item and 'description' not in check_item:
            errors.append(f"[{context}] {check_id}: Missing 'check_name' or 'description'")

        # 2. dimension_id合法性(基于能力体系)
        dimension_id = check_item.get('dimension_id')
        if dimension_id and dimension_id not in self.valid_dimensions:
            errors.append(f"[{context}] {check_id}: Invalid dimension_id '{dimension_id}', must be one of {sorted(self.valid_dimensions)}")

        # 3. subcategory_id合法性(基于能力体系)
        subcategory_id = check_item.get('subcategory_id')
        if subcategory_id:
            # 检查subcategory_id是否存在
            if subcategory_id not in self.subcategory_to_dimension:
                errors.append(f"[{context}] {check_id}: Invalid subcategory_id '{subcategory_id}', not found in capability taxonomy")
            # 检查subcategory_id是否属于指定的dimension_id
            elif dimension_id and self.subcategory_to_dimension.get(subcategory_id) != dimension_id:
                expected_dim = self.subcategory_to_dimension[subcategory_id]
                errors.append(f"[{context}] {check_id}: subcategory_id '{subcategory_id}' belongs to dimension '{expected_dim}', not '{dimension_id}'")

        # 4. check_type与subcategory的匹配性(基于能力体系)
        check_type = check_item.get('check_type')
        if check_type and subcategory_id:
            valid_types = self.subcategory_to_check_types.get(subcategory_id, [])
            if valid_types and check_type not in valid_types:
                errors.append(f"[{context}] {check_id}: check_type '{check_type}' not valid for subcategory '{subcategory_id}', must be one of {valid_types}")

        # 5. quality_tier合法性
        quality_tier = check_item.get('quality_tier')
        if quality_tier is not None and quality_tier not in valid_quality_tiers:
            errors.append(f"[{context}] {check_id}: Invalid quality_tier '{quality_tier}', must be 'basic', 'advanced', or null")

        # 6. content_quality维度必须有quality_tier
        if dimension_id == 'content_quality' and quality_tier is None:
            errors.append(f"[{context}] {check_id}: content_quality dimension must have quality_tier (basic or advanced)")

        # 7. is_critical类型检查
        is_critical = check_item.get('is_critical')
        if is_critical is not None and not isinstance(is_critical, bool):
            errors.append(f"[{context}] {check_id}: 'is_critical' must be boolean, got {type(is_critical).__name__}")

        # 8. weight类型检查
        weight = check_item.get('weight')
        if weight is not None and not isinstance(weight, (int, float)):
            errors.append(f"[{context}] {check_id}: 'weight' must be number, got {type(weight).__name__}")

        # 9. tool_called_with_params特定校验
        if check_type == 'tool_called_with_params':
            params = check_item.get('params', {})
            if 'tool_name' not in params:
                errors.append(f"[{context}] {check_id}: tool_called_with_params requires 'tool_name' in params")
            if 'required_params' not in params:
                warnings.append(f"[{context}] {check_id}: tool_called_with_params usually needs 'required_params' in params")

        # 10. 严格校验params格式（基于sample_format_spec.json）
        if check_type and 'params' in check_item and isinstance(check_item['params'], dict):
            self._validate_params_format(context, check_id, check_type, check_item['params'], errors)

    def validate_checklist_schemas(self):
        """校验check_list的schema合法性（支持check_definitions目录和内嵌两种模式）"""

        # quality_tier是固定的枚举值(不在能力体系中定义)
        VALID_QUALITY_TIERS = ['basic', 'advanced', None]

        errors = []
        warnings = []

        # 首先校验common_check_list（已经在__init__中加载到self.common_checks）
        if self.common_checks:
            for idx, check_item in enumerate(self.common_checks, 1):
                check_id = check_item.get('check_id', f'common_check_{idx}')
                self._validate_single_check('[common_check_list]', check_id, check_item,
                                           VALID_QUALITY_TIERS, errors, warnings)

        # 然后校验每个模板的check_list
        for template in self.scenario['user_need_templates']:
            template_id = template['need_template_id']
            
            # 获取模板检查项（优先从check_definitions，回退到template内嵌）
            if self.check_definitions_dir and template_id in self.template_checks:
                check_list = self.template_checks[template_id]
            else:
                check_list = template.get('check_list', [])

            if not check_list:
                errors.append(f"[{template_id}] check_list is empty or missing")
                continue

            for idx, check_item in enumerate(check_list, 1):
                check_id = check_item.get('check_id', f'check_{idx}')
                self._validate_single_check(template_id, check_id, check_item,
                                           VALID_QUALITY_TIERS, errors, warnings)

        # 输出校验结果
        if errors:
            print(f"\n❌ Found {len(errors)} schema errors:")
            for error in errors:
                print(f"  - {error}")
            raise ValueError(f"Checklist schema validation failed with {len(errors)} errors")

        if warnings:
            print(f"\n⚠️  Found {len(warnings)} warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        print(f"✓ All checklist schemas validated successfully ({len(self.scenario['user_need_templates'])} templates)")


    def generate_samples(self):
        """生成所有样本"""
        samples = []

        for template in self.scenario['user_need_templates']:
            template_id = template['need_template_id']
            query_pool_id = template['query_pool_id']
            word_count = template.get('word_count', '')

            print(f"\nProcessing template: {template_id}")

            # 从query池获取queries
            if query_pool_id not in self.query_pools:
                print(f"  Warning: Query pool {query_pool_id} not found, skipping")
                continue

            queries = self.query_pools[query_pool_id]

            # 成本和时间控制：限制各类型样本数量
            sample_limits = {
                'ultra_short': 5,
                'short': 3,         # 减少到3，预计生成5个
                'medium': 1,        # 减少到1，预计生成4个
                'long': 0,
                'ultra_long': 0
            }

            if word_count in sample_limits:
                limit = sample_limits[word_count]
                original_count = len(queries)
                queries = queries[:limit]
                if original_count > limit:
                    print(f"  Found {original_count} queries, limited to {limit} for cost/time control ({word_count})")
                else:
                    print(f"  Found {len(queries)} queries in pool {query_pool_id}")
            else:
                print(f"  Found {len(queries)} queries in pool {query_pool_id}")

            # 为每个query生成样本
            for idx, query_item in enumerate(queries, 1):
                sample = self._build_sample(template, query_item, idx)
                samples.append(sample)

        return samples

    def _build_sample(self, template, query_item, idx):
        """构建单个样本"""
        template_id = template['need_template_id']
        data_id = f"{template_id}_{idx:03d}"

        # 获取模板特有检查项（优先从check_definitions，回退到template内嵌）
        if self.check_definitions_dir and template_id in self.template_checks:
            template_check_list = self.template_checks[template_id]
        else:
            template_check_list = template.get('check_list', [])

        # 构建样本
        sample = {
            "data_id": data_id,
            "query": query_item['query_text'].strip(),
            "system": self.system_prompt,
            "servers": ["novel_writing_service"],
            "environment": self.environment,
            "check_list": self._convert_checklist(template_check_list, query_item),
            "user_simulator_prompt": template.get('user_simulator_prompt', '').strip()
        }

        # 添加扩展字段（元数据）
        sample["extension"] = {
            "source": query_item.get('source', ''),
            "query_id": query_item.get('query_id', ''),
            "clarity": template['clarity'],
            "word_count": template['word_count'],
            "query_word_count": query_item.get('word_count', ''),  # 新增：query实际字数要求
            "tone": template['tone'],
            "template_name": template.get('template_name', '')
        }

        return sample

    def _parse_word_count_range(self, word_count_str, tolerance=0.1):
        """解析word_count字符串，返回带容差的范围

        Args:
            word_count_str: 字数要求字符串，格式：
                - 范围: "6500-10000"
                - 精确值: "30000"
                - 开区间: "2000000+"
            tolerance: 浮动容差比例，默认10%

        Returns:
            tuple: (min_count, max_count) 或 (min_count, None)
        """
        word_count_str = str(word_count_str).strip()

        # 开区间格式: "2000000+"
        if word_count_str.endswith('+'):
            base = int(word_count_str[:-1])
            # 下限允许-10%浮动
            return (int(base * (1 - tolerance)), None)

        # 范围格式: "6500-10000"
        if '-' in word_count_str:
            parts = word_count_str.split('-')
            min_val = int(parts[0])
            max_val = int(parts[1])
            # 范围两端各允许10%浮动
            return (int(min_val * (1 - tolerance)), int(max_val * (1 + tolerance)))

        # 精确值格式: "30000"
        try:
            target = int(word_count_str)
            # ±10%浮动
            return (int(target * (1 - tolerance)), int(target * (1 + tolerance)))
        except ValueError:
            # 无法解析，返回None
            return (None, None)

    def _convert_checklist(self, template_check_list, query_item):
        """转换check_list格式为标准格式，保留所有字段，并合并通用检查项"""
        converted = []

        # 获取MCP server名称（用于给tool_name加前缀）
        server_name = self.scenario.get('mcp_service_config', {}).get('service_name', '')

        # 先添加通用检查项
        for item in self.common_checks:
            check_item = {
                "check_type": item['check_type'],
                "params": deepcopy(item['params'])  # 深拷贝params
            }

            # 如果是tool_called_with_params类型，给tool_name加上server前缀
            if item['check_type'] == 'tool_called_with_params' and server_name:
                if 'tool_name' in check_item['params']:
                    tool_name = check_item['params']['tool_name']
                    # 只有当tool_name不包含__时才加前缀（避免重复加）
                    if '__' not in tool_name:
                        check_item['params']['tool_name'] = f"{server_name}__{tool_name}"

            # 添加description（优先使用check_name）
            if 'check_name' in item:
                check_item['description'] = item['check_name']
            elif 'description' in item:
                check_item['description'] = item['description']

            # 保留所有其他字段（用于checker scoring），但跳过check_id（稍后统一编号）
            optional_fields = [
                'dimension_id', 'subcategory_id', 'quality_tier',
                'weight', 'is_critical'
            ]
            for field in optional_fields:
                if field in item:
                    check_item[field] = item[field]

            # 保留源 YAML 中的语义化 check_id（如果有）
            if 'check_id' in item:
                check_item['check_id'] = item['check_id']

            converted.append(check_item)

        # 再添加模板特定检查项
        query_word_count = query_item.get('word_count', '')

        for item in template_check_list:
            # 必需字段
            check_item = {
                "check_type": item['check_type'],
                "params": deepcopy(item['params'])  # 深拷贝params，避免修改原数据
            }

            # 如果是tool_called_with_params类型，给tool_name加上server前缀
            if item['check_type'] == 'tool_called_with_params' and server_name:
                if 'tool_name' in check_item['params']:
                    tool_name = check_item['params']['tool_name']
                    # 只有当tool_name不包含__时才加前缀（避免重复加）
                    if '__' not in tool_name:
                        check_item['params']['tool_name'] = f"{server_name}__{tool_name}"

            # 识别字数检查项并注入动态范围
            is_word_count_check = False
            check_name = item.get('check_name', '')

            # 判断是否是字数检查项（通过check_name或params）
            if '总字数' in check_name or '字数' in check_name:
                is_word_count_check = True
            elif 'validation_rules' in check_item['params']:
                for rule in check_item['params']['validation_rules']:
                    if 'word_count' in rule.get('rule_id', ''):
                        is_word_count_check = True
                        break

            # 如果是字数检查项，且query有word_count，则动态替换范围
            if is_word_count_check and query_word_count:
                min_count, max_count = self._parse_word_count_range(query_word_count)

                if min_count is not None:
                    # 更新check_name显示实际范围
                    if max_count:
                        check_item['description'] = f"总字数应在{min_count}-{max_count}之间（基于query要求{query_word_count}，±10%浮动）"
                    else:
                        check_item['description'] = f"总字数应≥{min_count}（基于query要求{query_word_count}，-10%浮动）"

                    # 更新params中的expected_range
                    if 'validation_rules' in check_item['params']:
                        for rule in check_item['params']['validation_rules']:
                            if 'word_count' in rule.get('rule_id', ''):
                                if max_count:
                                    rule['expected_range'] = [min_count, max_count]
                                else:
                                    rule['expected_range'] = [min_count, float('inf')]
                                break
            else:
                # 添加description（优先使用check_name）
                if 'check_name' in item:
                    check_item['description'] = item['check_name']
                elif 'description' in item:
                    check_item['description'] = item['description']

            # 保留所有其他字段（用于checker scoring），但跳过check_id（稍后统一编号）
            optional_fields = [
                'dimension_id', 'subcategory_id', 'quality_tier',
                'weight', 'is_critical'
            ]
            for field in optional_fields:
                if field in item:
                    check_item[field] = item[field]

            # 保留源 YAML 中的语义化 check_id（如果有）
            if 'check_id' in item:
                check_item['check_id'] = item['check_id']

            converted.append(check_item)

        # 统一处理 check_id：保留已有的语义化 ID，为没有 ID 的项生成兜底编号
        for idx, check_item in enumerate(converted, 1):
            if 'check_id' not in check_item:
                check_item['check_id'] = f"check_{idx:02d}"

        return converted

    def save_samples(self, samples, output_path):
        """保存样本为JSONL格式，同时生成可读版本和HTML查看器"""
        import base64

        output_file = self.base_dir / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 保存JSONL格式（用于评测）
        with open(output_file, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        print(f"\n✓ Generated {len(samples)} samples → {output_file}")

        # 自动生成格式化版本（用于VSCode查看）
        readable_file = output_file.parent / (output_file.stem + '_readable.json')
        with open(readable_file, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        print(f"✓ Generated readable version → {readable_file}")

        # 生成HTML查看器
        self._generate_html_viewer(samples, output_file.parent / 'viewer.html')

        # 统计信息
        template_counts = {}
        for sample in samples:
            template = sample['data_id'].rsplit('_', 1)[0]
            template_counts[template] = template_counts.get(template, 0) + 1

        print("\nSamples by template:")
        for template, count in sorted(template_counts.items()):
            print(f"  {template}: {count} samples")

    def _generate_html_viewer(self, samples, output_path):
        """生成HTML查看器"""
        import base64

        # 将数据转为JSON并base64编码
        json_str = json.dumps(samples, ensure_ascii=False)
        encoded = base64.b64encode(json_str.encode('utf-8')).decode('ascii')

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小说创作场景评测样本查看器</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            border-radius: 20px 20px 0 0;
        }}
        h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .stat {{ display: inline-block; margin-right: 30px; background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 10px; }}
        .stat-value {{ font-size: 24px; font-weight: 700; }}
        .controls {{ padding: 20px 40px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
        .search-box input {{
            width: 100%;
            max-width: 500px;
            padding: 12px 20px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 15px;
        }}
        .samples-grid {{
            padding: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 25px;
        }}
        .sample-card {{
            border: 2px solid #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .sample-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-color: #667eea;
        }}
        .sample-header {{
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }}
        .sample-id {{ font-size: 16px; font-weight: 700; color: #667eea; margin-bottom: 10px; }}
        .tag {{
            display: inline-block;
            padding: 4px 10px;
            margin: 2px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}
        .tag.word {{ background: #e3f2fd; color: #1976d2; }}
        .tag.tone {{ background: #f3e5f5; color: #7b1fa2; }}
        .tag.checks {{ background: #e8eaf6; color: #3f51b5; }}
        .sample-body {{ padding: 20px; color: #495057; line-height: 1.6; }}
        .query {{
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            padding: 20px;
            overflow-y: auto;
        }}
        .modal.active {{ display: flex; justify-content: center; align-items: start; }}
        .modal-content {{
            background: white;
            border-radius: 20px;
            max-width: 900px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            margin-top: 40px;
        }}
        .modal-header {{
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px 20px 0 0;
            position: sticky;
            top: 0;
        }}
        .close-btn {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 36px;
            height: 36px;
            border: none;
            background: rgba(255,255,255,0.2);
            color: white;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
        }}
        .modal-body {{ padding: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h3 {{
            font-size: 18px;
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }}
        .section-content {{
            color: #495057;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        .code-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 13px;
            max-height: 300px;
            overflow-y: auto;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>小说创作场景 - 评测样本查看器</h1>
            <div class="stat">总样本数: <span class="stat-value" id="total">0</span></div>
        </header>
        <div class="controls">
            <div class="search-box">
                <input type="text" id="search" placeholder="搜索样本ID或内容...">
            </div>
        </div>
        <div class="samples-grid" id="grid"></div>
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="close-btn" onclick="closeModal()">&times;</button>
                <h2 id="mtitle"></h2>
            </div>
            <div class="modal-body" id="mbody"></div>
        </div>
    </div>

    <script>
        const ENCODED_DATA = '{encoded}';

        // 正确解码UTF-8的base64
        function base64DecodeUnicode(str) {{
            const binary = atob(str);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {{
                bytes[i] = binary.charCodeAt(i);
            }}
            return new TextDecoder('utf-8').decode(bytes);
        }}

        const jsonStr = base64DecodeUnicode(ENCODED_DATA);
        const allSamples = JSON.parse(jsonStr);
        let filtered = allSamples;

        function render() {{
            document.getElementById('total').textContent = filtered.length;
            const grid = document.getElementById('grid');
            grid.innerHTML = filtered.map(s => `
                <div class="sample-card" onclick="show('${{s.data_id}}')">
                    <div class="sample-header">
                        <div class="sample-id">${{s.data_id}}</div>
                        <span class="tag word">${{s.extension.word_count}}</span>
                        <span class="tag tone">${{s.extension.tone}}</span>
                        <span class="tag checks">${{s.check_list.length}}项</span>
                    </div>
                    <div class="sample-body">
                        <div class="query">${{s.query.substring(0,200)}}...</div>
                    </div>
                </div>
            `).join('');
        }}

        function show(id) {{
            const s = allSamples.find(x => x.data_id === id);
            document.getElementById('mtitle').textContent = s.data_id;
            document.getElementById('mbody').innerHTML = `
                <div class="section">
                    <h3>System Prompt</h3>
                    <div class="code-box">${{renderMarkdown(s.system)}}</div>
                </div>
                <div class="section">
                    <h3>用户Query</h3>
                    <div class="section-content">${{renderMarkdown(s.query)}}</div>
                </div>
                <div class="section">
                    <h3>检查项列表 (${{s.check_list.length}})</h3>
                    <div class="section-content">${{s.check_list.map((c,i) => `${{i+1}}. ${{c.description || c.check_name}}`).join('\\n')}}</div>
                </div>
                <div class="section">
                    <h3>环境文件 (${{s.environment.length}})</h3>
                    <div class="section-content">${{s.environment.map(e => e.path).join('\\n')}}</div>
                </div>
                <div class="section">
                    <h3>用户模拟器Prompt</h3>
                    <div class="code-box">${{renderMarkdown(s.user_simulator_prompt || '无')}}</div>
                </div>
            `;
            document.getElementById('modal').classList.add('active');
        }}

        function closeModal() {{
            document.getElementById('modal').classList.remove('active');
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        function renderMarkdown(text) {{
            if (!text) return '';
            // 使用marked渲染Markdown
            return marked.parse(text);
        }}

        document.getElementById('search').addEventListener('input', e => {{
            const q = e.target.value.toLowerCase();
            filtered = allSamples.filter(s =>
                s.data_id.toLowerCase().includes(q) ||
                s.query.toLowerCase().includes(q)
            );
            render();
        }});

        document.getElementById('modal').onclick = e => {{
            if (e.target.id === 'modal') closeModal();
        }};

        render();
    </script>
</body>
</html>'''

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated HTML viewer → {output_path}")

    def export_check_revision(self, samples, revision_dir):
        """仅导出评测方案（checklist + judge_criteria）到 revision 目录

        用于在不重新生成完整样本的情况下，单独迭代评测方案。

        输出：
        - revision_dir/checklist.jsonl: 每行 {data_id, check_list}
        - revision_dir/judge_criteria/: 从 check_definitions 目录复制的 criteria 文件
        - revision_dir/meta.json: revision 元数据
        """
        import shutil

        revision_path = Path(revision_dir)
        revision_path.mkdir(parents=True, exist_ok=True)

        # 1. 导出 checklist.jsonl
        checklist_file = revision_path / "checklist.jsonl"
        with open(checklist_file, 'w', encoding='utf-8') as f:
            for sample in samples:
                entry = {
                    "data_id": sample["data_id"],
                    "check_list": sample["check_list"]
                }
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')

        print(f"\n✓ Exported {len(samples)} checklists → {checklist_file}")

        # 统计检查项信息
        if samples:
            check_count = len(samples[0]["check_list"])
            dims = {}
            for c in samples[0]["check_list"]:
                dim = c.get('dimension_id', 'unknown')
                dims[dim] = dims.get(dim, 0) + 1
            print(f"  Check items per sample: {check_count}")
            for d, n in sorted(dims.items()):
                print(f"    {d}: {n}")

        # 2. 复制 judge_criteria 目录（优先从check_definitions，回退到design目录）
        if self.check_definitions_dir:
            src_criteria = self.check_definitions_dir / "judge_criteria"
        else:
            src_criteria = self.base_dir / "judge_criteria"
        dst_criteria = revision_path / "judge_criteria"
        if src_criteria.exists():
            if dst_criteria.exists():
                shutil.rmtree(dst_criteria)
            shutil.copytree(src_criteria, dst_criteria)
            criteria_files = list(dst_criteria.rglob("*"))
            print(f"✓ Copied judge_criteria ({len([f for f in criteria_files if f.is_file()])} files) → {dst_criteria}")
        else:
            print(f"  Warning: {src_criteria} not found, skipping judge_criteria copy")

        # 3. 生成 revision 元数据
        meta = {
            "generated_at": __import__('datetime').datetime.now().isoformat(),
            "sample_count": len(samples),
            "check_count_per_sample": len(samples[0]["check_list"]) if samples else 0,
            "data_ids": [s["data_id"] for s in samples],
            "source_design_dir": str(self.base_dir),
        }
        meta_file = revision_path / "meta.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"✓ Written revision metadata → {meta_file}")

    def validate_samples(self, samples):
        """验证样本格式"""
        print("\nValidating samples...")

        required_fields = ['data_id', 'query', 'system', 'servers', 'environment', 'check_list']

        for idx, sample in enumerate(samples, 1):
            # 检查必需字段
            for field in required_fields:
                if field not in sample:
                    print(f"  Error in sample {idx}: Missing field '{field}'")
                    return False

            # 检查environment格式
            if not isinstance(sample['environment'], list) or len(sample['environment']) == 0:
                print(f"  Error in sample {idx}: Invalid environment")
                return False

            # 检查check_list格式
            if not isinstance(sample['check_list'], list) or len(sample['check_list']) == 0:
                print(f"  Error in sample {idx}: Invalid check_list")
                return False

        print(f"  ✓ All {len(samples)} samples validated successfully")
        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='生成小说创作场景评测样本')
    parser.add_argument('--output', '-o', default='samples/eval_dsv1.jsonl',
                        help='输出文件路径 (默认: samples/eval_dsv1.jsonl)')
    parser.add_argument('--export-check-revision', metavar='DIR',
                        help='仅导出评测方案到指定 revision 目录（不生成完整样本）。'
                             '示例: --export-check-revision check_revisions/rev_007')
    args = parser.parse_args()

    # 使用当前目录作为base_dir
    generator = NovelSampleGenerator(".")

    # 生成样本（两种模式都需要先生成内存中的样本以构建 checklist）
    samples = generator.generate_samples()

    # 验证样本
    if not generator.validate_samples(samples):
        print("\n✗ Sample validation failed")
        return 1

    if args.export_check_revision:
        # 仅导出评测方案模式
        generator.export_check_revision(samples, args.export_check_revision)
    else:
        # 完整样本生成模式
        generator.save_samples(samples, args.output)

    return 0


if __name__ == "__main__":
    exit(main())
