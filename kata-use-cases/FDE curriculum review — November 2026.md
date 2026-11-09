---
title: FDE Curriculum Review and U.S. Market Alignment (November 2026)
description: Principal Engineer and Learning Strategy review aligning the Forward-Deployed and Full-Stack AI Engineer curriculum with late-2026 U.S. job market demands
author: Raj Champaneriya
ms.date: 2026-11-09
ms.topic: overview
keywords:
  - forward deployed engineer
  - full-stack engineer
  - ai application engineer
  - agentic ai
  - model context protocol
  - azure ai foundry
  - github copilot
  - evaluation
estimated_reading_time: 12
---

## 1. Executive Summary

Nov 9, 2026 · @Raj Champaneriya

Keep the spine, move the hours. About half of the original plan (66 of 128 hours, projects 3 to 5) teaches how models are trained from scratch. Nothing the major cloud and AI vendors shipped since May 2026, and nothing in U.S. Forward-Deployed Engineer (FDE) or Full-Stack Development Engineer job postings, pays for pretraining mechanics. Employers pay for what Project 1 already does well: measuring systems rigorously, grounding them in enterprise context, building production full-stack and agentic interfaces, governing them with policy as code, and delivering them into customer environments within weeks.

Across the U.S. market, the boundary between Forward-Deployed Engineer, Full-Stack Engineer, and AI Application Engineer has converged. Leading engineering organizations expect engineers to pair AI-assisted software development (GitHub Copilot multi-file agent mode, Microsoft Copilot Studio, cursor/IDE workflows) with production cloud-native architecture (Azure AI Foundry, AWS Bedrock AgentCore, Google Gemini Enterprise Agent Platform, Model Context Protocol, OpenTelemetry, and DevSecOps).

| Decision     | Curriculum Part                         | Strategic Rationale                                                                                                                         |
|--------------|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Keep         | Project 1, Measure before you believe   | AWS, Microsoft, Google, OpenAI, and Anthropic all shipped managed evaluation services in 2026. Rigorous measurement remains your asset.     |
| Keep, widen  | Project 2, Meaning as numbers           | Combine vector retrieval with ontology work. The enterprise context layer is where Microsoft IQ, AWS, and Google now compete.               |
| Add          | Evals that run without you              | Calibrated LLM judges against human labels, simulated multi-turn users, OpenTelemetry trace grading, CI gates, and drift monitoring.        |
| Add          | A production-shaped full-stack agent    | Managed agent runtime, MCP servers, Agent Skills, streaming React/Next.js agent UI, identity, Cedar policy as code, and HITL approvals.     |
| Compress     | Projects 3 to 5 (from 66h to 11h)       | Retain 6 decision-driving topics: tokens/cost, temperature, context degradation, hallucination origins, training basics, and RAG vs FT.     |
| Rebuild      | Project 6, Back to the customer         | Rehearse a 6-week enterprise engagement: technical discovery, threat modeling and security review, executive readout, and handover.         |
| Deprioritize | Scratch micrograd and tiny GPT          | Retain only as an optional weekend track for personal curiosity or video channel content; remove from the core 90-day hiring critical path. |

### Current Baseline and Immediate Action

Days 1 to 9 shipped on schedule: 9 topics in 18 days (14 to 31 October). Day 10 has been open since 30 October with four missed tracker attempts, yet during those same 10 days you committed roughly 20 updates of substantive lab work (`continuous-learning` repo, day-11 README versions A, B, C, and `data/results` C3 runs) that the tracker failed to capture.

The C3 quality jump reflects real engineering, but three variables changed simultaneously: the underlying model (`glm-5.3-flash`), the grader, and the system design. Day 10 must isolate the gain by cause:

1. Re-grade saved runs A, B, C, and C2 using the current grader. Because C2 runs architecture C on `glm-5.3-flash`, the delta from C to C2 isolates the model contribution, and the delta from C2 to C3 isolates the architecture and policy contribution.
2. Draw a clean held-out evaluation set. Cases `c79` and `c80` sit in the current held-out list, but your day-5 notes explicitly reference both, meaning data leakage has occurred on the validation split.
3. Document one quantitative statement per cause with confidence intervals. This attribution paragraph forms the core evidence of the Day 11 Architecture Decision Record (ADR).

The highest-value mechanism you built is currently invisible in the tracker: deterministic escalation rules executing as code prior to LLM drafting, paired with an ontology envelope restricting permissible offers. That architecture directly implements policy as code and semantic grounding.

---

