"""Streamlit interface: all recruitment drafts are generated through OpenRouter."""
import hashlib
import json
import os

import streamlit as st

from evidence import parse_evidence
from recruiter_demo import CANDIDATES, DEFAULT_MODEL, ROLE, OpenRouterClient, OpenRouterError, generate

st.set_page_config(page_title='Recruiter Copilot · LLM', page_icon='📋', layout='wide')
st.title('Recruiter Copilot · LLM')
st.caption('OpenRouter-powered recruitment workshop • Fictional profiles')
st.info('Generate evidence-based drafts with an LLM. Verify every claim before use. No hiring decisions or outreach are executed.')


def setting(name, default=''):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return default


with st.sidebar:
    st.header('OpenRouter connection')
    api_key = st.text_input('OpenRouter API key', value=setting('OPENROUTER_API_KEY'), type='password')
    model = st.text_input('Model ID', value=setting('OPENROUTER_MODEL', DEFAULT_MODEL))
    st.caption('Use a model ID available to your OpenRouter account. Requests may incur usage charges.')
    st.caption('Generate sends the supplied role, fictional profiles and your instructions to OpenRouter and its model provider.')
    if st.button('Clear generated drafts'):
        for key in list(st.session_state):
            if key.startswith(('result_', 'editor_', 'error_')):
                del st.session_state[key]
    st.caption('Drafts and edits stay in this session. Download to keep them.')

if st.session_state.pop('restore_evidence', False):
    st.session_state['source_role'] = json.dumps(ROLE, indent=2)
    st.session_state['source_candidates'] = json.dumps(CANDIDATES, indent=2)

st.session_state.setdefault('source_role', json.dumps(ROLE, indent=2))
st.session_state.setdefault('source_candidates', json.dumps(CANDIDATES, indent=2))

client = OpenRouterClient(api_key=api_key, model=model)
with st.expander('Source evidence supplied to the LLM', expanded=True):
    st.caption('Edit the role and profiles below. Valid edits are used by every Generate button. '
               'Use fictional or authorized data only; generation sends this evidence to OpenRouter and its provider.')
    st.text_area('Role evidence (JSON)',
                 height=280, key='source_role')
    st.text_area('Candidate profiles (JSON)',
                 height=320, key='source_candidates')
    st.caption('Role needs a title; each candidate needs a unique id. Skills and years are optional: '
               'omit unknown facts instead of guessing. Add project descriptions or other evidence as extra fields. '
               'Use [] for candidates when drafting for a role only. Edits stay in this session.')
    if st.button('Restore fictional sample evidence', key='reset_evidence'):
        # Widget values can be changed before creation on the next run via a callback.
        st.session_state['restore_evidence'] = True
        st.rerun()
    source_role = source_candidates = None
    evidence_error = None
    try:
        source_role, source_candidates = parse_evidence(
            st.session_state['source_role'], st.session_state['source_candidates'])
    except ValueError as exc:
        evidence_error = str(exc)
        st.error(evidence_error)
    if evidence_error is None:
        st.success(f'Ready: {len(source_candidates)} candidate profile(s).')
        with st.expander('Preview evidence sent with the next request'):
            st.json({'role': source_role, 'candidates': source_candidates})
        st.download_button('Download source evidence',
                           json.dumps({'role': source_role, 'candidates': source_candidates}, indent=2),
                           'source_evidence.json', 'application/json', key='download_source')

# Never show drafts produced from a different source as current evidence.
source_revision = hashlib.sha256((st.session_state['source_role'] + '\n' +
                                  st.session_state['source_candidates']).encode()).hexdigest()
if st.session_state.get('source_revision') != source_revision:
    for key in list(st.session_state):
        if key.startswith(('result_', 'editor_', 'error_')):
            del st.session_state[key]
    st.session_state['source_revision'] = source_revision

sections = [
    ('role', 'Role brief'), ('sourcing', 'Sourcing'),
    ('comparison', 'Candidate comparison'), ('interview', 'Interview'),
    ('communication', 'Communication'), ('checklists', 'Joining & exit'),
    ('workshop', 'Workshop guide'),
]
tabs = st.tabs([title for _, title in sections])
for tab, (task, title) in zip(tabs, sections):
    with tab:
        st.header('Boolean sourcing query' if task == 'sourcing' else title)
        st.text_area('Additional instructions', key=f'instructions_{task}',
                     placeholder='Optional: focus on particular skills or adjust the draft.')
        if st.button(f'Generate {title.lower()}', key=f'generate_{task}', disabled=evidence_error is not None):
            # A replacement request must never present an older response as its result.
            for key in (f'result_{task}', f'editor_{task}', f'error_{task}'):
                st.session_state.pop(key, None)
            try:
                with st.spinner('Generating with OpenRouter…'):
                    result = generate(task, client, st.session_state[f'instructions_{task}'],
                                      role=source_role, candidates=source_candidates)
                st.session_state[f'result_{task}'] = result
                st.session_state[f'editor_{task}'] = result['content']
            except OpenRouterError as exc:
                st.session_state[f'error_{task}'] = str(exc)
        if f'error_{task}' in st.session_state:
            st.error(st.session_state[f'error_{task}'])
        result = st.session_state.get(f'result_{task}')
        if result:
            st.caption(f"Generated by {result['model']}. Review the draft below.")
            draft = st.text_area('Edit generated draft', key=f'editor_{task}', height=320)
            st.markdown(draft)
            st.download_button('Download draft', draft, f'{task}_draft.md', 'text/markdown',
                               key=f'download_{task}', disabled=not draft.strip())
            with st.expander('Token usage'):
                st.json(result['usage'])
        else:
            st.caption('Select Generate to request an LLM draft. No rule-based answer is substituted.')
