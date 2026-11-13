import base64, io, json, math, unittest
import numpy as np
from lab.core import astar, clean
from lab import tutor

class CoreTests(unittest.TestCase):

    def test_astar_routes_around_wall(self):
        path = astar([0, 0], [4, 4], [[2, y] for y in range(4)], 5)
        self.assertEqual(path[-1], [4, 4])
        self.assertTrue(all((p[0] != 2 or p[1] == 4 for p in path)))

    def test_astar_impossible(self):
        self.assertEqual(astar([0, 0], [2, 2], [[1, y] for y in range(3)], 3), [])

    def test_json_serialization(self):
        self.assertEqual(clean({'a': np.int64(2), 'b': float('nan')}), {'a': 2, 'b': None})

class TutorTests(unittest.TestCase):

    def test_answer_private(self):
        self.assertNotIn('expected', tutor.Engine().snapshot()['question'])

    def test_correct_posterior(self):
        e = tutor.Engine()
        q = e.state['question']
        before = e.state['mastery'][q['concept']]
        e.answer({'answer': q['expected']})
        self.assertGreater(e.state['mastery'][q['concept']], before)

    def test_invalid_row_does_not_mutate(self):
        e = tutor.Engine()
        old = json.dumps(e.state['matrix'])
        r = e.row_check({'row': '0,0,0', 'factor': -2, 'target': 1, 'source': 0})
        self.assertFalse(r['correct'])
        self.assertEqual(json.dumps(e.state['matrix']), old)

    def test_double_submission_rejected(self):
        e = tutor.Engine()
        e.answer({'answer': e.state['question']['expected']})
        with self.assertRaises(ValueError):
            e.answer({'answer': '0'})