## 2. Gap Analysis

### 2026 Platform Convergence Across Core Vendors

Major platform providers converged on a unified production stack in 2026: managed agent harnesses, integrated trace evaluation, semantic business-context layers, open interoperability standards (MCP, A2A, Agent Skills), and identity governance.

| Theme                              | 2026 Platform Releases                                                                                                                                                                                                                            | Curriculum Impact                                                                                                                                                       |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Managed agent loops as products    | AWS [AgentCore managed harness][aws-harness] GA (Jun). Microsoft [Foundry hosted agents][ms-foundry] (Jun). Google [Gemini Enterprise Agent Platform][gcp-agent] ADK (Apr). OpenAI [Agents API][oai-devday] (Sep). Anthropic [Claude Managed Agents][ant-managed] (May). | Your hand-built loop (Day 8) builds foundational intuition. Next, port C3 to one managed cloud runtime and benchmark on the identical dataset.                          |
| Evaluation as a platform primitive | AWS [AgentCore Evaluations][aws-evals] GA (Mar). Microsoft Foundry Rubric evaluator and trace optimizer (Jun). Google [Agent Evaluations][gcp-evals] GA (Jul) with user simulation and pytest CI. Anthropic Outcomes beta.                        | Expand Project 1 methods into automated pipelines: judge calibration against human labels, user simulation, OpenTelemetry trace grading, and CI gating.                  |
| Enterprise context layers          | Microsoft [IQ family][ms-iq] (Work, Fabric, Foundry IQ) and [Fabric IQ][fabric-iq] ontology preview. AWS AgentCore [knowledge layers][aws-knowledge] (Jun). Google [Gemini enterprise agent][gcp-work] (Oct).                                     | Formalize your ontology experiment as a controlled benchmark: evaluate ontology glossary alone vs. vector retrieval alone vs. hybrid grounding on identical test cases. |
| Open interoperability standards    | Anthropic donated Agent Skills to the [Agentic AI Foundation][aaif-skills] (Oct), joining MCP, A2A, and `AGENTS.md`. Microsoft Foundry Toolboxes aggregate tools behind one MCP endpoint. OpenAI proposed MCP Events.                             | Expose Acme domain tools via an MCP server with OAuth/scoped auth and package the evaluation grader as a portable Agent Skill.                                          |
| Identity, security, and policy     | Microsoft [Agent 365][ms-agent365] registry and RBAC. AWS AgentCore Policy GA using Cedar. Google agent identity, gateway, and dedicated workspace principals.                                                                                    | Add non-human identity management, least-privilege tool scoping, prompt injection defense, and Cedar/OPA policy-as-code enforcement.                                    |
| Constrained routing decisions      | OpenAI [Decisions API][oai-devday] preview for deterministic classification and routing across fixed action sets.                                                                                                                                 | Validates your Day 2 workflow-first architecture. Keep intent classification and escalation deterministic or strictly schema-constrained.                               |
| Stateful long-running memory       | OpenAI Dots, Google coworker agents, Anthropic dreaming research preview, and Microsoft Foundry procedural memory.                                                                                                                                | Cover at the architectural awareness level (state persistence diagrams and session checkpointing) without over-investing build hours.                                   |

> [!NOTE]
> Microsoft Ignite runs 17 to 20 November 2026. Re-verify the Foundry IQ, Agent 365, and GitHub Copilot rows immediately following the keynote announcements.

### Employer-Specific Skill Expectations (U.S. Market)

U.S. job postings for FDE and AI-enabled Full-Stack Engineers grew more than 729% year-over-year ([LeadDev][leaddev-fde]). Analyzing hiring bars across 11 bellwether U.S. employers reveals clear gaps in the original 128-hour plan:

