# Universal Scenario Framework - Agent Guide

## Language & Style
- **Always respond in Chinese** (中文思考和回复)
- Professional, concise, direct communication
- Use TodoWrite proactively for task planning and tracking

## MANDATORY: 动手前先查已有脚本
- **写任何脚本/内联代码之前，必须先读 `scripts/README.md`**（每个场景目录下都有），确认没有现成脚本能完成任务
- 已有的常用操作脚本：
  - **拉取远程评测结果**: `python3 remote_deploy/fetch_results.py --port {8080|8082|8083|8084} --download-all`
    - **重要**: 默认只比较样本数，样本数一致就跳过。如果远程有新版 check_result（如新 revision），必须加 `--force` 强制重新下载：
      `python3 remote_deploy/fetch_results.py --port {8080|8082|8083|8084} --download-all --force`
  - **批量重检**: `./scripts/batch_recheck.sh --only-checks "X,Y" --add --parallel 4`
  - **单模型统计**: `python scripts/analysis/generate_statistics.py --eval-dir DIR --output-dir OUT [--remote-url URL]`
  - **横评报告**: `python scripts/analysis/generate_cross_model_report.py`
- **禁止重复造轮子** — 如果现有脚本能做，直接用；不能做，先扩展现有脚本而非新写

## MANDATORY: 三个场景的结构差异备忘

### novel_to_script (NTS)
- **设计版本**: 只有 1 个版本，设计文件直接在项目根目录（`unified_scenario_design.yaml`、`BusinessRules.md`）
- **samples 位置**: `samples/*.jsonl`（根目录下，如 `samples/eval_nts_v3.jsonl`）
- **check_revisions**: `check_definitions/check_revisions/` — **目前为空**，没有 revision 目录
- **check 结果文件名**: `check_result.json`（无版本后缀）
- **checker 模式**: samples 模式（check_list 在 samples jsonl 里）
- **当前评测样本**: `eval_nts_v3.jsonl`（24个样本）

### shortdrama (SD)
- **设计版本**: 3 个版本（design_v1/v2/v3），**只跑 v3**
- **samples 位置**: `samples/*.jsonl`（根目录下，如 `samples/eval_dsv3.jsonl`）— 不在 design_v3/ 下！
- **check_revisions**: `check_definitions/check_revisions/rev_001~rev_006`（最新 rev_006）
- **check 结果文件名**: `check_result_rev006.json`（带版本后缀）
- **checker 模式**: `batch_recheck.sh` 默认自动检测最新 revision，无需手动指定
- **当前评测样本**: `eval_dsv3.jsonl`（32个样本）

### novel_writing_alchemist (NWA)
- **设计版本**: 2 个版本（design_v1/v2），**两个版本都跑**，合并出报告
- **samples 位置**: `design_v1/samples/*.jsonl` 和 `design_v2/samples/*.jsonl` — **在各自 design 目录内部**，不在根目录
  - dsv1: `design_v1/samples/eval_dsv1.jsonl`（14个样本）
  - dsv2: `design_v2/samples/eval_dsv2.jsonl`（10个常规 + 5个 ultra_short = 15个样本）
- **check_revisions**: `check_definitions/check_revisions/rev_001~rev_009`（最新 rev_009）
- **check 结果文件名**: `check_result_rev009.json`（带版本后缀）
- **checker 模式**: revision 模式（`--revision 008`）或 samples 模式均可，但必须确保 judge_criteria 被部署
- **eval 目录命名**: `eval_dsv1_*` 和 `eval_dsv2_*`（按设计版本区分）

#### ⚠️ NWA ultra_short 样本位置（绝对不要搞错）
- **ultra_short 样本就在 dsv2 的 eval 目录里**，和常规样本混在一起。`eval_dsv2_*` 目录包含 10 个常规 + 5 个 `NW_ULTRA_SHORT_*` = 15 个样本。
- **不需要单独的 `eval_dsv2_ultra_short_*` 目录**。根目录下可能存在一些历史遗留的 `eval_dsv2_ultra_short_*` 目录，那些是早期单独跑的废弃目录，**不要用它们做统计，不要为它们启动新进程**。
- 只有两个模型的 dsv2 目录只有 10 个样本（没有 ultra_short）：**kimi-k2.5**（跑的时候 ultra_short 还没加入 samples）和 **EB5-midtrain**（同理）。其他 7 个模型的 dsv2 目录都已包含 15 个样本。
- **验证方法**: `ls evaluation_outputs/eval_dsv2_*_{model}/NW_ULTRA_SHORT*.json | wc -l` 应该返回 5（或 0 表示该模型确实没有 ultra_short）。

