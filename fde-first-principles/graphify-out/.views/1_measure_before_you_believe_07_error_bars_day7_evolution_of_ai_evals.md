# View of 1-measure-before-you-believe/07-error-bars/day7-evolution-of-ai-evals.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Evolution of AI Evaluations
- [shape title] Evolution of AI Evaluations
- [shape subtitle] Evaluation shifted from “Does it pass?” to “How confident are we, and how do we know?” FDEs think in evidence, not verdicts.
- [shape read-hint] Read left → right, then down
- [shape sec-evolution] HOW EVALUATION EVOLVED
- [shape sec-learned] WHAT WE LEARNED
- [shape sec-conclusion] THE CONCLUSION
- [shape s1-marker] 1
- [shape s1-title] Traditional software testing
- [shape s1-question] “Is it correct?”
- [shape s1-card] Deterministic inputs and outputsPass/fail test casesFunctional correctness
- [shape s2-marker] 2
- [shape s2-title] Early machine learning evaluation
- [shape s2-question] “How accurate is it?”
- [shape s2-card] Accuracy, precision, recall, and F1Fixed test datasetsOffline model comparison
- [shape s3-marker] 3
- [shape s3-title] Foundation model evaluation
- [shape s3-question] “Is it good, safe, and grounded?”
- [shape s3-card] TURNING POINT · Outputs become open-ended
Benchmarks and human preferencePrompt sensitivityQuality, safety, bias, and groundedness
- [shape s4-marker] 4
- [shape s4-title] Statistical evaluation
- [shape s4-question] “How sure are we?”
- [shape s4-card] TURNING POINT · One run is not evidence
Repeated trialsConfidence intervalsVariance and uncertaintySample-size awarenessPairwise and comparative analysis
- [shape s5-marker] 5
- [shape s5-title] System-level evaluation
- [shape s5-question] “Does the whole system work?”
- [shape s5-card] Model, prompt, retrieval, tools, and orchestrationEnd-to-end task successLatency, cost, reliability, and failure modes
- [shape s6-marker] 6
- [shape s6-title] Agentic AI evaluation
- [shape s6-question] “Does the agent finish the job?”
- [shape s6-card] TURNING POINT · The AI acts, not just answers
Multi-step task completionTool-use correctnessPlanning and recoveryState managementHuman intervention and escalation
- [shape s7-marker] 7
- [shape s7-title] Continuous production evaluation
- [shape s7-question] “Is it still working for users?”
- [shape s7-card] Online monitoringReal-user feedbackRegression detectionRed-team testingEvaluation-driven improvement loops
- [shape lesson12] STAGE 1 → 2
A single score hides important variation
- [shape lesson23] STAGE 2 → 3
Evaluation datasets must represent real user tasks
- [shape lesson34] STAGE 3 → 4
Repeated measurements are necessary for probabilistic systems
- [shape lesson45] STAGE 4 → 5
Benchmark performance does not guarantee production success
- [shape lesson56] STAGE 5 → 6
Component evaluation alone cannot validate an entire AI system
- [shape lesson67] STAGE 6 → 7
Evaluation must continue after deployment
- [shape conclusion] Modern AI evaluation is not a one-time test.
It is a continuous decision system that produces evidence about
quality, safety, reliability, and business value.
- [shape lg-title] Legend
- [shape lg-stage-icon] 1
- [shape lg-stage-text] Evolution stage on the timeline
- [shape lg-turn-text] Turning point: the old mental model breaks
- [shape lg-arrow-text] Progression from one stage to the next
- [shape lg-card-text] What each stage measures
- [shape lg-question-icon] “?”
- [shape lg-question-text] The question an FDE asks at that stage
- [shape lg-lesson-text] Lesson learned at a transition
- [shape lg-dashed-text] Links a lesson to the two stages it bridges
- [shape lg-conclusion-text] Conclusion
- [arrow]: "1" -> "2"
- [arrow]: "2" -> "3"
- [arrow]: "3" -> "4"
- [arrow]: "4" -> "5"
- [arrow]: "5" -> "6"
- [arrow]: "6" -> "7"
- [arrow]: "Deterministic inputs and outputsPass/fail test casesFunctional correctness" -> "STAGE 1 → 2
A single score hides important variation"
- [arrow]: "Accuracy, precision, recall, and F1Fixed test datasetsOffline model comparison" -> "STAGE 1 → 2
A single score hides important variation"
- [arrow]: "Accuracy, precision, recall, and F1Fixed test datasetsOffline model comparison" -> "STAGE 2 → 3
Evaluation datasets must represent real user tasks"
- [arrow]: "TURNING POINT · Outputs become open-ended
Benchmarks and human preferencePrompt " -> "STAGE 2 → 3
Evaluation datasets must represent real user tasks"
- [arrow]: "TURNING POINT · Outputs become open-ended
Benchmarks and human preferencePrompt " -> "STAGE 3 → 4
Repeated measurements are necessary for probabilistic systems"
- [arrow]: "TURNING POINT · One run is not evidence
Repeated trialsConfidence intervalsVaria" -> "STAGE 3 → 4
Repeated measurements are necessary for probabilistic systems"
- [arrow]: "TURNING POINT · One run is not evidence
Repeated trialsConfidence intervalsVaria" -> "STAGE 4 → 5
Benchmark performance does not guarantee production success"
- [arrow]: "Model, prompt, retrieval, tools, and orchestrationEnd-to-end task successLatency" -> "STAGE 4 → 5
Benchmark performance does not guarantee production success"
- [arrow]: "Model, prompt, retrieval, tools, and orchestrationEnd-to-end task successLatency" -> "STAGE 5 → 6
Component evaluation alone cannot validate an entire AI system"
- [arrow]: "TURNING POINT · The AI acts, not just answers
Multi-step task completionTool-use" -> "STAGE 5 → 6
Component evaluation alone cannot validate an entire AI system"
- [arrow]: "TURNING POINT · The AI acts, not just answers
Multi-step task completionTool-use" -> "STAGE 6 → 7
Evaluation must continue after deployment"
- [arrow]: "Online monitoringReal-user feedbackRegression detectionRed-team testingEvaluatio" -> "STAGE 6 → 7
Evaluation must continue after deployment"