| Target Employer | Core Hiring Bar (Late 2026)                                                                                                   | Gap in Original Curriculum                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Microsoft       | Azure AI Foundry, GitHub Copilot Workspace/Agents, MCP Toolboxes, Microsoft IQ ontology, TypeScript/Python, AB-100            | No Azure AI Foundry deployment, no MCP server implementation, no formal GitHub Copilot agentic workflow lab  |
| Amazon (AWS)    | [AWS FDE pods][stateofai-fde] (45-day delivery), Bedrock AgentCore, Cedar policy, containers, [operational runbooks][pulse2-aws] | Missing Cedar policy-as-code, container/cloud deployment, and structured customer handover artifacts         |
| Google          | Gemini Enterprise Agent Platform, graph-based ADK, online drift monitoring, pytest CI evals, Cloud Run/GKE                    | Missing continuous drift monitoring, simulated multi-turn user harnesses, and cloud-hosted runtime parity    |
| Meta            | Full-stack velocity (React/TypeScript, GraphQL/streaming), Llama open-weight cost/latency optimization, eval rigor            | No front-end streaming UI for agent states/approvals; no latency vs. token cost SLA tradeoff modeling        |
| OpenAI          | [Deployment Company][stateofai-fde] embedded engineering, Agents API, Decisions API, structured outputs, security             | Missing constrained routing benchmarks and enterprise security review documentation                          |
| Anthropic       | [Claude Frontier Academy][ant-academy] model (use-case discovery, security review, handover), MCP, Agent Skills, `AGENTS.md`  | Missing two of Frontier Academy's three pillars: formal threat-model security review and client handover     |
| Stripe          | High-reliability TypeScript/Python APIs, idempotency, human-in-the-loop financial guardrails, deterministic audit             | `issue_refund` tool lacks idempotency keys, transactional rollback, and asynchronous human approval UI       |
| Datadog         | OpenTelemetry genai semantic conventions, distributed trace grading, SLOs for latency/cost/hallucination rate                 | Runs log to local JSONL files without OpenTelemetry spans, trace IDs, or real-time observability dashboards  |
| Thoughtworks    | Hexagonal architecture, evolutionary design, Continuous Delivery for ML/AI (CD4AI), pytest-bdd specification gates            | Strong hexagonal start in C3, but missing automated CI/CD quality gates that block regressions on PR merge   |
| NVIDIA          | Inference economics, KV-cache/context window degradation, NIM/vLLM throughput vs. TTFT tradeoffs, NIM microservices           | Original curriculum spent 66h on training math rather than inference latency, KV-cache limits, and unit cost |
| IBM             | Hybrid cloud governance, regulated industry compliance, explainable audit trails, deterministic policy envelopes              | Provenance hashes (model, prompt, grader, dataset) were missing or back-filled manually across run files     |

### Quadrant Gap Map

```mermaid
quadrantChart
    title Curriculum Topics by U.S. Employer Demand vs Current Coverage
    x-axis Low Current Coverage --> High Current Coverage
    y-axis Low Employer Demand --> High Employer Demand
    quadrant-1 Maintain and Showcase (Strong Fit)
    quadrant-2 Priority Additions (Critical Gaps)
    quadrant-3 Cut or Move to Optional Track
    quadrant-4 Keep Lean and Time-Boxed
    Baseline Evals and Error Analysis: [0.85, 0.92]
    Hexagonal Agent Loop and Escalation Code: [0.78, 0.85]
    Ontology Envelope and Hybrid RAG: [0.62, 0.88]
    MCP Servers and Agent Skills: [0.22, 0.90]
    Managed Cloud Runtime and CI Evals: [0.18, 0.94]
    Full-Stack Agent UI and HITL Approvals: [0.15, 0.84]
    Security Review and Client Handover: [0.20, 0.89]
    Inference Economics and Context Limits: [0.35, 0.76]
    Scratch Backprop and Micrograd: [0.75, 0.15]
    Pretraining Tiny GPT from Scratch: [0.70, 0.12]
```

---

## 3. Recommended Curriculum Changes

### Structural Reallocation of Hours

Remaining curriculum work drops from 110 hours to 90 hours, pulling the completion date forward to late January 2027 at an 8-hour weekly pace. Model training mechanics drop from 66 hours to 11 hours, while automated evaluations, full-stack production engineering, DevSecOps governance, and customer delivery expand from 17 hours to 52 hours.

1. Shift from model building to platform integration and full-stack delivery. Replace scratch neural network construction with deploying C3 onto a managed cloud runtime (Azure AI Foundry or AWS Bedrock AgentCore), exposing domain tools over MCP, and wiring a lightweight TypeScript/React streaming interface for human-in-the-loop (HITL) refund approvals.
2. Elevate AI-assisted software engineering to a first-class workflow. Standardize all repository labs around `AGENTS.md`, reusable Agent Skills, and GitHub Copilot multi-file edit and test-generation workflows to match modern enterprise engineering velocity.
3. Enforce DevSecOps and observability by default. Every evaluation run must emit OpenTelemetry traces and record cryptographic hashes for the prompt, grader, model configuration, and test dataset.
4. Integrate communication and executive readiness. Fold your Impromptu framework (headline-first executive synthesis followed by evidence) directly into Project 6 technical discovery, security sign-off, and client handover deliverables.