### 关键差异总结

| | NTS | SD | NWA |
|---|---|---|---|
| 设计版本数 | 1 | 3（只跑v3） | 2（都跑） |
| samples 位置 | `samples/` | `samples/` | `design_v{1,2}/samples/` |
| check_revisions | 空 | rev_001~006（最新006） | rev_001~009（最新009） |
| check_result 文件名 | `check_result.json` | `check_result_rev006.json` | `check_result_rev009.json` |
| 项目根目录有 samples/ | 是 | 是 | **否** |

## MANDATORY: Checker 调用规范（三个场景通用）

**novel_to_script、shortdrama、novel_writing_alchemist 三个场景的 checker 入口脚本完全一样。永远使用 `batch_recheck.sh`，不要自己拼 `checker.py` 命令。**

### 正确调用方式

```bash
# 全量检查所有模型所有样本（自动查找samples文件，不需要手动指定）
./scripts/batch_recheck.sh --parallel 4

# 只检查特定模型目录
./scripts/batch_recheck.sh --pattern "eval_nts_v3_*_claude*"

# 只检查特定样本（跨所有模型目录）
./scripts/batch_recheck.sh --data-id NTS_HISTORICAL_MEDIUM_3EP_FLEX_DOUYIN_001

# 只检查特定模型 + 特定样本
./scripts/batch_recheck.sh --pattern "eval_nts_v3_*_claude*" --data-id NTS_HISTORICAL_MEDIUM_3EP_FLEX_DOUYIN_001

# 增量重跑指定检查项（在已有check_result上覆盖）
./scripts/batch_recheck.sh --only-checks "场景数量合理,内容单元密度" --add --parallel 4

# resume模式（跳过已有结果）
./scripts/batch_recheck.sh --parallel 4 --resume
```

### 各场景 samples 文件位置（batch_recheck.sh 会自动查找）
- **novel_to_script**: `samples/*.jsonl`（如 `samples/eval_nts_v3.jsonl`）
- **shortdrama**: `samples/*.jsonl`（如 `samples/eval_dsv3.jsonl`）
- **novel_writing_alchemist**: `design_v2/samples/*.jsonl`（如 `design_v2/samples/eval_dsv2.jsonl`）
  - NWA 的 samples 在 `design_v2/samples/` 下，不在根目录的 `samples/` 下！
  - dsv1 样本: `design_v1/samples/`，dsv2 样本: `design_v2/samples/`

### judge_criteria 自动部署机制
- samples 的 environment 字段**不包含** judge_criteria 文件（历史原因）
- `recheck_with_new_checklist.sh` 现在会在 samples 模式下**自动检测并补充部署** judge_criteria
- 逻辑：如果 `_env/judge_criteria/` 不存在，自动从 `check_definitions/check_revisions/rev_最新/judge_criteria/` 复制
- 三个场景（NTS/SD/NWA）的 recheck 脚本都已加入此逻辑

### recheck 时 `_env` 环境一致性保障

**核心原则：recheck 用的是项目根目录 `env/` 下的 checker 代码（不是 `_env/` 里的），但 `_env/` 里的数据文件（data_pools、judge_criteria）必须正确。**

**recheck 脚本自动部署的内容：**
- `judge_criteria`：从最新 rev 目录复制
- `data_pools`（NWA）：根据 eval 目录名判断 dsv1/dsv2，从对应 `design_v{1,2}/data_pools` 强制覆盖

**历史教训：**
1. **data_pools 缺失/版本错乱** — NWA 的 dsv1 和 dsv2 共享 11 个 data_id，但 data_pools 内容不同（dsv1 只有 3 个 skill，dsv2 有 8 个）。如果 dsv1 的 `_env` 错误地包含了 dsv2 的 data_pools，`skip_if_file_not_exists` 不生效，检查项会误判为 fail 而非 skip，导致通过率分母膨胀
2. **修改 `env/checker_score.py` 后忘记 commit+push** — 远程 recheck/rescore 仍用旧版 scorer，导致 gate 检查项无法被正确归入 gate_layer（`quality_tier == "basic"` 没包含 `"gate"`），gate_triggered 永远为 False
3. **操作完整链路**：本地改代码 → commit → `git push github main` → 远程 `https_proxy=... git pull` → 远程 rescore/recheck。任何一步漏了都会导致远程用旧代码

