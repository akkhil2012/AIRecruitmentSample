# Recruiter Copilot — OpenRouter LLM edition

`RecuiterDemoLLM` is the LLM-backed edition of `RecuiterDemoFirst`. It retains the seven-tab Streamlit workshop and fictional JSON evidence, replacing weighted scoring and static recruitment answers with real OpenRouter chat-completion requests. The original branch is unchanged.

## Run locally

Python 3.10+:

```bash
git clone --branch RecuiterDemoLLM https://github.com/akkhil2012/AIRecruitmentSample.git
cd AIRecruitmentSample
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
export OPENROUTER_API_KEY='your-openrouter-key'
export OPENROUTER_MODEL='openai/gpt-4o-mini'
# PowerShell: $env:OPENROUTER_API_KEY='your-openrouter-key'
# PowerShell: $env:OPENROUTER_MODEL='openai/gpt-4o-mini'
python -m streamlit run app.py
```

Open http://localhost:8501. Alternatively enter your API key in the password field and your model ID in the sidebar. Streamlit deployment secrets are also supported:

```toml
# .streamlit/secrets.toml (never commit this file)
OPENROUTER_API_KEY = "your-openrouter-key"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
```

Use an available OpenRouter `provider/model` ID with text chat-completion support. Model availability, pricing and provider capabilities depend on your account. The default is configurable, not a guarantee of access. `.env` files are not automatically loaded; export environment variables or use Streamlit secrets.

## What each tab generates

| Tab | LLM output |
|---|---|
| Role brief | Explanation of role criteria and verification needs |
| Sourcing | Boolean search query and explanation, editable after generation |
| Candidate comparison | Listed-evidence table and follow-up questions; no scores or rankings |
| Interview | Structured plan, questions and assessment rubric |
| Communication | Invitation and evidence-summary drafts with unknowns left as placeholders |
| Joining & exit | Planning checklists and approval responsibilities |
| Workshop guide | A novice-friendly 60-minute guide |

Click **Generate** in a tab to make one API request. Responses are editable, previewable and downloadable as Markdown. Session state retains drafts while you use the app; download them before closing the session. Changing connection settings does not regenerate existing drafts; the caption retains the actual response model. Regeneration replaces that tab's draft. Clear generated drafts removes all outputs from the session.

The expanded **Source evidence supplied to the LLM** panel accepts editable role and candidate JSON. Every Generate button uses the current valid input, without changing repository files or restarting. Role needs a nonempty `title`; candidates need unique string `id` values. Optional `skills` are lists of strings and `years` must be finite nonnegative numbers. Omit unknown facts and add project descriptions as extra fields. Use `[]` for role-only tasks. Invalid input disables all Generate buttons. Changing either source clears old generated drafts to prevent stale comparisons. Download the source JSON to keep a copy, or restore the fictional sample with the reset button. Session inputs are not saved to disk. The JSON files in `data/` remain the initial defaults.

## API behavior

`recruiter_demo.py` calls `POST https://openrouter.ai/api/v1/chat/completions` with Bearer authentication, a system instruction, task instructions, source JSON, the selected model, temperature 0.2, a 3,000-token output limit and a 90-second timeout. It returns provider text, model metadata and token usage. There are no automatic retries or rule-based answer fallbacks. Authentication, credits, rate limits, connection errors, empty/invalid responses and truncated output produce actionable errors without exposing keys or raw provider error bodies.

The CLI uses the same client and prompts, with only Python's standard library:

```bash
python recruiter_demo.py --task comparison
python recruiter_demo.py --task sourcing --instructions 'Focus on Agentic AI roles'
python recruiter_demo.py --task interview --model openai/gpt-4o-mini
```

For another role, edit the source-evidence inputs in the app rather than only adding instructions. The CLI continues to use the JSON files in `data/`. Supported tasks: `role`, `sourcing`, `comparison`, `interview`, `communication`, `checklists`, `workshop`. The former `--weights` option and `screen()` scoring function have been removed.

## Evidence and human review

The LLM is instructed to use listed evidence, label missing details **not listed**, keep total years separate from verified relevant years, and avoid inferring location, production experience or communication ability. It must not score, rank, select or reject candidates. These are model instructions, not guarantees: users must verify generated text against the source evidence. Profile text is treated as data, but prompt-injection resistance is not guaranteed.

Generate transmits the role, profiles and additional instructions to OpenRouter and its selected provider and may incur charges. Use the supplied fictional profiles for workshops. Keys are used server-side and are not included in downloads. Do not commit credentials or use sensitive candidate information without appropriate authorization.

The app does not search LinkedIn or other candidate platforms, send messages, make offers or change access. The user manually runs sourcing queries elsewhere. This is an LLM drafting application, not an autonomous sourcing agent.

## Verification

```bash
python -m unittest discover -s tests -v
```

Tests mock the HTTP boundary: they verify request format, all task paths, errors, CLI behavior, UI generation, editing and persistence without paid calls. UI tests require `requirements.txt`; they are skipped if Streamlit is absent. A live smoke test requires your own configured key and credits: run `python recruiter_demo.py --task comparison` and check the returned evidence against the JSON.

Files in `templates/` and `prompts/workshop.md` are inherited workshop reference materials. They are not used as generated answers or as a fallback in this branch.