### Rule Changes for the Learning System

The stall on Day 10 occurred because high-value engineering happened outside the rigid daily tracker labels. Apply seven operational rules to keep velocity visible and metrics accurate:

1. Give lab depth its own topic type. When an architectural experiment expands (such as C3 policy envelopes), open a dedicated lab topic requiring a merged PR and a 2-minute walkthrough video. Scheduled topics pause cleanly rather than logging false misses.
2. Log one open topic with attempt counters rather than consecutive failure rows. Display "open, attempt 5" on a single line so tracker noise does not distort completion telemetry.
3. Replace the legacy "skip orchestration and cloud deployment" rule. Re-evaluate platform abstractions once per quarter because managed agent harnesses, MCP gateways, and cloud eval services materially changed the deployment baseline in 2026.
4. Authorize one capped cloud budget per project starting in Project 3. Local Ollama models remain the default for rapid iteration, while a strict spending cap (estimated prior to execution) funds managed runtime, commercial frontier model, and cloud evaluation benchmarks.
5. Enforce automated provenance logging at runtime. Three of your seven historical run files required manual back-filling, and none captured the grader version. Every execution script must automatically write `model_id`, `prompt_sha`, `grader_sha`, and `dataset_sha` into run metadata.
6. Schedule a 30-minute market radar check at each project boundary. Review release notes from Microsoft Foundry, AWS Bedrock, Google Cloud, OpenAI, and Anthropic to keep architectural choices current (next checkpoint: post-Ignite on 17 November).
7. Reconcile repository topic counts. Synchronize the progress README (currently listing 59 topics) with `learning_path.json` and `build_curriculum.py`.

---

## 4. New Modules and Topics

### Module A: Automated Evaluation Pipelines and Observability (Added to Project 3)

* Judge calibration mathematics: confusion matrices, Cohen's kappa, alignment against human gold labels, and bias correction for position/verbosity.
* Paired statistical comparisons: bootstrap confidence intervals and McNemar's test across model and architecture revisions (relocated from old Day 63).
* Adversarial and multi-turn simulation: synthetic customer personas that probe edge cases, multilingual/Hinglish switching, and mid-conversation goal shifts.
* Chaos engineering for tool use: injecting HTTP 429/503 faults, malformed JSON payloads, and high-latency responses into Acme backend tools.
* OpenTelemetry trace grading: instrumenting agent steps with OpenTelemetry GenAI semantic conventions and grading intermediate tool selection, not only final prose.
* Continuous Integration quality gates: enforcing regression thresholds in GitHub Actions with `pytest-bdd` so pull requests fail automatically when safety or accuracy drops.
* Production drift monitoring: replaying shadow traffic and configuring automated alerts when intent distributions or rubric scores shift.

### Module B: Production Agent Architecture, MCP, and Full-Stack HITL (Added to Project 4)

* Model Context Protocol (MCP) server engineering: wrapping Acme order, policy, and refund APIs in a standardized MCP server with strict JSON Schema validation and idempotency keys.
* Portable Agent Skills and `AGENTS.md`: packaging the evaluation grader and repository conventions into reusable skills compliant with Agentic AI Foundation specifications.
* Managed cloud runtime migration: deploying C3 onto Azure AI Foundry Agent Service (or AWS Bedrock AgentCore) and running parity benchmarks against the hand-built hexagonal loop.
* Full-stack streaming UI and Human-in-the-Loop (HITL) control: building a concise TypeScript/React (Next.js) operator console that renders real-time agent tool calls, trace citations, and an approval queue for high-value `issue_refund` actions.
* Non-human identity and Policy as Code: assigning scoped managed identities to agents and encoding deterministic refund caps and escalation rules in Cedar or Open Policy Agent (OPA).
* Adversarial security and prompt injection defense: executing indirect prompt injection attacks via poisoned customer tickets and verifying deterministic policy barriers (from old Day 61).

### Module C: Hybrid Semantic Grounding and Inference Economics (Added to Projects 2 and 5)

* Controlled grounding ablation: quantitative benchmark comparing vector retrieval alone, ontology glossary/envelope alone, and hybrid retrieval + ontology across identical regional and edge-case datasets.
* Inference economics and latency engineering: analyzing tokenization overhead across languages (including Hinglish), Time to First Token (TTFT), KV-cache memory scaling, context rot in long prompts, and the ROI decision matrix between prompting, hybrid RAG, and fine-tuning.