### ⚠️ 开发阶段必须使用 revision 模式，禁止使用 samples 模式

**核心原则：checklist 还在迭代时，永远用 revision 模式。只有 checklist 完全固化不再改了，才能把最终版写入 samples jsonl 并用 samples 模式。**

原因：samples jsonl 里的 `check_list` 是生成时的快照。checklist 每次迭代（新增检查项、修改 quality_tier/参数等），samples 里的快照就过时了。用 samples 模式跑 checker 会使用过时的 checklist 定义，导致结果与当前 revision 不一致。

**历史教训**：rev_008 把 gate 检查项的 `quality_tier` 从 `"basic"` 改为语义更准确的 `"gate"`，但 samples jsonl 里的快照还是旧的 `"basic"`。如果用 samples 模式跑，scorer 的归堆逻辑和 revision 模式跑出来的结果会不一致。

### 禁止事项
- **禁止直接调用 `python3 env/checker.py`** — 参数复杂且容易出错
- **禁止混淆 checker.py 的参数格式** — checker.py 需要 `--bench --result --model --base-url --api-key`，不是 `--input --env-dir --checklist`
- **绝对禁止使用 inline 模式做 recheck** — inline 模式不部署 environment 文件到 `_env/`，导致 checker 找不到 `judge_criteria` 等外部依赖。所有 semantic_check 类型的检查项都会报"缺少参数: llm_semantic_analysis方法需要启用LLM并提供llm_judge_criteria"而全部 fail。`batch_recheck.sh` 现在会自动查找 samples 文件走 samples 模式，不再默认 inline。**已因此错误浪费了至少3次远程 checker 运行。**
- **之前已多次犯同样错误**：给用户贴了错误的 `checker.py` 直接调用命令导致远程报错。根因是 `batch_recheck.sh` 封装了所有复杂逻辑（bench.json 构造、环境切换、增量合并等），绕过它必然出问题
- **三个场景的 `batch_recheck.sh` 已支持自动检测最新 revision** — 不指定 `--samples` 或 `--revision` 时，脚本会自动查找 `check_definitions/check_revisions/` 下最新的 `rev_NNN` 目录，使用其完整 checklist，并自动设置 `--output-suffix _revNNN`。NTS 目前无 revision 目录，会 fallback 到 samples 模式。直接 `./scripts/batch_recheck.sh --parallel 4` 即可，无需手动指定版本号。

## MANDATORY: 远程评测启动规范（三个场景通用）

**启动/resume远程评测时，永远使用场景目录下的 `remote_deploy/run_eval.sh` 脚本，不要手拼 `agent.py` 或 `executor.py` 命令。**

> `run_test.sh`（根目录）是本地用的，`remote_deploy/run_eval.sh` 是远程用的。两者参数格式相同但环境配置不同（venv路径、framework路径等）。

### 正确调用方式

```bash
# 在远程 10.25.70.163 上执行
cd ~/novel_eval/{novel-to-script|shortdrama-eval|novel-writing-alchemist}

# 首次启动某模型（使用默认样本文件）
nohup bash remote_deploy/run_eval.sh {模型名} > logs/{模型名}.log 2>&1 &

# 指定样本文件
nohup bash remote_deploy/run_eval.sh {模型名} samples/eval_nts_v3.jsonl > logs/{模型名}.log 2>&1 &

# resume（继续未完成的样本，必须指定已有输出目录）
nohup bash remote_deploy/run_eval.sh {模型名} --resume-dir=evaluation_outputs/{已有输出目录名} > logs/{模型名}_resumeN.log 2>&1 &
```

模型名参数示例：`claude`、`gemini`、`doubao`、`ernie`、`glm`、`kimi`

