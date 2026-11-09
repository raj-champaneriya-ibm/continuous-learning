# View of 1-measure-before-you-believe/06-one-llm-call/day6-embedding-compatibility.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Day 6 · Chat model vs embedding model
- [shape t1] Day 6 · Do the chat model and the embedding model need to be compatible?
- [shape t2] No. They never exchange vectors. They meet only through plain text.
- [shape p1t] 1 · How the two models connect
- [shape zvl] EMBEDDING MODEL · works in vectors
- [shape ztl] CHAT MODEL · works in text
- [shape n_email] Customer email
- [shape n_emb1] embeddinggemma
email → vector
- [shape n_kb] 16 help articles
- [shape n_emb2] embeddinggemma
article → vector
- [shape n_search] Similarity search
cosine · top 3
- [shape n_lookup] Look up article
text by ID
- [shape n_note_v] Vectors stay inside this box. The chat model never sees them.
- [shape n_handoff] Plain text
the only handoff
- [shape n_chat] qwen3:4b
reads text only
- [shape n_out] JSON reply
intent · reply · needs_human
- [shape n_note_t] Also in the prompt: system prompt, policy, account card and the email itself.
- [shape p2t] 2 · What must match
- [shape c1] Same embedding model for emails and articles

Vectors from different models, or versions, can't be compared. Mixing them fails silently.

Safe today: the cache is keyed by model. Watch a saved index after changing EMBED_MODEL.
- [shape c2] Same input format on both sides

embeddinggemma expects a short task label before each text. Add it to both sides or neither.

Consistent today: no labels on either side.
- [shape c3] Both models handle Hinglish

Search that misses an article can't be rescued by the chat model, and the reverse also fails.

Check: Hinglish recall@3 in step 2b (14 of 84 emails).
- [shape c4] Fits the chat model's input limit

Retrieved articles are added to the prompt. Ollama's default limit is small and chat() doesn't raise it.

Fits today: policy + all articles ≈ 1,100 words.
- [shape c5] Both fit in memory together

Ollama keeps both models loaded at the same time.

Small risk on an 8 GB Mac; a gate in the step 2b rubric.
- [shape nm] Doesn't need to match: model family, vendor, tokenizer or vector size. qwen3 for chat with Gemma for embeddings is fine.
- [shape p3t] 3 · The real test is end to end
- [shape r1] Version B + fixed articles (INTENT_KB)
- [shape r2] Version B + searched articles (top 3)
- [shape r_gap] Pass-rate gap
= what search costs you
- [shape r_diag] Read the gap with recall@3 from step 2b

Low recall@3 → the embedding model misses articles. Fix search first.
High recall@3 but a big gap → the chat model struggles with searched context. Fix the prompt or the chat model.
- [arrow]: "Customer email" -> "embeddinggemma
email → vector"
- [arrow]: "16 help articles" -> "embeddinggemma
article → vector"
- [arrow]: "embeddinggemma
email → vector" -> "Similarity search
cosine · top 3"
- [arrow]: "embeddinggemma
article → vector" -> "Similarity search
cosine · top 3"
- [arrow]: "Similarity search
cosine · top 3" -> "Look up article
text by ID"
- [arrow]: "Look up article
text by ID" -> "Plain text
the only handoff"
- [arrow]: "Plain text
the only handoff" -> "qwen3:4b
reads text only"
- [arrow]: "qwen3:4b
reads text only" -> "JSON reply
intent · reply · needs_human"
- [arrow]: "Version B + fixed articles (INTENT_KB)" -> "Pass-rate gap
= what search costs you"
- [arrow]: "Version B + searched articles (top 3)" -> "Pass-rate gap
= what search costs you"
- [arrow]: "Pass-rate gap
= what search costs you" -> "Read the gap with recall@3 from step 2b

Low recall@3 → the embedding model miss"
