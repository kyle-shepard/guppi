# GUPPI

### General-purpose Unified Personal Productivity Intelligence

**A voice-first personal assistant built around memory. Runs on your own hardware, reaches for the cloud only when it earns its place. Built in the open.**

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> 🚧 **Status: Rebuilding from scratch.**
> Formerly *JARVIS*, this project went through three architectures and then sat idle for a few months. Rather than patch the drift, it's being rebuilt from the ground up — and built in public as a working demonstration of **QRSPI**, a disciplined AI-assisted development flow.
> The entire previous codebase is preserved, untouched, on the [`archive/legacy`](../../tree/archive/legacy) branch (tag `v1-archive`). Nothing was lost; `main` is a clean slate.

> **On the name:** GUPPI is a nod to GUPPY, the loyal shipboard AI from Dennis E. Taylor's *Bobiverse* — a capable, unobtrusive aide that runs the ship and remembers everything so its human doesn't have to. That's the job. (The Bobiverse's own term for what happened to this repo over three rewrites, fittingly, is *replicative drift*.)

---

## What GUPPI is

A **voice-first personal assistant** you talk to, that **remembers everything in structured form** — food, medications, workouts, finances, tasks — instead of dumping it into flat chat logs. It coaches, plans, and reminds across every corner of your life, and surfaces connections across those domains without being asked.

The differentiator isn't the conversation — it's the **memory**. What GUPPI *knows* about your life, and what it does with that, is the product.

**Planned modules** (each a focused vertical on a shared memory + agent foundation):

- 🍽️ **Food** — tell it what you ate; multi-step intake resolves the entry, then a background pass enriches it with macros
- 💊 **Medicine** — track doses; proactive reminders to take them
- 🏋️ **Fitness** — a coach that nudges you to train, logs what you did, and charts effort over time
- 💰 **Finance** — expense and bill tracking with analytics
- ✅ **Tasks** — talk through your todos; it holds them and reminds you

The first shippable slice is one thin vertical, spoken to locally at a desk — not all five at once.

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
- [x] Name and frame the rebuild
- [ ] **Q — define the goal and success criteria for the first vertical** ← *here*
- [ ] R — Research
- [ ] S — Spec / Design
- [ ] P — Plan
- [ ] I — Implement

The stack is intentionally **not chosen yet** — that's a design (S) decision, made after the goal is locked, not before. Likely ingredients on the table: Whisper for speech, LiteLLM for model routing, LangSmith for call tracing, n8n for later orchestration.

---

## The old code

Everything from the earlier JARVIS-era codebase (Node/Express backend, React frontend, Rust voice module, self-evolving schema system) lives on [`archive/legacy`](../../tree/archive/legacy). Browse it for reference; `main` starts fresh.

## License

MIT — see [LICENSE](LICENSE).