### Module D: Enterprise Engagement Lifecycle and DevSecOps Handover (Added to Project 6)

* Structured technical discovery: qualifying high-ROI agent use cases, defining latency/cost/accuracy SLAs, and establishing deterministic fallback boundaries with customer stakeholders.
* Enterprise security review pack: data flow diagrams, PII redaction pipelines, RBAC/identity matrix, prompt injection test reports, and audit log retention schemas.
* Operational handover kit: production runbooks, on-call escalation playbooks, CI evaluation dashboards, and client champion enablement sessions.

---

## 5. Topics to Remove or Deprioritize

| Topic / Legacy Module                                       | Original Hours | Action                  | Justification                                                                                                                              |
|-------------------------------------------------------------|----------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Project 4: Build `micrograd` scalar autograd engine         | 19             | Move to Optional Track  | Zero occurrence in 2026 FDE and Full-Stack AI Application job requirements; tests calculus mechanics rather than production system design. |
| Project 5: Pretrain a character-level Tiny GPT              | 27             | Move to Optional Track  | Pretraining from scratch is confined to foundation model research labs, not forward-deployed, cloud, or full-stack engineering roles.      |
| Project 3: Manual gradient descent and backprop derivations | 20             | Compress to 2h notebook | Condense Days 23 to 26 into a single conceptual notebook focused on what training optimizes and why fine-tuning changes style, not facts.  |
| Unconstrained multi-agent free-form chat loops              | 6              | Replace                 | Replaced by constrained routing (Decisions API pattern), deterministic workflow state machines, and policy-governed tool execution.        |
| Ad-hoc manual JSONL result logging                          | 4              | Replace                 | Replaced by automated runtime provenance hashing (`model`, `prompt`, `grader`, `dataset`) and OpenTelemetry trace spans.                   |

### Conditions That Would Reverse These Cuts

Three specific scenarios would justify restoring parts of old Projects 3 to 5 to the mandatory path:

* Your target interview loop explicitly tests ML internals. If a specific Principal ML Engineer or Research Engineer loop includes whiteboard backpropagation derivations, restore the 19-hour `micrograd` module prior to that interview.
* Your enterprise clients self-host and fine-tune open-weight models on sovereign infrastructure. Regulated defense, banking, or sovereign cloud engagements running custom LoRA/vLLM clusters require deeper coverage of quantization, GPU memory math, and supervised fine-tuning pipelines.
* Content growth on the Build2Understand channel takes priority over immediate 90-day U.S. job market alignment. From-scratch Karpathy-style builds perform strongly on video platforms; treat that as a deliberate content strategy decision separate from hiring readiness.

---

## 6. Hands-on Projects and Capstones

Hours are calculated using the curriculum baseline formula and should be recomputed via `build_curriculum.py` once Project 1 actuals are logged.

