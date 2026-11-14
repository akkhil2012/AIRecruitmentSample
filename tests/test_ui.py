"""UI checks mock only the network boundary; no paid API calls."""
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

HAS_STREAMLIT = importlib.util.find_spec('streamlit') is not None

@unittest.skipUnless(HAS_STREAMLIT, 'Install requirements.txt to run UI tests')
class UITests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest
        self.env = patch.dict('os.environ', {'OPENROUTER_API_KEY': '', 'OPENROUTER_MODEL': 'test/model'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.network = patch('urllib.request.urlopen')
        self.request = self.network.start()
        self.addCleanup(self.network.stop)
        self.app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=20)

    def test_no_api_call_on_initial_render_or_edit(self):
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.tabs), 7)
        self.app.text_area(key='instructions_comparison').set_value('Focus on Java').run()
        self.request.assert_not_called()

    def test_missing_key_has_actionable_error(self):
        self.app.button(key='generate_comparison').click().run()
        self.assertFalse(self.app.exception)
        self.assertIn('OPENROUTER_API_KEY', self.app.error[0].value)
        self.request.assert_not_called()

    def test_generation_edit_persistence_and_error_removes_old_answer(self):
        self.app.text_input[0].set_value('test-key').run()
        self.request.return_value = io.BytesIO(json.dumps({
            'choices': [{'message': {'content': 'LLM generated comparison'}}],
            'model': 'test/model', 'usage': {'total_tokens': 20},
        }).encode())
        self.app.button(key='generate_comparison').click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.request.call_count, 1)
        self.app.text_area(key='editor_comparison').set_value('Edited evidence').run()
        self.assertEqual(self.request.call_count, 1)
        self.assertEqual(self.app.text_area(key='editor_comparison').value, 'Edited evidence')
        from urllib.error import URLError
        self.request.side_effect = URLError('offline')
        self.app.button(key='generate_comparison').click().run()
        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.error)
        self.assertNotIn('editor_comparison', [x.key for x in self.app.text_area])

    def test_dynamic_sources_reach_api_and_changes_clear_drafts(self):
        self.app.text_input[0].set_value('test-key').run()
        self.app.text_area(key='source_role').set_value('{"title":"Agent Engineer"}').run()
        self.app.text_area(key='source_candidates').set_value('[{"id":"Z","project":"Agent tools"}]').run()
        self.request.return_value = io.BytesIO(json.dumps({
            'choices': [{'message': {'content': 'New evidence'}}], 'model': 'test/model'
        }).encode())
        self.app.button(key='generate_comparison').click().run()
        self.assertFalse(self.app.exception)
        body = json.loads(self.request.call_args.args[0].data)
        text = body['messages'][1]['content']
        self.assertIn('Agent Engineer', text)
        self.assertIn('Agent tools', text)
        self.assertNotIn('Senior Java Developer', text)
        self.app.text_area(key='source_candidates').set_value('[]').run()
        self.assertNotIn('editor_comparison', [x.key for x in self.app.text_area])
        self.assertEqual(self.request.call_count, 1)

    def test_invalid_sources_block_generation_and_reset_restores_sample(self):
        self.app.text_area(key='source_role').set_value('invalid').run()
        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.button(key='generate_comparison').disabled)
        self.request.assert_not_called()
        self.app.button(key='reset_evidence').click().run()
        self.assertFalse(self.app.exception)
        self.assertFalse(self.app.button(key='generate_comparison').disabled)
        self.assertEqual(json.loads(self.app.text_area(key='source_role').value)['title'], 'Senior Java Developer')
        self.request.assert_not_called()

if __name__ == '__main__':
    unittest.main()