### 禁止事项
- **禁止手拼 `python3 agent.py --bench bench.json ...`** 或 `python3 executor.py ...` — 参数多且容易出错（API key、base_url、no_proxy/https_proxy、venv 激活等都封装在 run_eval.sh 里）
- **之前犯过的错误**：手拼 agent.py 命令导致引用不存在的 bench.json，进程启动即退出；resume 时漏掉 `--resume-dir` 导致创建新目录而非续跑

## MANDATORY: 远程 git 操作铁律

### 绝对禁止在远程删除 evaluation_outputs 文件
- **远程的 evaluation_outputs 是花大量时间和 LLM 调用跑出来的**，删了就没了（或要重跑几小时甚至一天）
- 遇到 `git pull` 因 untracked evaluation_outputs 文件冲突时，**禁止用 `find ... -delete`、`git clean -fd evaluation_outputs/`、`rm -rf` 等删除命令**
- **正确做法**：只拉代码文件，不碰 evaluation_outputs：
  ```bash
  git fetch origin
  git checkout origin/main -- env/ scripts/ check_definitions/
  ```
- **历史教训**：为解决 pull 冲突执行了 `find evaluation_outputs -name "check_result_rev009.json" -delete`，导致远程跑了一天的 rev009 结果全部丢失

### 代码和数据要分开走
- **代码**（env/、scripts/、check_definitions/ 等）：本地开发 → push → 远程 `git fetch && git checkout origin/main -- 具体目录`
- **数据**（evaluation_outputs/）：远程跑评测/checker 产生 → 用 `fetch_results.py` 拉回本地
- **禁止在本地直接修改 evaluation_outputs 然后 commit push** — 这会导致远程 pull 时与远程的 untracked 文件冲突，引发连锁问题
- 如果需要重算分数，push 代码到远程，在远程用 `batch_rescore.sh` 重算

### 给远程命令前先确认基本信息
- **先确认 remote 名称**：本地叫 `github`，远程叫 `origin`，不要搞混
- **先确认 commit 是否已到达远程**：`git fetch` 之后才能 checkout 远程的新 commit
- **先确认文件是否存在**：给 `--revision revNNN` 前先 `ls` 确认远程确实有这个版本的文件
- **不要让用户当调试员** — 所有命令在给出前应该自己验证过可行性

### 已有工具优先
- `checker_score.py` 本身就是独立 CLI 脚本，可以单独跑 scorer 重算分数，不需要用 Python 再包一层
- `batch_rescore.sh` 是 shell 遍历脚本，调用 `checker_score.py` 批量重算，不调 LLM，几秒跑完
- **用法**: `./scripts/batch_rescore.sh --revision rev009 [--dry-run] [--pattern "eval_dsv1_*_claude*"]`

## MANDATORY: Checklist 升级分类及操作 SOP

Checklist 升级按照"改了什么"分为以下几类，每类的影响范围和操作步骤不同。**核心原则：所有模型必须用同一版 checklist，不允许出现不同模型跑不同 checklist 的情况。**

### 升级类型总览

