# Demystifying Evals for AI Agents

> Source: Anthropic Engineering Blog, Published Jan 09, 2026
> Authors: Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe

The capabilities that make agents useful also make them difficult to evaluate. The strategies that work across deployments combine techniques to match the complexity of the systems they measure.

## Introduction

Good evaluations help teams ship AI agents more confidently. Without them, it's easy to get stuck in reactive loops—catching issues only in production, where fixing one failure creates others. Evals make problems and behavioral changes visible before they affect users, and their value compounds over the lifecycle of an agent.

As we described in Building effective agents, agents operate over many turns: calling tools, modifying state, and adapting based on intermediate results. These same capabilities that make AI agents useful—autonomy, intelligence, and flexibility—also make them harder to evaluate.

Through our internal work and with customers at the frontier of agent development, we've learned how to design more rigorous and useful evals for agents. Here's what's worked across a range of agent architectures and use cases in real-world deployment.

## The Structure of an Evaluation

An **evaluation** ("eval") is a test for an AI system: give an AI an input, then apply grading logic to its output to measure success. In this post, we focus on **automated evals** that can be run during development without real users.

**Single-turn evaluations** are straightforward: a prompt, a response, and grading logic. For earlier LLMs, single-turn, non-agentic evals were the main evaluation method. As AI capabilities have advanced, **multi-turn evaluations** have become increasingly common.

In a simple eval, an agent processes a prompt, and a grader checks if the output matches expectations. For a more complex multi-turn eval, a coding agent receives tools, a task (building an MCP server in this case), and an environment, executes an "agent loop" (tool calls and reasoning), and updates the environment with the implementation. Grading then uses unit tests to verify the working MCP server.

**Agent evaluations** are even more complex. Agents use tools across many turns, modifying state in the environment and adapting as they go—which means mistakes can propagate and compound. Frontier models can also find creative solutions that surpass the limits of static evals. For instance, Opus 4.5 solved a τ2-bench problem about booking a flight by discovering a loophole in the policy. It "failed" the evaluation as written, but actually came up with a better solution for the user.

### Key Definitions

When building agent evaluations, we use the following definitions:

- A **task** (a.k.a **problem** or **test case**) is a single test with defined inputs and success criteria.
- Each attempt at a task is a **trial**. Because model outputs vary between runs, we run multiple trials to produce more consistent results.
- A **grader** is logic that scores some aspect of the agent's performance. A task can have multiple graders, each containing multiple assertions (sometimes called **checks**).
- A **transcript** (also called a **trace** or **trajectory**) is the complete record of a trial, including outputs, tool calls, reasoning, intermediate results, and any other interactions. For the Anthropic API, this is the full messages array at the end of an eval run - containing all the calls to the API and all of the returned responses during the evaluation.
- The **outcome** is the final state in the environment at the end of the trial. A flight-booking agent might say "Your flight has been booked" at the end of the transcript, but the outcome is whether a reservation exists in the environment's SQL database.
- An **evaluation harness** is the infrastructure that runs evals end-to-end. It provides instructions and tools, runs tasks concurrently, records all the steps, grades outputs, and aggregates results.
- An **agent harness** (or **scaffold**) is the system that enables a model to act as an agent: it processes inputs, orchestrates tool calls, and returns results. When we evaluate "an agent," we're evaluating the harness *and* the model working together.
- An **evaluation suite** is a collection of tasks designed to measure specific capabilities or behaviors. Tasks in a suite typically share a broad goal. For instance, a customer support eval suite might test refunds, cancellations, and escalations.

## Why Build Evaluations?

When teams first start building agents, they can get surprisingly far through a combination of manual testing, dogfooding, and intuition. More rigorous evaluation may even seem like overhead that slows down shipping. But after the early prototyping stages, once an agent is in production and has started scaling, building without evals starts to break down.

The breaking point often comes when users report the agent feels worse after changes, and the team is "flying blind" with no way to verify except to guess and check. Absent evals, debugging is reactive: wait for complaints, reproduce manually, fix the bug, and hope nothing else regressed. Teams can't distinguish real regressions from noise, automatically test changes against hundreds of scenarios before shipping, or measure improvements.

