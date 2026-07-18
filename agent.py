"""GUPPI slice 2, Phase 1: the recall loop — LLM-driven read of structured memory.

A hand-rolled LiteLLM function-calling loop (no framework). The model may call one tool,
`recall_exchanges`, which keyword-searches the slice-1 `exchanges` store; the reply is then
grounded in what it finds. R proved llama3.2 *over*-calls (fabricates tools, re-calls instead
of finishing), so the loop's real job is stopping and guarding, not coaxing:
  - stop after one recall round-trip by dropping `tools=` on the grounding call (D4.1);
  - ignore phantom tool names the model invents (D4.2);
  - pass straight through when the model doesn't call a tool (D4.3).
"""
import json
import sys

import litellm

import store

MODEL = "ollama/llama3.2"  # defined here; app.py imports it (never the reverse — app.py runs Streamlit at import)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "recall_exchanges",
            "description": (
                "Search the user's own past conversations stored in memory. Call this to "
                "answer questions about things the user told you in earlier sessions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords to search past exchanges for, e.g. 'dog name' or 'favorite food'.",
                    }
                },
                "required": ["query"],
            },
        },
    }
]


def recall_exchanges(query):
    """The tool body: keyword recall over the structured store, returned as a JSON string.

    Empty/blank query → no rows (don't let a `%%` LIKE match the whole table). R saw the
    model emit an empty `{"query":""}` on cold calls.
    """
    if not query or not query.strip():
        return json.dumps([])
    return json.dumps(store.search(query))


def reply(messages):
    """Run one recall round-trip and return the final grounded reply string.

    Works on a local copy — the tool-call turn and role:"tool" results must NOT leak into
    the caller's session messages, or they'd render as raw messages in the GUI.
    """
    convo = list(messages)
    resp = litellm.completion(model=MODEL, messages=convo, tools=TOOLS, tool_choice="auto")
    msg = resp.choices[0].message

    # D4.3 — no tool call: the model answered directly, pass it through.
    if not getattr(msg, "tool_calls", None):
        return msg.content

    # Append the assistant tool-call turn once (plain dict — works for real + demo message objects).
    convo.append(
        {
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        }
    )

    # One role:"tool" result per call, each bound to its tool_call_id (required by the format).
    for tc in msg.tool_calls:
        try:
            args = json.loads(tc.function.arguments or "{}")
        except (json.JSONDecodeError, TypeError):
            args = {}
        if tc.function.name == "recall_exchanges":
            query = args.get("query", "")
            print(f"[agent] recall_exchanges(query={query!r})", file=sys.stderr)  # F5: proves the call fired
            result = recall_exchanges(query)
        else:
            # D4.2 — phantom tool the model invented: acknowledge, do NOT dispatch.
            result = f"Tool '{tc.function.name}' is not available."
        convo.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    # D4.1 — stop condition: grounding call with `tools=` OMITTED entirely (not tool_choice="none";
    # R verified dropping tools= is what recovers the grounded reply from this model).
    final = litellm.completion(model=MODEL, messages=convo)
    return final.choices[0].message.content


def demo():
    """Runnable check for the loop's real logic — no live model, no store.

    Scripts a two-response completion (tool_calls: recall + phantom, then grounded text) and
    stubs store.search. Asserts: recall dispatched, phantom NOT dispatched, the grounding call
    omits tools=, grounded text returned.
    """
    from types import SimpleNamespace

    def tc(id_, name, arguments):
        return SimpleNamespace(id=id_, function=SimpleNamespace(name=name, arguments=arguments))

    def resp(content, tool_calls):
        msg = SimpleNamespace(content=content, tool_calls=tool_calls)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

    scripted = iter(
        [
            resp(None, [tc("call_1", "recall_exchanges", '{"query":"dog"}'),
                        tc("call_2", "get_weather", '{"city":"NYC"}')]),
            resp("Your dog's name is Biscuit.", None),
        ]
    )
    calls = []
    dispatched = []

    def fake_completion(**kwargs):
        calls.append(kwargs)
        return next(scripted)

    def fake_search(query, **kw):
        dispatched.append(query)
        return [{"user_message": "my dog's name is Biscuit"}]

    orig_completion, orig_search = litellm.completion, store.search
    litellm.completion, store.search = fake_completion, fake_search
    try:
        out = reply([{"role": "user", "content": "what's my dog's name?"}])
    finally:
        litellm.completion, store.search = orig_completion, orig_search

    assert dispatched == ["dog"], f"recall should dispatch once with 'dog'; phantom must not search: {dispatched}"
    assert len(calls) == 2, f"expected 2 completion calls, got {len(calls)}"
    assert "tools" not in calls[1], "grounding (2nd) call must omit tools="
    assert out == "Your dog's name is Biscuit.", out
    print("agent.demo() OK")


if __name__ == "__main__":
    demo()
