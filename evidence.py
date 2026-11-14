"""Validate user-supplied source structure, without assessing candidate suitability."""
import json
import math

MAX_EVIDENCE_CHARS = 100_000


def parse_evidence(role_text, candidates_text):
    if len(role_text) + len(candidates_text) > MAX_EVIDENCE_CHARS:
        raise ValueError('Source evidence must be at most 100,000 characters in total.')
    try:
        role = json.loads(role_text)
        candidates = json.loads(candidates_text)
    except (ValueError, RecursionError):
        raise ValueError('Enter valid JSON in both editors. Use double quotes and remove trailing commas.') from None
    if not isinstance(role, dict) or not isinstance(role.get('title'), str) or not role['title'].strip():
        raise ValueError('Role must be a JSON object with a nonempty "title".')
    for name in ('required_skills', 'preferred_skills', 'other_requirements'):
        if name in role and (not isinstance(role[name], list) or
                             any(not isinstance(x, str) or not x.strip() for x in role[name])):
            raise ValueError(f'Role "{name}" must be a list of nonempty strings.')
    if 'minimum_years' in role and not valid_years(role['minimum_years']):
        raise ValueError('Role "minimum_years" must be a finite nonnegative number.')
    if not isinstance(candidates, list):
        raise ValueError('Candidates must be a JSON list; use [] for a role-only task.')
    ids = set()
    for index, candidate in enumerate(candidates, 1):
        if not isinstance(candidate, dict):
            raise ValueError(f'Candidate {index} must be a JSON object.')
        identifier = candidate.get('id')
        if not isinstance(identifier, str) or not identifier.strip() or identifier.strip() in ids:
            raise ValueError(f'Candidate {index} needs a unique, nonempty string "id".')
        ids.add(identifier.strip())
        if 'skills' in candidate and (not isinstance(candidate['skills'], list) or
                                     any(not isinstance(x, str) or not x.strip() for x in candidate['skills'])):
            raise ValueError(f'Candidate {index}: "skills" must be a list of nonempty strings.')
        if 'years' in candidate and not valid_years(candidate['years']):
            raise ValueError(f'Candidate {index}: "years" must be a finite nonnegative number; omit it if unknown.')
    return role, candidates


def valid_years(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0