We've seen this progression play out many times. For instance, Claude Code started with fast iteration based on feedback from Anthropic employees and external users. Later, we added evals—first for narrow areas like concision and file edits, and then for more complex behaviors like over-engineering. These evals helped identify issues, guide improvements, and focus research-product collaborations. Combined with production monitoring, A/B tests, user research, and more, evals provide signals to continue improving Claude Code as it scales.

Writing evals is useful at any stage in the agent lifecycle. Early on, evals force product teams to specify what success means for the agent, while later they help uphold a consistent quality bar.

Descript's agent helps users edit videos, so they built evals around three dimensions of a successful editing workflow: don't break things, do what I asked, and do it well. They evolved from manual grading to LLM graders with criteria defined by the product team and periodic human calibration, and now regularly run two separate suites for quality benchmarking and regression testing. The Bolt AI team started building evals later, after they already had a widely used agent. In 3 months, they built an eval system that runs their agent and grades outputs with static analysis, uses browser agents to test apps, and employs LLM judges for behaviors like instruction following.

Some teams create evals at the start of development; others add them once at scale when evals become a bottleneck for improving the agent. Evals are especially useful at the start of agent development to explicitly encode expected behavior. Two engineers reading the same initial spec could come away with different interpretations on how the AI should handle edge cases. An eval suite resolves this ambiguity. Regardless of when they're created, evals help accelerate development.

Evals also shape how quickly you can adopt new models. When more powerful models come out, teams without evals face weeks of testing while competitors with evals can quickly determine the model's strengths, tune their prompts, and upgrade in days.

Once evals exist, you get baselines and regression tests for free: latency, token usage, cost per task, and error rates can be tracked on a static bank of tasks. Evals can also become the highest-bandwidth communication channel between product and research teams, defining metrics researchers can optimize against.

## How to Evaluate AI Agents

We see several common types of agents deployed at scale today, including coding agents, research agents, computer use agents, and conversational agents. Each type may be deployed across a wide variety of industries, but they can be evaluated using similar techniques.

### Types of Graders for Agents

Agent evaluations typically combine three types of graders: code-based, model-based, and human. Each grader evaluates some portion of either the transcript or the outcome.

#### Code-based Graders

**Methods**: String match checks (exact, regex, fuzzy, etc.), binary tests (fail-to-pass, pass-to-pass), static analysis (lint, type, security), outcome verification, tool calls verification (tools used, parameters), transcript analysis (turns taken, token usage).

**Strengths**: Fast, cheap, objective, reproducible, easy to debug, verify specific conditions.

**Weaknesses**: Brittle to valid variations that don't match expected patterns exactly, lacking in nuance, limited for evaluating some more subjective tasks.

#### Model-based Graders

**Methods**: Rubric-based scoring, natural language assertions, pairwise comparison, reference-based evaluation, multi-judge consensus.

**Strengths**: Flexible, scalable, captures nuance, handles open-ended tasks, handles freeform output.

**Weaknesses**: Non-deterministic, more expensive than code, requires calibration with human graders for accuracy.

#### Human Graders

**Methods**: SME review, crowdsourced judgment, spot-check sampling, A/B testing, inter-annotator agreement.

**Strengths**: Gold standard quality, matches expert user judgment, used to calibrate model-based graders.

**Weaknesses**: Expensive, slow, often requires access to human experts at scale.

For each task, scoring can be weighted (combined grader scores must hit a threshold), binary (all graders must pass), or a hybrid.

### Capability vs. Regression Evals

**Capability or "quality" evals** ask, "What can this agent do well?" They should start at a low pass rate, targeting tasks the agent struggles with and giving teams a hill to climb.

**Regression evals** ask, "Does the agent still handle all the tasks it used to?" and should have a nearly 100% pass rate. They protect against backsliding, as a decline in score signals that something is broken and needs to be improved.

After an agent is launched and optimized, capability evals with high pass rates can "graduate" to become a regression suite that is run continuously to catch any drift. Tasks that once measured "Can we do this at all?" then measure "Can we still do this reliably?"

