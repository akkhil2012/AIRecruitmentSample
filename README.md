# Recruiter Copilot — AI Recruitment Sample

A simple 60-minute workshop based on *AI & Machine Learning for Recruiters*: ABC Technologies is hiring two Senior Java Developers in Hyderabad.

## Quick start

Python 3.10+; no packages or API keys needed.

```bash
git clone https://github.com/akkhil2012/AIRecruitmentSample.git
cd AIRecruitmentSample
python recruiter_demo.py
python recruiter_demo.py --weights 55 10 35
python -m unittest discover -s tests -v
```

Use `python3` or Windows `py` if needed.

## Streamlit interface

Install the UI dependency and launch locally:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501. Use the sidebar to choose baseline, preferred-skills or custom weights. Custom weights must total 100 before scores are displayed.

In the Sourcing tab, edit the Boolean query in the multiline editor, preview it, and download it as a text file. Edits stay in the current session and survive changes to the workshop controls. Download a copy to keep it after the session ends.

Seven tabs cover the role brief, Boolean search, candidate comparison, interview, communication, joining/exit plans and workshop guide. Compare scores, inspect evidence gaps, download a CSV, and open the AI prompts. All profiles are fictional. The UI calls no AI service and requires no API key. The CLI still works without installing Streamlit.

Run all checks after installation with `python -m unittest discover -s tests -v`. Without Streamlit, UI tests are skipped and CLI tests still run.

## What the demo covers

1. Role checklist and Boolean sourcing query.
2. Five fictional profiles and transparent weighted checklist scores.
3. Structured interview questions and a 1–5 rubric.
4. A draft screening invitation and interview-evidence summary.
5. Joining and exit plans with human approval.

The Python component is **rule-based scoring and static templates**, not a trained ML model or an LLM. Use the separate prompts in an approved AI assistant for generative AI activities. Semantic search is discussed, not implemented. No outreach, offers or access changes are executed.

## Workshop materials

- [60-minute presenter guide](docs/walkthrough.md)
- [Generative AI activity prompts](prompts/workshop.md)
- [Expected results and scoring formula](docs/expected-results.md)
- [Interview plan](templates/interview.md)
- [Communications](templates/communication.md)
- [Joining and exit checklist](templates/checklists.md)
- [Fictional candidates](data/candidates.json) and [role](data/role.json)

## Scoring

`--weights` takes required-skills, experience and preferred-skills weights. Defaults: 70/20/10. Values must be nonnegative and total 100. Years coverage is capped at five; four years receive partial coverage. Missing skills receive no coverage points but remain follow-up items.

| Candidate | 70/20/10 | 55/10/35 |
|---|---|---|
| A | 97 | 88 |
| B | 90 | 65 |
| C | 89 | 75 |
| D | 44 | 47 |
| E | 93 | 77 |

## Extend it

Edit the JSON files to explore evidence and scoring. Use nonempty required/preferred skill lists, a positive minimum experience and nonnegative candidate years. The printed brief, query and templates are specific to the Java scenario; update them for another role.

Possible next steps: an approved LLM drafting adapter, embedding-based search, or an authenticated ATS connection. Keep permission checks in application code and require appropriate approvals before writes.

## Responsible use

Scores measure checklist coverage, not job performance or eligibility. Missing information means **not listed**, not absent. Verify whether years are relevant and check production experience, problem-solving, communication and location separately. Exclude protected traits from ranking. Use fictional data in public workshops. Qualified people own selection, rejection, outreach, offers and compliance.

The original presentation is not redistributed in this public repository.