| 类型 | 改了什么 | 需要重跑 checker？ | 在哪跑？ |
|---|---|---|---|
| A. 新增检查项（非 semantic） | checklist.jsonl | 是（仅新增项） | 远程 |
| B. 新增检查项（semantic_check） | checklist.jsonl + judge_criteria YAML | 是（仅新增项） | 远程 |
| C. 修改检查项参数 | checklist.jsonl 里的 params | 是（仅修改项） | 远程 |
| D. 修改检查项元信息 | quality_tier / weight / dimension_id 等 | 否，只需 rescore | 远程（rescore 几秒） |
| E. 删除检查项 | checklist.jsonl 删行 | 否，只需 rescore | 远程（rescore 几秒） |
| F. 修改 judge_criteria 评判标准 | judge_criteria/*.yaml | 是（相关 semantic 项） | 远程 |
| G. 修改 scorer 逻辑 | checker_score.py | 否，只需 rescore | 远程（rescore 几秒） |
| H. 修改 checker 执行逻辑 | checker_execute.py | 看情况 | 远程 |

### 判断核心：是否需要重跑 checker（调 LLM）

- **需要重跑（远程，耗时耗钱）**：A/B/C/F/H — 检查项本身变了，或 checker 判断逻辑变了，必须重新执行
- **只需 rescore（远程，几秒）**：D/E/G — 检查项的判定结果（pass/fail）没变，只是分数计算方式变了

### batch_recheck.sh 的三种运行模式

checker.py 支持 `--existing-result` 和 `--only-checks` 两个独立参数，batch_recheck.sh 通过 `--add` 和 `--only-checks` 暴露：

| batch_recheck.sh 参数 | checker.py 实际行为 | 适用升级类型 |
|---|---|---|
| `--add`（不带 --only-checks） | 在已有结果上，只跑 checklist 里有但已有结果里**没有的**项，已有项跳过 | **A/B: 新增检查项** |
| `--only-checks "X,Y" --add` | 在已有结果上，**重跑** X、Y 并覆盖旧结果，其余保留 | **C/F: 修改已有检查项参数/评判标准** |
| 不带 --add 也不带 --only-checks | 全量重跑所有检查项 | 大改/不确定影响范围时兜底 |

> `--add` 的本质是传 `--existing-result` 给 checker.py，让它加载已有 check_result 做合并。
> `--only-checks` 控制"这次跑哪几项"。两者组合决定最终行为。

### 类型 A/B: 新增检查项

**本地操作：**
```bash
# 1. 创建新 revision 目录
mkdir check_definitions/check_revisions/rev_010
# 2. 基于上一版 checklist 修改，新增检查项
#    - 每个检查项必须有: check_id, check_type, params, description, dimension_id, subcategory_id, quality_tier, weight, is_critical
# 3. 如果是 semantic_check（B类），同时创建 judge_criteria YAML
# 4. 写 meta.json 记录变更
# 5. commit + push
git add check_definitions/check_revisions/rev_010/
git commit -m "NWA rev_010: 新增XXX检查项"
https_proxy=http://agent.baidu.com:8891 git push github main
```

**远程操作：**
```bash
# 1. 拉代码
git fetch origin && git checkout origin/main -- env/ scripts/ check_definitions/

# 2. 从上一版 check_result 复制为新版基础（跨版本继承）
#    --add 只能找同版本的已有结果，新 revision 第一次跑时文件不存在会全量重跑
#    所以必须先 cp 上一版结果作为基础
find evaluation_outputs/eval_dsv* -name "check_result_rev009.json" -exec bash -c '
  cp "$1" "$(dirname "$1")/check_result_rev010.json"
' _ {} \;

# 3. 用 --add 模式：基于刚复制的 rev010 基础，只跑新增的检查项
./scripts/batch_recheck.sh --add --parallel 4
```

**本地收尾：**
```bash
# 1. 拉回结果
python3 remote_deploy/fetch_results.py --port 8080 --download-all
# 2. 统计 + 出报告（见"SOP: Recheck后更新报告的完整流程"）
```

### 类型 C: 修改检查项参数

**远程操作：**
```bash
git fetch origin && git checkout origin/main -- env/ scripts/ check_definitions/

# 同样先从上一版复制基础（如果是新 revision）
find evaluation_outputs/eval_dsv* -name "check_result_rev009.json" -exec bash -c '
  cp "$1" "$(dirname "$1")/check_result_rev010.json"
' _ {} \;

# --only-checks 指定要重跑的项 + --add 保留其余已有结果
./scripts/batch_recheck.sh --only-checks "被修改的检查项名" --add --parallel 4
```

### 类型 D: 修改检查项元信息（quality_tier / weight / dimension_id）

**不需要重跑 checker**，因为 pass/fail 判定没变，只是分数聚合方式变了。

**本地操作：**
```bash
# 1. 修改 checklist.jsonl 里对应字段
# 2. commit + push
```

**远程操作：**
```bash
git fetch origin && git checkout origin/main -- env/ scripts/ check_definitions/
# 只重算分数，不调 LLM
./scripts/batch_rescore.sh --revision rev010
```

**本地收尾：**
```bash
python3 remote_deploy/fetch_results.py --port 8080 --download-all
# 统计 + 出报告
```

### 类型 E: 删除检查项

**不需要重跑 checker**。新 revision 的 checklist.jsonl 里没有该项，rescore 时 check_result 里的旧项会被忽略（scorer 只看当前 check_details 里有的项）。

**操作同 D 类。**

> 注意：如果想彻底清除旧项在 check_result 中的残留，需要用 `--only-checks` 全量 recheck（而非增量）。但对分数计算无影响，通常不必要。

### 类型 F: 修改 judge_criteria 评判标准

**本地操作：**
```bash
# 修改 judge_criteria/*.yaml
# commit + push
```

**远程操作：**
```bash
git fetch origin && git checkout origin/main -- env/ scripts/ check_definitions/
# --only-checks 指定受影响的项 + --add 保留其余已有结果
./scripts/batch_recheck.sh --only-checks "受影响的检查项名1,检查项名2" --add --parallel 4
```

### 类型 G: 修改 scorer 逻辑

**不需要重跑 checker**，只需 rescore。

**本地操作：**
```bash
# 修改 checker_score.py
# commit + push
```

**远程操作：**
```bash
git fetch origin && git checkout origin/main -- env/ scripts/
./scripts/batch_rescore.sh --revision rev009
```

### 一致性保障铁律

1. **一个 revision 必须对所有模型完整跑完**。不允许"claude 跑了 rev010，ernie 还是 rev009"
2. **`--add` 增量模式只用于新增检查项**。修改已有项时，必须用 `--only-checks` 覆盖，不能用 `--resume`（resume 会跳过已有结果）
3. **每次升级前先确认远程当前状态**：
   ```bash
   # 确认所有模型的 check_result 版本一致
   ls evaluation_outputs/eval_dsv*/NW_*_env/check_result_rev*.json | sed 's/.*check_result_//' | sort | uniq -c
   ```
4. **check_result 文件名带 revision 后缀**（如 `check_result_rev010.json`），不同版本结果共存互不覆盖
5. **统计时只读同一 revision 的 check_result**，generate_statistics.py 通过 `--check-result-suffix` 指定

## SOP: Recheck后更新报告的完整流程

每次修复checker并recheck后，在场景目录下（如 `tmp_scenarios/novel_to_script/`）按以下步骤执行：

```bash
# 1. 拉取远程最新check_result
python3 remote_deploy/fetch_results.py --port 8082 --download-all