### Evaluating Coding Agents

**Coding agents** write, test, and debug code, navigating codebases and running commands much like a human developer. Effective evals for modern coding agents usually rely on well-specified tasks, stable test environments, and thorough tests for the generated code.

Deterministic graders are natural for coding agents because software is generally straightforward to evaluate: does the code run and do the tests pass? Two widely used coding agent benchmarks, SWE-bench Verified and Terminal-Bench, follow this approach. SWE-bench Verified gives agents GitHub issues from popular Python repositories and grades solutions by running the test suite; a solution passes only if it fixes the failing tests without breaking existing ones. LLMs have progressed from 40% to >80% on this eval in just one year. Terminal-Bench takes a different track: it tests end-to-end technical tasks, such as building a Linux kernel from source or training an ML model.

Once you have a set of pass-or-fail tests for validating the key *outcomes* of a coding task, it's often useful to also grade the transcript. For instance, heuristics-based code quality rules can evaluate the generated code based on more than passing tests, and model-based graders with clear rubrics can assess behaviors like how the agent calls tools or interacts with the user.

**Example: Theoretical evaluation for a coding agent**

Consider a coding task where the agent must fix an authentication bypass vulnerability:

```yaml
task:
  id: "fix-auth-bypass_1"
  desc: "Fix authentication bypass when password field is empty and ..."
  graders:
    - type: deterministic_tests
      required: [test_empty_pw_rejected.py, test_null_pw_rejected.py]
    - type: llm_rubric
      rubric: prompts/code_quality.md
    - type: static_analysis
      commands: [ruff, mypy, bandit]
    - type: state_check
      expect:
        security_logs: {event_type: "auth_blocked"}
    - type: tool_calls
      required:
        - {tool: read_file, params: {path: "src/auth/*"}}
        - {tool: edit_file}
        - {tool: run_tests}
  tracked_metrics:
    - type: transcript
      metrics: [n_turns, n_toolcalls, n_total_tokens]
    - type: latency
      metrics: [time_to_first_token, output_tokens_per_sec, time_to_last_token]
```

### Evaluating Conversational Agents

**Conversational agents** interact with users in domains like support, sales, or coaching. Unlike traditional chatbots, they maintain state, use tools, and take actions mid-conversation. Effective evals for conversational agents usually rely on verifiable end-state outcomes and rubrics that capture both task completion and interaction quality. Unlike most other evals, they often require a second LLM to simulate the user.

Success for conversational agents can be multidimensional: is the ticket resolved (state check), did it finish in <10 turns (transcript constraint), and was the tone appropriate (LLM rubric)? Two benchmarks that incorporate multidimensionality are τ-Bench and its successor, τ2-Bench. These simulate multi-turn interactions across domains like retail support and airline booking, where one model plays a user persona while the agent navigates realistic scenarios.

**Example: Theoretical evaluation for a conversational agent**

```yaml
graders:
  - type: llm_rubric
    rubric: prompts/support_quality.md
    assertions:
      - "Agent showed empathy for customer's frustration"
      - "Resolution was clearly explained"
      - "Agent's response grounded in fetch_policy tool results"
  - type: state_check
    expect:
      tickets: {status: resolved}
      refunds: {status: processed}
  - type: tool_calls
    required:
      - {tool: verify_identity}
      - {tool: process_refund, params: {amount: "<=100"}}
      - {tool: send_confirmation}
  - type: transcript
    max_turns: 10
```

### Evaluating Research Agents

**Research agents** gather, synthesize, and analyze information, then produce outputs like an answer or report. Unlike coding agents where unit tests provide binary pass/fail signals, research quality can only be judged relative to the task. What counts as "comprehensive," "well-sourced," or even "correct" depends on context.

Research evals face unique challenges: experts may disagree on whether a synthesis is comprehensive, ground truth shifts as reference content changes constantly, and longer, more open-ended outputs create more room for mistakes.

