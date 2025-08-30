# Oedipus: Product, Market, and Business Roadmap

## **Vision**
Oedipus is observability and analytics infrastructure for AI systems. It provides developers and teams with a standardized evaluation layer for LLMs and agent-based systems. By shortening the feedback loop between deployment, evaluation, and iteration, Oedipus makes it easy to compare models, track regressions, and build trustworthy AI products without reinventing the wheel.

Instead of bespoke scripts and ad-hoc dashboards, Oedipus offers a repeatable, rigorous framework for analyzing AI behavior — from raw completions to complex agent traces.  

---

## **Value Proposition**
**For developers:**  
- Replace costly, one-off evaluation pipelines with a standardized, extensible system.  
- Get actionable metrics in minutes: entropy, word count, token usage, correlations, error modes.  
- Plug into CI/CD to detect regressions early.  
- Move faster with confidence in model behavior.  

**For teams:**  
- Collaborate on shared datasets, annotations, and evaluations.  
- Compare models across domains, tasks, and versions.  
- Visualize and debug agent behavior step by step.  
- Export insights to existing workflows (PDF, API, Tableau/BI tools, MLflow, W&B).  

**For the ecosystem:**  
- A common schema for evaluation data and agent traces.  
- Community benchmarks and shared evaluation sets.  
- A plugin marketplace for domain-specific metrics.  

👉 **One-line positioning:**  
**Oedipus is to AI evaluation what PostHog is to product analytics: a developer-first feedback loop that standardizes and accelerates decision-making.**

---

## **Comparison to Existing Tools**
- **Weights & Biases (W&B):** Great for training-time experiment tracking, but not designed for post-deployment LLM/agent evaluation. Oedipus complements W&B by focusing on completions, traces, and human annotations.  
- **Tableau/BI tools:** Flexible for visualization but lack domain-specific metrics, schema support, or agent observability. Oedipus solves the “AI-native” evaluation problem.  
- **Custom scripts/notebooks:** Ubiquitous but costly to maintain, error-prone, and non-standardized. Oedipus replaces them with an opinionated but flexible infra layer.  

---

## **Market**
- **Primary users:** Developers and product teams building AI-powered applications.  
- **Pain point:** Lack of standardized, fast feedback loops for evaluation leads to wasted cycles and unreliable deployments.  
- **Market segments:**  
  1. **Startups** building AI products → need lightweight, affordable infra.  
  2. **Mid-size teams** → need collaboration, benchmarks, integrations with CI/CD.  
  3. **Enterprises** → need compliance-ready auditing, large-scale agent observability.  

---

## **Product Roadmap**

### **Phase 1: MVP (Complete)**
- Bulk dataset upload (CSV) with `input`/`output` schema.  
- Core metrics (entropy, token counts, word counts).  
- Interactive visualizations (Plotly, Streamlit).  
- Export (JSON/CSV).  
- SQLite/Postgres + Celery task processing.  

**Goal:** Validate demand. Users can upload a dataset and see insights in <2 minutes.  

---

### **Phase 2: Rich Data Support + Human Analysis**
- Flexible schema detection (`model`, `version`, `timestamp`, `human_score`, etc.).  
- Human-in-the-loop annotations, tagging, and side-by-side comparisons.  
- Advanced visualizations (distribution, correlations, time-series).  
- Support for JSON/JSONL imports.  

**Goal:** Expand beyond MVP into real-world evaluation workflows.  

---

### **Phase 3: Agent Execution Analysis**
- Ingest agent traces (`step`, `tool_calls`, `observations`, `internal_state`).  
- Replay interface for agent decision paths.  
- Metrics for execution efficiency, tool usage, error recovery.  
- Comparative analysis between agent versions.  

**Goal:** Become the go-to observability tool for multi-step AI agents.  

---

### **Phase 4: Advanced Analytics + Integrations**
- Statistical rigor: significance testing, effect sizes, regression detection.  
- Custom metric plugins and A/B testing support.  
- Export to enterprise workflows (MLflow, W&B, Tableau, CI/CD pipelines).  
- Automated insights (“model improved 23% on safety metrics”).  

**Goal:** Transition from a tool to essential infra for evaluation pipelines.  

---

### **Phase 5: Community & Standards**
- Public evaluation datasets + benchmarks.  
- Model/agent leaderboards.  
- Marketplace for metrics and evaluation protocols.  
- Knowledge base for evaluation best practices.  

**Goal:** Establish Oedipus as the neutral standard for evaluation data formats and community benchmarks.  

---

## **Business Model**
- **Phase 1–2 (Freemium SaaS):**  
  - Free: <1,000 rows, single dataset, basic metrics.  
  - Paid ($29/mo): Unlimited data, advanced visualization.  
- **Phase 3 (Professional tiers):**  
  - Teams ($99/mo): Collaboration, CI/CD integration.  
  - Enterprise ($299+/mo): Compliance features, private deployments.  
- **Phase 4–5 (Platform economics):**  
  - Plugin marketplace for custom metrics.  
  - Benchmark datasets and evaluation services.  
  - Revenue sharing with ecosystem contributors.  

---

## **Success Criteria**
- **Short-term (MVP):** 5+ early adopters uploading data weekly; time-to-insight <2 min.  
- **Mid-term:** Integration into developer CI/CD workflows; repeat usage on multiple datasets.  
- **Long-term:** Community-contributed evaluation sets and benchmarks > internal ones.  
- **Business metrics:** Engagement depth (time per session), volume of data processed, export/API usage, NPS from developers.  

---

## **Strategic Moat**
- **Schema & Standards:** Owning the default schema for evaluation + traces creates lock-in.  
- **CI/CD Integration:** Embedding into dev workflows makes Oedipus infra, not a tool.  
- **Community:** Shared benchmarks and plugins make it costly to switch.  
