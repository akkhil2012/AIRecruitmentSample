"""Recruitment workshop: offline rules and templates, not a trained AI model."""
import argparse

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROLE = json.loads((ROOT / 'data/role.json').read_text())
REQUIRED = set(ROLE['required_skills'])
PREFERRED = set(ROLE['preferred_skills'])
CANDIDATES = [(p['id'], p['years'], set(p['skills'])) for p in
              json.loads((ROOT / 'data/candidates.json').read_text())]

def screen(weights):
    if len(weights) != 3 or min(weights) < 0 or sum(weights) != 100:
        raise ValueError('Weights must be nonnegative and total 100.')
    rows = []
    for candidate, years, skills in CANDIDATES:
        coverage = (len(skills & REQUIRED) / len(REQUIRED),
                    min(years / ROLE['minimum_years'], 1),
                    len(skills & PREFERRED) / len(PREFERRED))
        score = round(sum(w * v for w, v in zip(weights, coverage)))
        gaps = [f'{skill}: not listed' for skill in sorted(REQUIRED - skills)]
        if years < ROLE['minimum_years']:
            gaps.append(f'verify experience: {years} years listed')
        status = '; '.join(gaps) or 'Meets listed skill and years criteria'
        rows.append((candidate, score, status))
    return sorted(rows, key=lambda row: (-row[1], row[0]))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--weights', nargs=3, type=int, default=[70, 20, 10],
                        metavar=('SKILLS', 'YEARS', 'PREFERRED'))
    args = parser.parse_args()
    if min(args.weights) < 0 or sum(args.weights) != 100:
        parser.error('Weights must be nonnegative and total 100.')

    print('\n1. ROLE CHECKLIST')
    print('ABC Technologies | Senior Java Developer | Hyderabad | 2 openings')
    print('Required: Java, Spring Boot, REST APIs, SQL; 5+ relevant years.')
    print('Preferred: AWS, Docker, Kubernetes.')
    print('Verify production experience, problem-solving and communication separately.')

    print('\n2. SOURCING QUERY')
    print('(\"Java Developer\" OR \"Backend Engineer\" OR \"Software Engineer\")')
    print('AND (\"Spring Boot\" OR SpringBoot)')
    print('AND (\"REST API\" OR Microservices) AND (SQL OR PostgreSQL)')
    print('Apply location separately. Microservices alone does not prove REST API skills.')

    print('\n3. CHECKLIST COVERAGE — HUMAN REVIEW REQUIRED')
    print('Weights:', args.weights)
    for candidate, score, status in screen(args.weights):
        print(f'{candidate} | {score:3}/100 | {status}')
    print('Scores are coverage indicators, not predictions of job performance.')
    print('Not listed means ask for evidence; it does not mean absent.')

    print('\n4. STRUCTURED INTERVIEW — SAME QUESTIONS FOR EVERYONE')
    questions = [
        'Java: How would you investigate a memory leak?',
        'Spring Boot: Explain dependency injection with an example.',
        'Java/Spring: How do you handle API errors consistently?',
        'Scenario: How would you investigate a production API timeout?',
        'Scenario: How would you investigate a slow SQL query?',
        'Collaboration: Describe resolving a technical disagreement.',
    ]
    for i, question in enumerate(questions, 1):
        print(f'{i}. {question}')
    print('Timing: intro 2m, technical 6m, scenarios 6m, collaboration 3m, close 3m.')
    print('Rubric: 1=no relevant evidence; 2=partial; 3=workable approach;')
    print('4=specific example and trade-offs; 5=reasoning, verification and alternatives.')
    print('Skipped competency: not assessed, never automatically zero.')

    print('\n5. COMMUNICATION — DRAFT ONLY')
    print('Hi [Candidate name], please join a 20-minute screening call for our')
    print('Senior Java Developer role in Hyderabad at [time and time zone].')
    print('Meeting: [meeting link]. Please confirm availability. Thanks, [recruiter name].')
    print('Recruiter must review and send. This program sends no messages.')

    print('\n6. ONBOARDING / OFFBOARDING — PLANNING ONLY')
    print('Joining: HR documents; IT access request; manager induction and first-week plan.')
    print('Exit: manager handover; IT asset return and access revocation confirmation.')
    print('Authorized staff approve and execute offers and access changes.')

if __name__ == '__main__':
    main()
