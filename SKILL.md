---
name: vibe-research
description: A cyclic academic workflow for economics research (v4.0). Features a 4-block loop (Framework -> Empirical -> Writing -> Review) to iteratively build rigor and rationality.
source: anthropics/skills
license: Apache-2.0
---

# Vibe Research (Econ Edition v4.0)

An academic research workflow system based on the **"Vibe Loop"** architecture. It helps researchers build rational (Why) and rigorous (How) arguments through iterative cycles.

---

## 🔄 The Vibe Loop Architecture

The workflow consists of **4 recurring blocks** that form a research cycle, managed by a project controller.

### 1. Concept Framework (The Navigator)
- **Command**: `/框架`
- **Output**: `概念框架.md`
- **Function**: Defines the **Rationality** (Research Question, Theoretical Gap, Policy Implication) and **Rigor** (Identification Strategy, Data Match, Logic Blueprint).
- **Agent**: `_系统/概念框架Agent.md`

### 2. Empirical Verification (The Analyst)
- **Command**: `/实证`
- **Output**: `论文章节/实证结果.md` or `研究笔记/意外结果.md`
- **Function**: Interprets regression tables (Stata/Python), checks identification assumptions (Parallel Trends, IV validity), and verifies hypotheses.
- **Agent**: `_系统/实证检验Agent.md`

### 3. Writing Output (The Scribe)
- **Command**: `/写作`
- **Output**: `论文章节/xx-Title.md`
- **Function**: Converts structural blueprints and empirical evidence into academic text. Drafts and polishes content.
- **Agent**: `_系统/学术写作Agent.md`

### 4. Argumentation Review (The Auditor & Strategist)
- **Command**: `/审查`
- **Output**: Literature Search Strategy (Keywords/Journals) & Logic Gap Report
- **Function**: 
    1. **Logic Audit**: Checks for logical leaps.
    2. **Evidence Strategy**: Provides **Search Queries** and **Journal Suggestions** for evidence gathering. **Strict Anti-Hallucination Rule**: AI acts as a navigator, providing maps (keywords), not the terrain (fake papers).
- **Agent**: `_系统/论证审查Agent.md`

---

## 🎮 Command Center

| Command | Action | Description |
|---------|--------|-------------|
| **`/框架`** | **Define** | Build or revise the theoretical lens (Why & How). |
| **`/实证`** | **Verify** | Interpret data results against the framework. |
| **`/写作`** | **Draft** | Write specific sections based on current block. |
| **`/审查`** | **Audit** | Check logic and plan evidence search. |
| **`/主干`** | **Control** | Show progress, return to main task, manage cycles. |
| **`/成稿`** | **Assemble** | Compile all section cards into a full draft. |

---

## 🛠 System Logic

### Cycle Management
- **Prototype Cycle**: Build v0.1 framework -> Initial results -> Rough draft -> Logic check.
- **Refinement Cycle**: Deepen theory -> Robustness checks -> Polished writing -> Evidence sufficiency check.
- **Transition**: Passing the `/审查` (Review) block is the key to entering the next cycle.

### Automations
1. **Auto-Detection**: On defined prompts, AI detects project path and reads `项目信息.md` to identify the current Cycle and Block.
2. **Round Tracking**: 
   - Tracks conversation turns (e.g., "Round 1/4").
   - Automatically triggers Card Generation at end of block (Round 4).
3. **Main Stem Protection**:
   - Detects when conversation drifts to side topics (Knowledge Cards).
   - Prompts user to return to the Main Stem (Output Cards).

---

## 📂 File Structure

```
项目/[Project Name]/
├── 项目信息.md              # Cycle tracker & Task manager
├── 概念框架.md              # The evolving definition of the project
├── 论文章节/                # Output Cards (Draft content)
├── 研究笔记/                # Knowledge Cards (Evidence, Ideas, Side-notes)
├── 实证结果/                # Raw Stata logs/tables
└── 文献/                    # PDF Storage
```

---

## 🚀 Quick Start

1. Create a project folder.
2. Run `/框架` to define your Research Question (Rationality) and Identification Strategy (Rigor).
3. Follow the Vibe Loop: **Frame -> Verify -> Write -> Review -> Repeat**.
