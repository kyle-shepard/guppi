# PAL — Personal AI Liaison

**A local-first AI assistant — everything runs on your machine. Currently being rebuilt in the open.**

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> 🚧 **Status: Rebuilding from scratch.**
> PAL went through three architectures and then sat idle for a few months. Rather than patch the drift, it's being rebuilt from the ground up — and built in public as a working demonstration of **QRSPI**, a disciplined AI-assisted development flow.
> The entire previous codebase is preserved, untouched, on the [`archive/legacy`](../../tree/archive/legacy) branch (tag `v1-archive`). Nothing was lost; `main` is a clean slate.

---

## What PAL is

A local-first personal assistant that stores what it learns as **structured, queryable memory** instead of flat chat logs. A local LLM, structured event storage, and self-managing context — privacy by architecture, since core functions never leave your machine.

The long-term vision (structured events, cross-domain correlation, proactive pattern surfacing) carried across every iteration and is captured in the archived [V3 README](../../blob/archive/legacy/README.md). This rebuild deliberately **re-derives its requirements from scratch** rather than inheriting them — the exact goal is the first thing being nailed down (see *Where this build is now*).

---

## Why rebuild — and what QRSPI is

The old repo drifted the way projects do: a detailed architecture doc raced ahead of the code, nothing tied the design to actually-shipped slices, and it stalled. QRSPI exists to prevent exactly that. Five steps, each leaving **one artifact a human reads and owns** before moving on:

| Step | Produces | The human owns |
|---|---|---|
| **Q — Question** | an interrogated ticket with explicit success criteria | what "done" means |
| **R — Research** | how the code actually works *today* | that it matches reality |
| **S — Spec / Design** | current state → desired state → decisions | the architecture |
| **P — Plan** | small, shippable vertical slices | the slicing, before any code |
| **I — Implement** | the code / PR | every line |

The principle: **the AI does the volume, the human makes the decisions.** No step is outsourced end-to-end — each produces something a person validates before the next begins. This repo is where that plays out for a real project.

---

## Where this build is now

- [x] Archive the legacy codebase (`archive/legacy`)
- [ ] **Q — define the goal and new requirements** ← *here*
- [ ] R — Research
- [ ] S — Spec / Design
- [ ] P — Plan
- [ ] I — Implement

The stack is intentionally **not chosen yet** — that's a design (S) decision, made after the goal is locked, not before.

---

## The old code

Everything from the JARVIS → V1 → V2 lineage (Node/Express backend, React frontend, Rust voice module, self-evolving schema system) lives on [`archive/legacy`](../../tree/archive/legacy). Browse it for reference; `main` starts fresh.

## License

MIT — see [LICENSE](LICENSE).
