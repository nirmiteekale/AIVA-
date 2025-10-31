# AIVA — Product Requirements Document (PRD)

## 1. Problem Statement
Aspiring PMs and early founders struggle to convert raw ideas into structured PRDs and measurable KPIs. They rely on static templates or generic chat tools that lack user context and guidance.

## 2. Objectives (Success Criteria)
- Reduce PRD first-draft time by **≥80%** (from ~6 hours to ≤1 hour).
- Achieve **≥70%** user‑rated relevance of AI‑generated sections.
- Enable **export** to Markdown/Doc and **save** versions per user.

## 3. Target Users & Personas
- **PM Student**: learning PM frameworks, needs structure & examples.
- **Indie Founder**: needs fast validation, KPIs, lightweight GTM.
- **Junior PM**: time‑boxed drafts, consistency across teams.

## 4. Use Cases
1. Enter idea → get PRD outline + editable draft.  
2. Ask “what KPIs should I track?” → Metric Mentor returns 3–5 KPIs.  
3. Generate a quick competitor landscape (top 3 + SWOT bullets).

## 5. Functional Requirements
- AI PRD Generator (Problem, Goals, Personas, KPIs, Risks, Scope out)
- Metric Mentor (metrics by product type and funnel stage)
- Competitor Analyzer (top 3 + problem angle + quick SWOT)
- Save/Load PRDs (basic user context; local for MVP)

## 6. Non‑Functional
- Response in ≤3s for single sections, ≤10s for full PRD.
- Clear error handling if AI API fails.
- Privacy: store locally unless user opts into cloud.

## 7. Assumptions & Constraints
- Internet & valid OpenAI key required.  
- MVP focuses on **single‑user local context** (expand later).

## 8. Open Questions
- Should we add templates per domain (FinTech, EdTech, SaaS)?  
- When to introduce authentication (Firebase) vs local persistence?

## 9. Metrics
- Draft Time Saved, Edit Distance (user changes), CSAT (1–5), Feature usage.

## 10. Scope v1 (MVP)
- PRD generator, KPIs, competitor quick-scan; Streamlit UI; export Markdown.

---

### Meeting Answer Points
- **“MVP narrows scope to PRD + KPIs + competitor scan for speed of value.”**  
- **“Non‑functional goals are response time and graceful failure behavior.”**
