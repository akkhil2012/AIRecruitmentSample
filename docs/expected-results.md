# Expected behavior — LLM edition

There are no fixed candidate scores, expected rankings or deterministic generated answers.

- Opening the app makes no API request.
- Clicking Generate calls OpenRouter once for the selected task.
- Comparison should cover all fictional profiles, label missing information "not listed", separate total years from relevant years, and ask follow-up questions.
- The LLM should not score, rank, select or reject candidates.
- Editing a generated draft or changing tabs makes no new API call.
- Failed generation displays an error, with no static-answer fallback and no stale replacement answer.
- Downloads contain the current edited draft.

Verify every output manually; model instructions cannot guarantee factual accuracy. Automated tests use mocked responses, not live model evaluation. See the README for API setup and a live smoke-test command.