One strategy to build research agent evals is to combine grader types. Groundedness checks verify that claims are supported by retrieved sources, coverage checks define key facts a good answer must include, and source quality checks confirm the consulted sources are authoritative. For tasks with objectively correct answers, exact match works. An LLM can flag unsupported claims and gaps in coverage but also verify the open-ended synthesis for coherence and completeness.

### Computer Use Agents

**Computer use agents** interact with software through the same interface as humans—screenshots, mouse clicks, keyboard inputs, and scrolling—rather than through APIs or code execution. They can use any application with a graphical user interface (GUI).

Evaluation requires running the agent in a real or sandboxed environment where it can use software applications and checking whether it achieved the intended outcome. WebArena tests browser-based tasks, using URL and page state checks to verify the agent navigated correctly. OSWorld extends this to full operating system control, with evaluation scripts that inspect diverse artifacts after task completion.

### Non-determinism in Evaluations

Agent behavior varies between runs, which makes evaluation results harder to interpret. Each task has its own success rate—maybe 90% on one task, 50% on another—and a task that passed on one eval run might fail on the next.

Two metrics help capture this nuance:

**pass@k** measures the likelihood that an agent gets at least one correct solution in *k* attempts. As *k* increases, pass@k score rises: more "shots on goal" means higher odds of at least 1 success. A score of 50% pass@1 means that a model succeeds at half the tasks in the eval on its first try.

**pass^k** measures the probability that *all k* trials succeed. As *k* increases, pass^k falls since demanding consistency across more trials is a harder bar to clear. If your agent has a 75% per-trial success rate and you run 3 trials, the probability of passing all three is (0.75)³ ≈ 42%.

Both metrics are useful: pass@k for tools where one success matters, pass^k for agents where consistency is essential.

## Going from Zero to One: A Roadmap to Great Evals

This section lays out practical, field-tested advice for going from no evals to evals you can trust.

### Step 0: Start Early

We see teams delay building evals because they think they need hundreds of tasks. In reality, 20-50 simple tasks drawn from real failures is a great start. After all, in early agent development, each change to the system often has a clear, noticeable impact, and this large effect size means small sample sizes suffice. More mature agents may need larger, more difficult evals to detect smaller effects, but it's best to take the 80/20 approach in the beginning.

### Step 1: Start with What You Already Test Manually

Begin with the manual checks you run during development—the behaviors you verify before each release and common tasks end users try. If you're already in production, look at your bug tracker and support queue. Converting user-reported failures into test cases ensures your suite reflects actual usage.

### Step 2: Write Unambiguous Tasks with Reference Solutions

A good task is one where two domain experts would independently reach the same pass/fail verdict. Could they pass the task themselves? If not, the task needs refinement. Ambiguity in task specifications becomes noise in metrics.

Each task should be passable by an agent that follows instructions correctly. With frontier models, a 0% pass rate across many trials (i.e. 0% pass@100) is most often a signal of a broken task, not an incapable agent.

### Step 3: Build Balanced Problem Sets

Test both the cases where a behavior *should* occur and where it *shouldn't*. One-sided evals create one-sided optimization. For instance, if you only test whether the agent searches when it should, you might end up with an agent that searches for almost everything.

We learned this firsthand when building evals for web search in Claude.ai. The challenge was preventing the model from searching when it shouldn't, while preserving its ability to do extensive research when appropriate.

### Step 4: Build a Robust Eval Harness with a Stable Environment

It's essential that the agent in the eval functions roughly the same as the agent used in production, and that the environment itself doesn't introduce further noise. Each trial should be "isolated" by starting from a clean environment. Unnecessary shared state between runs can cause correlated failures due to infrastructure flakiness rather than agent performance.

### Step 5: Design Graders Thoughtfully

Choose deterministic graders where possible, LLM graders where necessary or for additional flexibility, and human graders judiciously for additional validation.

There is a common instinct to check that agents followed very specific steps like a sequence of tool calls in the right order. We've found this approach too rigid and results in overly brittle tests, as agents regularly find valid approaches that eval designers didn't anticipate. It's often better to grade what the agent produced, not the path it took.

For tasks with multiple components, build in partial credit. A support agent that correctly identifies the problem and verifies the customer but fails to process a refund is meaningfully better than one that fails immediately.

