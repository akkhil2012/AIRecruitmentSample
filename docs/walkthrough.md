# OpenRouter workshop walkthrough

1. **0–10 minutes:** Explain the fictional role, source-evidence panel, API key and selected model. Explain that Generate sends this information to OpenRouter and its provider.
2. **10–20 minutes:** Generate the role brief and Boolean sourcing query. Edit the query and download it. Explain that a person runs it on an authorized platform; the app does not search.
3. **20–35 minutes:** Generate the candidate comparison. Check every claim against the JSON. Discuss why listed years do not establish relevant years and missing information means "not listed".
4. **35–45 minutes:** Generate the interview plan and evidence probes. Discuss consistent questions and human assessment.
5. **45–55 minutes:** Generate communication drafts and joining/exit checklists. Verify placeholders and approval responsibilities. Nothing is sent or executed.
6. **55–60 minutes:** Download an edited draft, inspect token usage, and discuss model uncertainty and usage costs.

Each tab calls the LLM only on Generate. There is no numerical scoring engine or static-answer fallback. Missing keys, API errors and unusable responses show errors. Use README setup instructions; never put a real key in committed files.
