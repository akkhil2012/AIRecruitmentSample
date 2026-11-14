import json
import unittest
from evidence import parse_evidence

class EvidenceTests(unittest.TestCase):
    def test_unknown_facts_omitted_and_extra_evidence_preserved(self):
        role, candidates = parse_evidence('{"title":"AI Engineer"}', '[{"id":"X","project":"Built an agent"}]')
        self.assertNotIn('years', candidates[0])
        self.assertEqual(candidates[0]['project'], 'Built an agent')
        self.assertEqual(parse_evidence(json.dumps(role), '[]')[1], [])

    def test_invalid_inputs(self):
        for role, candidates in [('{', '[]'), ('[]','[]'), ('{}','[]'),
                                 ('{"title":"AI","minimum_years":true}', '[]'),
                                 ('{"title":"AI"}','{}'),
                                 ('{"title":"AI"}','[{"id":"X"},{"id":"X"}]'),
                                 ('{"title":"AI"}','[{"id":"X","years":NaN}]'),
                                 ('{"title":"AI"}','[{"id":"X","years":-1}]'),
                                 ('{"title":"AI"}','[{"id":"X","skills":"Python"}]'),
                                 ('x'*100001,'[]')]:
            with self.subTest(role=role[:60], candidates=candidates), self.assertRaises(ValueError):
                parse_evidence(role, candidates)
