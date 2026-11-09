# View of 1-measure-before-you-believe/08-agent-loop-from-scratch/agent-loop.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: agent-loop
- [shape email] Customer email + customer_id
{role: 'user'}
- [shape system] Agent Prompt
policy
- [shape model] chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)
- [shape decision] reply has
tool_calls?
- [shape toolrun] your code runs each tool
FUNCTIONS[name](**args)
- [shape append] append {role: 'tool', result}
to messages
- [shape extract] extract_json(reply)
- [shape answer] final answer
{intent, reply, needs_human}
(JSON parse fails → needs_human=True)
- [shape gaveup] MAX_STEPS = 6
{gave_up: True, needs_human: True}
- [shape tools] TOOLS 
lookup_customer · search_kb
get_article · escalate
- [shape trace] trace: every step records
tokens and seconds
- [arrow]: "" -> "Customer email + customer_id
{role: 'user'}"
- [arrow]: "Customer email + customer_id
{role: 'user'}" -> "chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)"
- [arrow]: "Agent Prompt
policy" -> "chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)"
- [arrow]: "chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)" -> "reply has
tool_calls?"
- [arrow] ([tool_calls]): "reply has
tool_calls?" -> "your code runs each tool
FUNCTIONS[name](**args)"
- [arrow]: "your code runs each tool
FUNCTIONS[name](**args)" -> "append {role: 'tool', result}
to messages"
- [arrow] (result goes back): "append {role: 'tool', result}
to messages" -> "chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)"
- [arrow] ([no tool_calls]): "reply has
tool_calls?" -> "extract_json(reply)"
- [arrow]: "extract_json(reply)" -> "final answer
{intent, reply, needs_human}
(JSON parse fails → needs_human=True)"
- [arrow]: "final answer
{intent, reply, needs_human}
(JSON parse fails → needs_human=True)" -> ""
- [arrow]: "MAX_STEPS = 6
{gave_up: True, needs_human: True}" -> "chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)"
- [arrow]: "TOOLS 
lookup_customer · search_kb
get_article · escalate" -> "chat(messages, tools=TOOLS)
the model call (Ollama, temperature=0)"
- [arrow]: "trace: every step records
tokens and seconds" -> "append {role: 'tool', result}
to messages"
