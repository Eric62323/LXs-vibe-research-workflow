---
name: vibe-research
description: A cyclic academic workflow for economics research (v6.0). Features a 4-block loop (Framework -> Empirical -> Writing -> Review) with Phase 0-4 empirical pipeline, multi-role peer review, Worker-Critic adversarial pairing, and integrity gates.
source: anthropics/skills
license: MIT
---

# Vibe Research (Econ Edition v6.0)

An academic research workflow system based on the **4-Block Cycle** architecture. Helps researchers build rigorous empirical analysis through iterative cycles with built-in quality gates.

---

## Core Architecture: 4-Block Cycle

```
/框架 ──→ /实证 ──→ /写作 ──→ /审查
  ↑                                  |
  └──── Review not passed, return to /框架 ──┘
```

### Block 1: Concept Framework (`/框架`)
- Define research question, literature review (3-tier), theory, causal identification (DAGs)
- Socratic coaching with SCR protocol
- Agent: `_系统/概念框架Agent.md`

### Block 2: Empirical Analysis (`/实证`)
- Phase 0-4 pipeline: Data Cleaning → Audit+EDA → Main Regression → Heterogeneity → Robustness
- VERIFY numeric source tracking, Worker-Critic internal review
- Paper-type taxonomy with reviewer expectation checklist
- Quantitative integrity gate (≥80 to pass)
- Agent: `_系统/实证检验Agent.md`

### Block 3: Writing Output (`/写作`)
- 7 writing modes (full, plan, outline-only, revision, revision-coach, abstract-only, lit-review)
- Claim-faithfulness audit with citation fidelity 3-tier annotation
- AI high-frequency word detection
- Agent: `_系统/学术写作Agent.md`

### Block 4: Argumentation Review (`/审查`)
- 5-member review team + Editorial Synthesizer
- 7-dimension scoring (0-100), Devil's Advocate with concession threshold protocol
- "What would change my mind" protocol, frame-lock detection
- Socratic coaching + revision + re-review sub-cycle (max 3 rounds)
- Agent: `_系统/论证审查Agent.md`

---

## Integrity Gates

4 mandatory checkpoints at critical transitions:
- Gate 2.5: Literature completeness
- Gate 4.5: Framework → Empirical readiness
- Empirical Gate: Quantitative score ≥80
- Review Gate: All 7 dimensions ≥75, no score regression

---

## Commands

| Command | Block | Function |
|---------|-------|----------|
| `/框架` | Framework | Research question, literature, theory, identification |
| `/实证` | Empirical | Phase 0-4 pipeline with integrity gate |
| `/写作` | Writing | 7 modes, claim audit, AI word detection |
| `/审查` | Review | 5-person review team, scoring, Socratic coaching |
| `/主干` | Project Mgmt | Progress tracking, cycle management |
| `/成稿` | Assembly | Compile all sections into full draft |

---

## References

- **Academic Research Skills (ARS)** v3.7-3.9.4 by Cheng-I Wu (CC BY-NC 4.0)
- **claude-code-my-workflow** by Pedro H. C. Sant'Anna (MIT License)
- **CLO-Author** by Hugo Sant'Anna (MIT License)
- **Karpathy's AI Coding Principles** by Andrej Karpathy

---

## Quick Start

1. Clone into Claude Code skills directory
2. Create project folder with `项目信息.md`
3. Run `/框架` to define your research question
4. Follow the cycle: **Frame → Empirical → Write → Review → Repeat**
