"""Optional UI checks: install requirements.txt to enable these tests."""
import importlib.util
from pathlib import Path
import unittest

HAS_STREAMLIT = importlib.util.find_spec('streamlit') is not None

@unittest.skipUnless(HAS_STREAMLIT, 'Install requirements.txt to run Streamlit UI tests')
class UITests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest
        self.app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=20)

    def test_initial_render_and_baseline(self):
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.tabs), 7)
        self.assertEqual(list(self.app.dataframe[1].value['Score / 100']), [97,93,90,89,44])

    def test_preset_changes_scores(self):
        self.app.radio[0].set_value('Preferred skills · 55 / 10 / 35').run()
        self.assertFalse(self.app.exception)
        self.assertEqual(list(self.app.dataframe[1].value['Candidate']), ['A','E','C','B','D'])
        self.assertEqual(list(self.app.dataframe[1].value['Score / 100']), [88,77,75,65,47])

    def test_custom_invalid_total_hides_scores_then_recovers(self):
        self.app.radio[0].set_value('Custom').run()
        self.app.slider[0].set_value(60).run()
        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.error)
        self.assertEqual(len(self.app.dataframe), 1)
        self.app.slider[2].set_value(20).run()
        self.assertFalse(self.app.exception)
        self.assertFalse(self.app.error)
        self.assertEqual(len(self.app.dataframe), 2)

    def test_candidate_followup(self):
        self.app.selectbox[0].set_value('D').run()
        self.assertFalse(self.app.exception)
        text = '\n'.join(item.value for item in self.app.markdown)
        self.assertIn('using Java?', text)
        self.assertIn('using Spring Boot?', text)

if __name__ == '__main__':
    unittest.main()
