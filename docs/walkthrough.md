# 60-minute presenter guide

## Preparation

Install Python 3.10+, clone the repository and run both commands in the README. Open the AI prompts and an approved AI assistant. Keep the templates as offline fallbacks. No package installation or API key is needed for Python. Run commands from the repository root.

## Schedule

| Minutes | Slides | Live demonstration and audience activity |
|---|---|---|
| 0–5 | 1–4 | Ask how many resumes participants review. Explain AI, ML and generative AI. Compare an exact title search with finding Java API experience by meaning. The project does not implement semantic search. |
| 5–12 | 5–7 | Show the role checklist in the Python output. Paste prompt 1. Ask whether AI added an unsupported degree or certification. Approve the checklist together. |
| 12–22 | 8–9 | Show the Boolean query. Explain AND and OR. Ask for alternative titles. Apply Hyderabad separately in an authorized platform; verify supported syntax and REST API evidence. No external search is executed here. |
| 22–35 | 10–14 | Open data/candidates.json. Paste prompt 2 and verify extracted facts. Run baseline and alternative weights. Ask why C overtakes B, and whether that removes the experience follow-up. |
| 35–43 | 15–16 | Paste prompt 3. Compare with templates/interview.md. Ask a volunteer one question, record evidence and apply the rubric. |
| 43–50 | 17–18 | Paste prompt 4. Check placeholders and screening stage. Discuss why skipped SQL means not assessed. Recruiter approval precedes sending. |
| 50–56 | 19–20 | Paste prompt 5. Assign HR, manager and IT owners. Separate planning from authorized execution. |
| 56–60 | 21–22 | Review fairness, privacy, accuracy and human oversight. Ask each participant for one repetitive task they could improve. |

## Live commands

```bash
python recruiter_demo.py
python recruiter_demo.py --weights 55 10 35
```

Walk through the numbered output sections as each agenda topic arrives. The workshop's interview segment demonstrates the 20-minute interview plan; it does not conduct a full interview.

## Closing questions

- Did the assistant invent requirements?
- Did anyone confuse not listed with absent?
- Why did changing weights change the order?
- Who owns selection, rejection, outreach, offers and access changes?

Do not use age, gender, religion, caste, disability or other protected traits for ranking. Use fictional profiles. Weighted checklist coverage is not a validated hiring assessment or performance prediction.

## Troubleshooting

Use python3 or Windows py if python is unavailable. If the AI service is unavailable, use the templates and expected-results document. AI outputs vary; compare them with source facts. No external service is needed for the Python demo.