Model grading often takes careful iteration to validate accuracy. LLM-as-judge graders should be closely calibrated with human experts. To avoid hallucinations, give the LLM a way out, like providing an instruction to return "Unknown" when it doesn't have enough information.

### Step 6: Check the Transcripts

You won't know if your graders are working well unless you read the transcripts and grades from many trials. When a task fails, the transcript tells you whether the agent made a genuine mistake or whether your graders rejected a valid solution. Reading transcripts is how you verify that your eval is measuring what actually matters.

### Step 7: Monitor for Capability Eval Saturation

An eval at 100% tracks regressions but provides no signal for improvement. **Eval saturation** occurs when an agent passes all of the solvable tasks, leaving no room for improvement. As evals approach saturation, progress will also slow, as only the most difficult tasks remain.

As a rule, we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts. If grading is unfair, tasks are ambiguous, valid solutions are penalized, or the harness constrains the model, the eval should be revised.

### Step 8: Keep Evaluation Suites Healthy Long-term

An eval suite is a living artifact that needs ongoing attention and clear ownership to remain useful.

At Anthropic, we experimented with various approaches to eval maintenance. What proved most effective was establishing dedicated evals teams to own the core infrastructure, while domain experts and product teams contribute most eval tasks and run the evaluations themselves.

We recommend practicing eval-driven development: build evals to define planned capabilities before agents can fulfill them, then iterate until the agent performs well.

## How Evals Fit with Other Methods

Automated evaluations can be run against an agent in thousands of tasks without deploying to production or affecting real users. But this is just one of many ways to understand agent performance. A complete picture includes production monitoring, user feedback, A/B testing, manual transcript review, and systematic human evaluation.

### Overview of Approaches

| Method | Pros | Cons |
|--------|------|------|
| **Automated evals** | Faster iteration, fully reproducible, no user impact, can run on every commit | Requires up-front investment, ongoing maintenance, can create false confidence |
| **Production monitoring** | Reveals real user behavior, catches issues synthetic evals miss | Reactive, signals can be noisy, requires instrumentation |
| **A/B testing** | Measures actual user outcomes, controls for confounds | Slow (days/weeks), only tests deployed changes |
| **User feedback** | Surfaces unanticipated problems, comes with real examples | Sparse and self-selected, skews toward severe issues |
| **Manual transcript review** | Builds intuition, catches subtle quality issues | Time-intensive, doesn't scale, inconsistent coverage |
| **Systematic human studies** | Gold-standard quality judgments from multiple raters | Expensive, slow turnaround, inter-rater disagreement |

These methods map to different stages of agent development. Automated evals are especially useful pre-launch and in CI/CD. Production monitoring kicks in post-launch. A/B testing validates significant changes once you have sufficient traffic. User feedback and transcript review are ongoing practices. Reserve systematic human studies for calibrating LLM graders or evaluating subjective outputs.

Like the Swiss Cheese Model from safety engineering, no single evaluation layer catches every issue. With multiple methods combined, failures that slip through one layer are caught by another. The most effective teams combine these methods: automated evals for fast iteration, production monitoring for ground truth, and periodic human review for calibration.

## Appendix: Eval Frameworks

Several open-source and commercial frameworks can help teams implement agent evaluations:

- **Harbor**: Designed for running agents in containerized environments, with infrastructure for running trials at scale across cloud providers and a standardized format for defining tasks and graders.
- **Promptfoo**: A lightweight, flexible, open-source framework focusing on declarative YAML configuration for prompt testing, with assertion types ranging from string matching to LLM-as-judge rubrics.
- **Braintrust**: A platform combining offline evaluation with production observability and experiment tracking.
- **LangSmith**: Offers tracing, offline and online evaluations, and dataset management with tight LangChain integration.
- **Langfuse**: Similar capabilities as a self-hosted open-source alternative for teams with data residency requirements.

Many teams combine multiple tools, roll their own eval framework, or just use simple evaluation scripts as a starting point. It's often best to quickly pick a framework that fits your workflow, then invest your energy in the evals themselves by iterating on high-quality test cases and graders.