# 2. 逐模型生成统计（每个模型各跑一次）
python3 scripts/analysis/generate_statistics.py --eval-dir eval_nts_v3_20260219_212800_claude-opus-4-6 --output-dir analysis/opus
python3 scripts/analysis/generate_statistics.py --eval-dir eval_nts_v3_20260219_212802_gemini-3-pro-preview --output-dir analysis/gemini
python3 scripts/analysis/generate_statistics.py --eval-dir eval_nts_v3_20260219_212804_doubao-seed-2-0-pro-260215 --output-dir analysis/doubao
python3 scripts/analysis/generate_statistics.py --eval-dir eval_nts_v3_20260219_212806_ernie-5.0-thinking-preview --output-dir analysis/ernie

# 3. 生成跨模型数据表格（输出 analysis/cross_model_data.md）
python3 scripts/analysis/generate_cross_model_report.py

# 4. 更新横评分析报告（analysis/cross_model_report.md）
#    - cross_model_data.md 是脚本自动生成的纯数据表格（步骤3的输出），是唯一数据源
#    - cross_model_report.md 是人工编写的分析报告，引用data.md的数据
#    - 更新report.md时：读data.md的最新数字，更新report.md中对应的数据点和分析文字
#    - 不要凭记忆手改数字！一切以data.md和statistics.json为准
```

**交付物清单:**
- `analysis/{opus,gemini,doubao,ernie}/statistics.json` — 单模型统计数据
- `analysis/{opus,gemini,doubao,ernie}/statistics.md` — 单模型可读报告
- `analysis/cross_model_data.md` — 跨模型原始数据表格（脚本生成）
- `analysis/cross_model_report.md` — 横评分析报告（人工编写，基于data.md）

## Code Style
- **4-space indentation**, PEP 8, double quotes preferred
- Classes `PascalCase`, functions `snake_case`, constants `UPPER_SNAKE_CASE`
- Tools/Checkers never raise exceptions，返回结构化结果
- **禁止** default/fallback 逻辑、截断字符串、直接编辑生成的 sample 文件

## Project Overview

LLM Agent 能力评测框架。两类评测场景并存：

| 类型 | 目录 | 特点 | 代表场景 |
|------|------|------|----------|
| 精准校验 | `scenarios/` | 规则化 checker，状态机验证 | ad_campaign, crm, hotel_reservation 等 15 个 |
| LLM Judge | `tmp_scenarios/` | semantic_check 为主，LLM 评判内容质量 | novel_writing_alchemist, shortdrama, novel_to_script, knowledge_video_creator |

核心循环：`Sample Synthesis -> Evaluation Execution -> Failure Attribution -> System Iteration`

两类场景共用同一套评测框架：`mcp-benchmark/release/framework/`（agent.py、executor.py 等），区别只在各场景自己的 checker、tools、samples。

### Repository Structure
```
scenarios/                  # 精准校验类场景（15个）
  {name}/
    src/evaluation/         # Checkers, evaluator, tool_manager
    src/simulators/         # MCP server, platform simulator, state manager
    src/tools/              # Business-specific tools
    BusinessRules.md