| Project | Module Title                                         | Core Topics and Practical Labs (In Order)                                                                                                                                                                                                                                       | Hours | Capstone Deliverable and Measurable Outcome                                                                                            |
|---------|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|----------------------------------------------------------------------------------------------------------------------------------------|
| 1       | Measure before you believe (Finish)                  | Inspect C3 v3 failures · isolate C3 gain by cause across model, grader, and design (Day 10) · write the evidence-backed ADR (Day 11) · author and verify technical article (Day 12)                                                                                             | 7     | Published ADR and article on `rajc.work` with statistically sound attribution table across runs A, B, C, C2, and C3.                   |
| 2       | Grounding: meaning as numbers and enterprise context | Vectors, dot product, and cosine similarity (Days 13-14 merged) · production embeddings · NumPy vector search · `recall@k` · chunking strategies · vector DB vs. NumPy · RAG in Version B · ablation: ontology glossary vs. vector RAG vs. hybrid · article                     | 20    | Benchmark report running B and C3 without oracle context, proving `recall@k` and end-to-end resolution lift from hybrid ontology RAG.  |
| 3       | Evals that run without you                           | Calibrate LLM judge against human labels (confusion matrix, Cohen's kappa) · paired statistical comparisons · simulated multi-turn users · fault injection on broken tools · OpenTelemetry trace grading · `pytest-bdd` CI gate · drift alerts · vendor eval parity             | 19    | Automated GitHub Actions CI pipeline with a calibrated LLM judge (kappa >= 0.80) that fails the build on accuracy or policy regression. |
| 4       | A production-shaped full-stack agent                 | Expose Acme tools as an MCP server · package grader as an Agent Skill · port C3 to Azure AI Foundry or Bedrock AgentCore · React/TypeScript HITL approval UI for `issue_refund` · agent identity and Cedar policy as code · prompt injection red-team · capped frontier run     | 20    | Cloud-deployed agent with MCP tools, streaming React operator UI, Cedar policy guardrails, and 100% block rate on seeded injections.   |
| 5       | Inside the model: mechanics that change decisions    | Tokenization economics and multilingual/Hinglish cost (Day 48) · softmax, temperature, and consistency data (Days 46, 57) · attention scaling and long-context degradation (Day 51) · hallucination mechanisms (Day 55) · 1-notebook training overview · RAG vs. FT vs. prompt | 11    | Six executive architecture diagrams and a quantitative cost/latency calculator guiding customer build-vs-tune-vs-retrieve decisions.   |
| 6       | The 6-week enterprise engagement rehearsal           | Customer discovery and use-case scoping · threat model and enterprise security review pack · final system ADR (Day 64) · headline-first executive readout (Day 65) · operational handover runbook, SLO dashboard, and owner matrix · recorded live rehearsal                     | 13    | Recorded 45-minute live customer simulation (discovery, security sign-off, exec readout, handover) plus production deployment template. |

---

## 7. Alignment with U.S. Job Market Trends

### Role-to-Curriculum Mapping

| Target U.S. Job Role       | Primary Curriculum Projects | Demonstrated Portfolio Artifacts                                                                                       | Key Technical Stack Validated                                                                       |
|----------------------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Forward-Deployed Engineer  | Projects 1, 2, 4, 6         | 6-week engagement pack, customer discovery rubric, ontology envelope, security review pack, recorded executive readout | Python, TypeScript, MCP, Azure AI Foundry / Bedrock AgentCore, hybrid RAG, executive communication  |
| AI Application Engineer    | Projects 1, 2, 3, 4, 5      | Calibrated LLM-as-a-Judge harness, hybrid ontology + vector RAG pipeline, latency/cost tradeoff model                  | LLM APIs, embeddings, vector databases, prompt engineering, evaluation frameworks, structured output |
| Full-Stack Engineer (AI)   | Projects 3, 4, 6            | Streaming React/TypeScript operator console, asynchronous HITL approval workflow for `issue_refund`, MCP API server     | TypeScript, React/Next.js, Python FastAPI, MCP, REST/SSE streaming, idempotent state management     |
| AI Agent Developer         | Projects 1, 3, 4            | Hexagonal C3 agent vs. managed runtime benchmark, portable Agent Skills, `AGENTS.md`, multi-turn user simulator        | Agentic workflows, MCP, Agent Skills, tool-use fault recovery, deterministic routing                |
| Platform Engineer (AI/ML)  | Projects 3, 4               | OpenTelemetry GenAI trace pipeline, `pytest-bdd` CI/CD regression gates, drift alerting, provenance hash enforcement   | OpenTelemetry, GitHub Actions CI/CD, Docker/containers, observability dashboards, shadow replay     |
| Cloud / DevSecOps Engineer | Projects 4, 6               | Non-human agent identity config, Cedar/OPA policy-as-code engine, prompt injection red-team suite, security review pack | Azure / AWS IAM, Cedar policy language, secret/PII governance, threat modeling, compliance auditing |

### High-ROI Certifications and Credentials (Next 90 Days)

Prioritize credentials that directly validate the architecture built in Projects 3 and 4 without diverting hours into unrelated exam prep:

1. Microsoft Certified: Azure AI Engineer Associate / AB-100 Agentic AI track. Selecting Microsoft Foundry as your managed runtime in Project 4 covers roughly 80% of the hands-on objectives required for Microsoft's 2026 agentic certification path.
2. GitHub Copilot Certification. Validates proficiency in AI-assisted software development, workspace agents, custom instructions, and automated test generation sought by enterprise engineering teams.
3. AWS Certified AI Practitioner or Solutions Architect Associate (Optional alternative). Relevant if your immediate client engagements standardize on Amazon Bedrock AgentCore and Cedar policies.

---

## 8. Phased Implementation Roadmap

### Phase 1: Immediate Two-Week Sprint (Nov 9 to Nov 21, 2026)

Complete Project 1 by Monday 16 November, synchronize after Microsoft Ignite, and launch Project 2. Each work block represents one 80-minute focused morning session, with Sundays reserved for rest.

* [ ] Mon 9 Nov: Ship Day 10 at minimum viable scope before Tuesday's 05:00 deadline. Inspect C3 v3's 11 failures, populate the category-by-version matrix, and report v1 to v3 as the controlled before-and-after comparison.
* [ ] Tue 10 Nov: Re-grade saved runs A, B, C, and C2 with the current grader. Produce the three-way attribution table (model, grader, design) as primary evidence for the Day 11 ADR.
* [ ] Wed 11 Nov: Validate C3 on an uncontaminated evaluation split (either a fresh sample or `cases_regional.jsonl` if untouched during tuning). Automate runtime logging of grader, prompt, model, and dataset SHA hashes across all run metadata.
* [ ] Thu 12 Nov: Complete Day 11 ADR. Document the architectural decision, operating conditions, and rollback triggers using the attribution table.
* [ ] Fri 13 Nov: Draft Day 12 article (first 300 words from memory to test conceptual clarity, followed by strict verification of every metric against run files).
* [ ] Sat 14 Nov: Expand Day 12 article to 800-1,200 words incorporating the attribution chart and ADR recommendation.
* [ ] Mon 16 Nov: Edit and publish the Project 1 article on `rajc.work`. Mark Project 1 complete.
* [ ] Tue 17 Nov: Commit the revised 90-hour plan into `learning_path.json` and regenerate trackers via `build_curriculum.py`. Review the Microsoft Ignite keynote and update the 2026 vendor table.
* [ ] Wed 18 to Thu 19 Nov: Execute Project 2 Topic 1 (vectors, dot product, and cosine similarity merged module).
* [ ] Fri 20 to Sat 21 Nov: Execute Project 2 Topic 2 (production embeddings and dimensionality tradeoffs).

### Phase 2: 90-Day Execution Plan (Nov 2026 to Jan 2027)

| Phase   | Target Window            | Focus Area                                                 | Milestone Exit Criteria                                                                                     |
|---------|--------------------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Phase 1 | Weeks 1-2 (Nov 9-21)     | Close Project 1 and launch Project 2 foundations           | Project 1 article live on `rajc.work`; `learning_path.json` updated; embeddings lab complete.               |
| Phase 2 | Weeks 3-4 (Nov 23-Dec 5) | Complete Project 2 (Hybrid RAG and Ontology Grounding)     | Controlled benchmark published comparing vector RAG, ontology glossary, and hybrid grounding on C3.         |
| Phase 3 | Weeks 5-7 (Dec 7-Dec 26) | Complete Project 3 (Automated Evals, OTel, and CI Gates)   | Calibrated LLM judge (kappa >= 0.80), OpenTelemetry trace grading, and GitHub Actions CI gate active.       |
| Phase 4 | Weeks 8-9 (Dec 28-Jan 9) | Complete Project 4 (Managed Runtime, MCP, HITL UI, Policy) | C3 running on Azure AI Foundry or Bedrock AgentCore with MCP server, React HITL UI, and Cedar policies.     |
| Phase 5 | Week 10 (Jan 11-Jan 16)  | Complete Project 5 (Model Internals for Decision Makers)   | Six customer-ready architecture diagrams and token/latency/cost calculator published.                       |
| Phase 6 | Weeks 11-12 (Jan 18-30)  | Complete Project 6 (6-Week Engagement Rehearsal)           | Recorded live client simulation (discovery, security review, readout, handover) and final capstone article. |

---

## 9. Priority Ranking

### Must Have, Should Have, and Nice to Have Matrix

| Priority Tier | Curriculum Items and Capabilities                                                                                                                                                              | Delivery Window | Hiring Signal Impact                                                                                  |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|-------------------------------------------------------------------------------------------------------|
| Must Have     | Cause-by-cause attribution (Day 10-12) · Hybrid RAG + Ontology benchmark (Proj 2) · Calibrated LLM judge and `pytest-bdd` CI gate (Proj 3) · MCP server + Managed Runtime + Cedar policy (Proj 4) | Weeks 1 to 9    | Directly matches 80%+ of U.S. FDE, AI Application Engineer, and Full-Stack AI screening requirements. |
| Should Have   | React/TypeScript HITL approval UI for `issue_refund` · OpenTelemetry GenAI trace grading · Multi-turn simulated customers · Enterprise security review pack and handover runbook (Proj 6)      | Weeks 6 to 12   | Differentiates Senior/Principal candidates in system design, DevSecOps reviews, and client readiness. |
| Nice to Have  | Long-running procedural memory diagrams · Multi-cloud runtime portability beyond primary cloud · Optional weekend track (`micrograd` and Tiny GPT for video channel content)                   | Post-Jan 2027   | Useful for content creation and specialized research loops, but non-blocking for immediate U.S. roles. |

### Architectural Risk Mitigation

Two structural risks apply regardless of cloud vendor selection:

* Rapid API churn across cloud providers. AWS deprecated original Bedrock Agents for new customers in 2026, and Google consolidated Vertex AI components into the Gemini Enterprise Agent Platform. Mitigate churn by keeping C3 domain logic strictly behind hexagonal ports and adapters, learning one primary managed runtime deeply (such as Microsoft Foundry), and mapping competing clouds by architectural primitive.
* Recruiter and vendor bias in job-market aggregates. Treat headline hiring growth percentages as directional indicators rather than exact quotas, and anchor portfolio proof in reproducible code, calibrated evaluations, and live deployment artifacts.

---

## Sources

### Repository Baseline (Inspected 9 November 2026)

* [curriculum.md](https://github.com/rajchampaneriya/fde-impromptu-coach/blob/main/fde-learn/references/curriculum.md)
* [fde-first-principles progress](https://github.com/rajchampaneriya/continuous-learning/tree/main/fde-first-principles) and experiment logs in `data/results`

### 2026 Vendor Announcements

* AWS: [AgentCore managed harness GA][aws-harness] · [AgentCore Evaluations and Policy][aws-evals] · [AgentCore knowledge layers][aws-knowledge] · [Bedrock Agents Classic transition](https://builder.aws.com/content/3ItUUFljIPOutbUGruzDO3RX7Gw/amazon-bedrock-agentcore)
* Microsoft: [Foundry at Build 2026][ms-foundry] · [Build 2026 analysis, Microsoft IQ][ms-iq] · [Fabric IQ status][fabric-iq] · [Ignite 2025 Book of News, Agent 365][ms-agent365] · [Ignite 2026 dates](https://www.moscone.com/node/852)
* Google: [Gemini Enterprise Agent Platform][gcp-agent] · [Agent Evaluations GA][gcp-evals] · [Gemini agent for work][gcp-work]
* OpenAI: [DevDay 2026 for developers][oai-devday]
* Anthropic: [Claude Managed Agents update][ant-managed] · [Agent Skills donated to the Agentic AI Foundation][aaif-skills] · [Claude Frontier Academy][ant-academy]

### U.S. Market and FDE Hiring Signals

* [AWS, OpenAI, and Anthropic FDE programs compared][stateofai-fde]
* [AWS FDE engagement model][pulse2-aws]
* [FDE job postings growth, Indeed via LeadDev][leaddev-fde]
* [2026 FDE hiring trends across ~1,000 job posts](https://getperspective.ai/blog/2026-fde-hiring-trends-what-1000-job-posts-reveal)

[aws-harness]: https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-harness-generally-available
[ms-foundry]: https://devblogs.microsoft.com/foundry/agent-service-build2026/
[gcp-agent]: https://siliconangle.com/2026/04/22/google-brings-agentic-development-optimization-governance-one-roof-gemini-enterprise-agent-platform/
[oai-devday]: https://infoq.com/news/2026/10/openai-devday-2026
[ant-managed]: https://claude.com/resources/articles/new-in-claude-managed-agents
[aws-evals]: https://aws.amazon.com/fr/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/
[gcp-evals]: https://developers.googleblog.com/en/agent-and-model-evaluations-in-gemini-enterprise-agent-platform-are-now-ga/
[ms-iq]: https://futurumgroup.com/?p=90820
[fabric-iq]: https://atlan.com/know/microsoft-fabric/what-is-fabric-iq/
[aws-knowledge]: https://awsinsider.net/articles/2026/06/25/amazon-bedrock-agentcore-adds-three-new-layers-of-agent-knowledge.aspx
[gcp-work]: https://siliconangle.com/google-cloud-introduces-gemini-agent-to-change-enterprise-work
[aaif-skills]: https://www.i-scoop.eu/agent-skills-agentic-ai-foundation/
[ms-agent365]: https://news.microsoft.com/ignite-2025-book-of-news/
[leaddev-fde]: https://leaddev.com/hiring/the-rise-of-the-forward-deployed-engineer
[stateofai-fde]: https://www.thestateofai.com/news/amazon-bets-one-billion-on-forward-deployed-engineers
[pulse2-aws]: https://pulse2.com/amazon-aws-invests-1-billion-to-embed-ai-forward-deployed-engineers-with-customers/
[ant-academy]: https://anthropic.com/news/claude-frontier-academy

