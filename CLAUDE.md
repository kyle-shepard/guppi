# GUPPI

**G**eneral-purpose **U**nified **P**ersonal **P**roductivity **I**ntelligence — a voice-first personal assistant built around structured memory. Formerly *JARVIS*; being **rebuilt from scratch** via the QRSPI flow (see [README](README.md)). Name is a nod to GUPPY from the *Bobiverse*.

## State

- No application code on `main` yet. The build is pre-implementation.
- The legacy JARVIS / V1 / V2 codebase (Node/Express, React, Rust voice, self-evolution) is on branch `archive/legacy` (tag `v1-archive`) — **reference only, do not resurrect its assumptions.**
- **Stack is undecided.** It is an S-step (design) decision, made after the goal is locked. Do not assume the old Node/Tauri stack carries over.

## Working method — QRSPI

Question → Research → Spec/Design → Plan → Implement. The AI does the volume; the human owns every decision. Each step produces one artifact a human validates before the next begins.

- Artifacts live on the **GitHub issue** for each piece of work, not as doc sprawl in the repo.
- Do not scaffold or write application code until a plan is approved.