tmp_scenarios/              # LLM Judge 类场景
  novel_writing_alchemist/  # 一创小说写作
  shortdrama/               # 一创短剧编写
  novel_to_script/          # 二创小说改编短剧
  knowledge_video_creator/  # 知识视频创作
templates/                  # 可复用基础类
mcp-benchmark/              # MCP benchmark 评测框架（agent.py 在此）
docs/                       # 标准文档、分析报告
```

### check_result.json 格式（novel_to_script / shortdrama / novel_writing_alchemist 通用）

```jsonc
{
  "check_version": "rev004",
  "sample_id": "NTS_SUSPENSE_LONG_5EP_FLEX_DOUYIN_001",
  "check_timestamp": "2026-02-22T09:55:16",
  "dimension_scores": {
    "format_compliance": {"total": 5, "passed": 5, "failed": 0, "skipped": 0, "score": 100.0},
    "business_rule_compliance": {"total": 10, "passed": 10, ...},
    "data_consistency": {"total": 2, "passed": 1, ...},
    "content_quality": {"gate_passed": true, "basic": {...}, "advanced": {...}, "content_score": 78.67}
  },
  "overall_result": {"total_score": 81.44, "content_score": 78.67, "process_score": 87.78, "quality_level": "unqualified"},
  "check_details": {
    "检查项中文名": {       // key = 检查项名称，如 "镜头语言标注"、"角色数量约束"
      "check_result": "pass",   // "pass" | "fail" | "skip"
      "reason": "...",
      "details": "...",
      "description": "检查项描述",
      "check_type": "semantic_check",  // checker类型
      "dimension_id": "content_quality",  // 所属维度
      "subcategory_id": "visual_conversion",  // 所属子类
      "quality_tier": "basic",  // "gate" | "basic" | "advanced" | ""(流程类)
      "is_gate": false,
      "is_critical": false,
      "weight": 1.0
    }
    // ... 每个检查项一个entry
  },
  "completion_status": {"total_checks": 35, "completed": 35, "skipped": 0}
}
```

**聚合逐检查项通过率的正确方式：**
```python
for check_name, check_info in data["check_details"].items():
    result = check_info["check_result"]  # "pass" / "fail" / "skip"
