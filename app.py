"""Streamlit front end for the fictional recruitment workshop."""
import csv
import io

import streamlit as st

from recruiter_demo import CANDIDATES, PREFERRED, REQUIRED, ROLE, ROOT, screen

st.set_page_config(page_title='Recruiter Copilot', page_icon='📋', layout='wide')
st.title('Recruiter Copilot')
st.caption('A 60-minute recruitment workshop • ABC Technologies • Fictional profiles')
st.info('Explore listed evidence and prepare recruiter drafts. Scores measure checklist coverage, not job performance or hiring eligibility.')

with st.sidebar:
    st.header('Workshop controls')
    preset = st.radio('Scoring scenario', ['Baseline · 70 / 20 / 10', 'Preferred skills · 55 / 10 / 35', 'Custom'])
    if preset == 'Custom':
        weights = [
            st.slider('Required skills (%)', 0, 100, 70),
            st.slider('Experience (%)', 0, 100, 20),
            st.slider('Preferred skills (%)', 0, 100, 10),
        ]
    else:
        weights = [70, 20, 10] if preset.startswith('Baseline') else [55, 10, 35]
    valid_weights = sum(weights) == 100
    st.metric('Weight total', f'{sum(weights)}%')
    if not valid_weights:
        st.error('Weights must total 100%. Adjust the sliders to see scores.')
    st.caption('Required skills / experience / preferred skills')
    st.divider()
    st.markdown('**Human review required**\n\nNot listed means follow up. No messages, offers or access changes are executed.')

brief, sourcing, comparison, interview, communication, checklists, workshop = st.tabs([
    'Role brief', 'Sourcing', 'Candidate comparison', 'Interview',
    'Communication', 'Joining & exit', 'Workshop guide',
])

with brief:
    st.header(ROLE['title'])
    a, b, c = st.columns(3)
    a.metric('Location', ROLE['location'])
    b.metric('Openings', ROLE['openings'])
    c.metric('Relevant experience', f"{ROLE['minimum_years']}+ years")
    left, right = st.columns(2)
    left.subheader('Required skills')
    left.markdown('\n'.join(f'- {s}' for s in ROLE['required_skills']))
    right.subheader('Preferred skills')
    right.markdown('\n'.join(f'- {s}' for s in ROLE['preferred_skills']))
    st.subheader('Also verify')
    st.write(', '.join(ROLE['other_requirements']))
    st.caption('These additional requirements are not included in the numerical checklist score.')

with sourcing:
    st.header('Boolean sourcing query')
    sourcing_query = st.text_area(
        'Edit Boolean sourcing query',
        value='("Java Developer" OR "Backend Engineer" OR "Software Engineer")\nAND ("Spring Boot" OR SpringBoot)\nAND ("REST API" OR Microservices)\nAND (SQL OR PostgreSQL)',
        height=180,
        key='sourcing_query',
        help='Edit the query for your sourcing platform. Changes stay in this session.',
    )
    st.caption('Edits stay in this session. Download the query to keep a copy.')
    if sourcing_query.strip():
        st.code(sourcing_query, language='text')
    st.download_button(
        'Download Boolean query', sourcing_query, 'boolean_sourcing_query.txt',
        'text/plain', disabled=not sourcing_query.strip(),
    )
    st.write('OR broadens a group; AND requires each group. Apply Hyderabad separately and check the search syntax in your authorized platform.')
    st.warning('A microservices mention alone does not establish REST API experience. Verify the evidence.')

with comparison:
    st.header('Compare listed evidence')
    profiles = [{
        'Candidate': candidate, 'Years listed': years,
        'Required listed': ', '.join(sorted(skills & REQUIRED)) or 'Not listed',
        'Preferred listed': ', '.join(sorted(skills & PREFERRED)) or 'Not listed',
    } for candidate, years, skills in CANDIDATES]
    st.dataframe(profiles, hide_index=True, width='stretch')
    if valid_weights:
        results = screen(weights)
        rows = [{'Candidate': c, 'Score / 100': s, 'Review status': status} for c, s, status in results]
        st.subheader('Weighted checklist coverage')
        st.dataframe(rows, hide_index=True, width='stretch')
        st.bar_chart(rows, x='Candidate', y='Score / 100', horizontal=True)
        baseline = {c: s for c, s, _ in screen([70, 20, 10])}
        st.caption('Score change from baseline: ' + ' · '.join(f'{c}: {s - baseline[c]:+d}' for c, s, _ in results))
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['Candidate', 'Score / 100', 'Review status'])
        writer.writeheader()
        writer.writerows(rows)
        st.download_button('Download comparison CSV', output.getvalue(), 'candidate_comparison.csv', 'text/csv')
        with st.expander('How the score works'):
            st.write('Required weight × fraction of required skills listed + experience weight × min(years / minimum years, 1) + preferred weight × fraction of preferred skills listed. The result is rounded.')
            st.write('Listed years are assumed relevant for this workshop calculation and need verification. Changing weights does not remove minimum requirements.')
    else:
        st.warning('Comparison scores are hidden until weights total 100%.')
    selected = st.selectbox('Inspect a fictional candidate', [c for c, _, _ in CANDIDATES])
    candidate, years, skills = next(p for p in CANDIDATES if p[0] == selected)
    st.subheader(f'Follow-up questions for Candidate {candidate}')
    questions = [f'Can you share a concrete example of using {skill}?' for skill in sorted(REQUIRED - skills)]
    if years < ROLE['minimum_years']:
        questions.append(f'{years} years are listed. Can you clarify your total relevant experience against the five-year requirement?')
    questions.append('Describe a production application you worked on and your individual contribution.')
    st.markdown('\n'.join(f'- {q}' for q in questions))

for tab, title, path in [
    (interview, 'Structured interview', 'templates/interview.md'),
    (communication, 'Communication drafts', 'templates/communication.md'),
    (checklists, 'Joining and exit plans', 'templates/checklists.md'),
]:
    with tab:
        st.header(title)
        content = (ROOT / path).read_text()
        st.markdown(content)
        st.download_button('Download workshop template', content, path.split('/')[-1], 'text/markdown', key=path)

with workshop:
    st.header('Facilitator materials')
    st.caption('The app uses rules and templates. Generative AI exercises use an approved assistant separately; no AI API is called here.')
    guide = (ROOT / 'docs/walkthrough.md').read_text()
    st.markdown(guide)
    with st.expander('Copy-and-paste AI activity prompts'):
        st.markdown((ROOT / 'prompts/workshop.md').read_text())
    st.download_button('Download presenter guide', guide, 'walkthrough.md', 'text/markdown')
