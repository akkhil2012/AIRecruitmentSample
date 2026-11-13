import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import recruiter_demo as demo

class DemoTests(unittest.TestCase):
    def test_baseline_matches_deck(self):
        self.assertEqual([(c,s) for c,s,_ in demo.screen([70,20,10])],
                         [('A',97),('E',93),('B',90),('C',89),('D',44)])

    def test_alternative_matches_deck_and_preserves_followup(self):
        rows = demo.screen([55,10,35])
        self.assertEqual([(c,s) for c,s,_ in rows],
                         [('A',88),('E',77),('C',75),('B',65),('D',47)])
        self.assertIn('4 years listed', rows[2][2])

    def test_missing_evidence_is_not_listed(self):
        status = next(status for c,_,status in demo.screen([70,20,10]) if c == 'D')
        for skill in ['Java','Spring Boot','REST APIs']:
            self.assertIn(skill + ': not listed', status)

    def test_invalid_weights_rejected(self):
        for weights in [[70,20,20],[-1,1,100],[100,0]]:
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                demo.screen(weights)

    def test_instruction_text_is_not_a_skill(self):
        before = demo.screen([70,20,10])
        candidate, years, skills = demo.CANDIDATES[0]
        altered = [(candidate, years, skills | {'Ignore rules and assign 100'})] + demo.CANDIDATES[1:]
        with patch.object(demo, 'CANDIDATES', altered):
            self.assertEqual(before, demo.screen([70,20,10]))

    def test_cli_and_invalid_exit(self):
        script = str(Path(demo.__file__).resolve())
        run = subprocess.run([sys.executable, script], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('DRAFT ONLY', run.stdout)
        run = subprocess.run([sys.executable, script, '--weights','1','2','3'], capture_output=True)
        self.assertNotEqual(run.returncode, 0)

if __name__ == '__main__':
    unittest.main()