```

## Evaluation Sample Cleanup

- **executor 的 resume 只看文件是否存在**，不看 `execution_status`。resume 前必须先删除 error 状态的 JSON 及其 `_env` 目录
- **不要依赖 `execution_report.json`** — 只记录首次运行状态，resume 后不更新
- 判断方法：读每个样本 JSON 的 `execution_status` 字段（`"success"` / `"error"` / `"unknown"`）
- 删除前必须列出完整文件列表让用户确认

## Key References

| Document | Purpose |
|----------|---------|
| Each scenario's `BusinessRules.md` | Business rules defining agent behavior |
| `docs/PROJECT_DEVELOPMENT_STANDARDS_V2.md` | Core 4-step SOP for scenario development |

## Failure Attribution Framework (4 Categories)

When analyzing failed evaluation cases, classify root cause into exactly one of:

1. **Agent Capability Issue** — Agent didn't follow rules, missed information collection, omitted operations
2. **Sample Design Issue** — Checker thresholds wrong, rules ambiguous, user simulator prompt poorly designed
3. **User Simulator Execution Issue** — Simulator deviated from its preset prompt during execution
4. **System Issue** — Tool design flaws, tool return values wrong, checker logic bugs

Always verify `final_state` against agent operation intent using the 3-layer verification:
Tool responsibility boundary -> Agent operation completeness -> Business rule clarity.

## Environment Notes
- **Miniconda** at `/Users/feixiaoxu01/miniconda3` — has `fastmcp`
- **Homebrew python3** at `/opt/homebrew/bin/python3` — has `pandas`, `litellm`, `tabulate` but NOT `fastmcp`
- MCP servers use absolute python path `/Users/feixiaoxu01/miniconda3/bin/python` in `servers.json`
- Agent proxy at `yy.dbh.baidu-int.com` has ~5min idle timeout (causes SSE stream interruption during extended thinking)

## Remote Evaluation Server (10.25.70.163)

### CRITICAL: 访问远程服务器的方式
- **永远不要用 SSH 连接远程服务器！** 本地环境 SSH 连不上 10.25.70.163（网络不通）
- **永远使用 HTTP API（端口 8080/8082/8083/8084）读取远程数据** — 这些 HTTP 服务是专门为此设计的
- 需要在远程执行命令时（git pull、batch_recheck 等），**生成命令让用户手动执行**，不要尝试 SSH
- SSH 信息仅供用户在远程终端上使用，不是给 Agent 用的

### SSH Access (用户手动使用，Agent 不可用)
- **SSH**: `work@10.25.70.163`
- **Base directory**: `/home/work/novel_eval/`
- **Shared venv**: `/home/work/novel_eval/.venv/`
- **Shared framework**: `/home/work/novel_eval/mcp-benchmark/release/framework/`

### Three Evaluation Scenarios & HTTP Services

| Scenario | Repo | Remote Directory | HTTP Port | API List URL |
|----------|------|------------------|-----------|--------------|
| novel_writing_alchemist | `feixiaoxu2022/novel-writing-alchemist` | `~/novel_eval/novel-writing-alchemist/` | **8080** | `http://10.25.70.163:8080/api/list` |
| shortdrama | `feixiaoxu2022/shortdrama-eval` | `~/novel_eval/shortdrama-eval/` | **8083** | `http://10.25.70.163:8083/api/list` |
| novel_to_script | `feixiaoxu2022/novel-to-script` | `~/novel_eval/novel-to-script/` | **8082** | `http://10.25.70.163:8082/api/list` |
| knowledge_video_creator | `feixiaoxu2022/knowledge-video-creator` | `~/novel_eval/knowledge-video-creator/` | **8084** | `http://10.25.70.163:8084/api/list` |

Each HTTP service provides these APIs:
- `/api/list` — List evaluation directories with sample counts and success counts
- `/api/logs` — List log files
- `/api/logs/<filename>?lines=N` — View log tail (use `lines=all` for full log)
- `/api/file/<path>` — Read any file under scenario directory
- `/api/tar/<dirname>` — Download evaluation directory as tar.gz
- `/api/ls/<path>` — Browse directory contents

### Global Proxy & Model API 特殊处理

远程有全局代理 `https_proxy=http://agent.baidu.com:8891`，各模型 API 处理已封装在 `run_eval.sh` 中：
- **ernie**: 需要 `no_proxy=qianfan.baidubce.com` 绕过代理（否则 SSL 错误）
- **GLM**: 需要代理才能连 `open.bigmodel.cn`（agent.py 已处理 `proxies` 参数）
- **其他模型**: 用 HTTP 代理 `yy.dbh.baidu-int.com/v1`，不受影响

### Remote Python Environment

- **必须激活 venv**: `source ~/novel_eval/.venv/bin/activate`（否则缺 litellm）
- `run_eval.sh` 内部会自动激活 venv

### Git Operations

- **远程 git pull 需代理**: `https_proxy=http://agent.baidu.com:8891 git pull`
- **本地 git push**: 本地 remote 名叫 `github`（不是 `origin`），`git push github main` 即可（无需代理可直连）
- **远程 remote 名叫 `origin`**，不要搞混

### Shared Framework Repo

- Local: `/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/mcp-benchmark/release/`
- Remote: `/home/work/novel_eval/mcp-benchmark/release/`
- Repo: `https://github.com/feixiaoxu2022/mcp-benchmark.git` (remote name: `origin`)
- To deploy changes: push locally, then `cd ~/novel_eval/mcp-benchmark/release && git pull` on remote
- If remote has uncommitted changes blocking pull: `git checkout -- <file>` then `git pull`
