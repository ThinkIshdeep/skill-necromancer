from fractions import Fraction
import numpy as np
from .core import Base

class Engine(Base):
    actions = Base.actions | {'answer', 'next', 'row_check', 'hint'}

    def __init__(self):
        super().__init__()
        self.reset({})

    def reset(self, p):
        self.state = {'mastery': {'signs': 0.25, 'scaling': 0.25, 'elimination': 0.15}, 'history': [], 'question': None, 'matrix': [[2, 1, 5], [4, -1, 7]], 'row_history': [], 'feedback': None, 'last_result': None}
        self.next({})

    def next(self, p):
        s = self.state
        concept = min(s['mastery'], key=s['mastery'].get)
        r = np.random.default_rng(42 + len(s['history']))
        a = int(r.integers(2, 9))
        b = int(r.integers(2, 9))
        if concept == 'signs':
            prompt = f'Calculate -{a} - (-{b}).'
            answer = -a + b
            explain = f'Subtracting a negative becomes addition: -{a} + {b}.'
        elif concept == 'scaling':
            prompt = f'Row [1, -{a}, {b}] is multiplied by -2. What is its second entry?'
            answer = 2 * a
            explain = f'Multiply every entry. (-2) × (-{a}) = {2 * a}.'
        else:
            prompt = f'R2 ← R2 - {a}R1. The first entries of R1 and R2 are 1 and {a}. What is the new first entry of R2?'
            answer = 0
            explain = f'{a} - {a} × 1 = 0. This eliminates the first entry.'
        s['question'] = {'id': len(s['history']) + 1, 'concept': concept, 'prompt': prompt, 'expected': str(answer), 'explanation': explain, 'why': f'{concept.title()} has the lowest current mastery estimate.', 'hint_used': False}
        s['feedback'] = None

    def snapshot(self):
        out = super().snapshot()
        if out['question']:
            out['question'].pop('expected', None)
            out['question'].pop('explanation', None)
        return out

    def persist(self):
        return self.state

    def answer(self, p):
        s = self.state
        q = s['question']
        if not q:
            raise ValueError('Choose Next question')
        if q.get('answered'):
            raise ValueError('This question was already answered. Choose Next.')
        try:
            given = Fraction(str(p.get('answer', '')))
            expected = Fraction(q['expected'])
        except (ValueError, ZeroDivisionError):
            raise ValueError('Enter a number or fraction such as -3 or 1/2')
        correct = given == expected
        concept = q['concept']
        prior = s['mastery'][concept]
        slip = 0.12
        guess = 0.18
        if correct:
            posterior = prior * (1 - slip) / (prior * (1 - slip) + (1 - prior) * guess)
        else:
            posterior = prior * slip / (prior * slip + (1 - prior) * (1 - guess))
        learn = 0.08 if q['hint_used'] else 0.15
        s['mastery'][concept] = round(posterior + (1 - posterior) * learn, 4)
        q['answered'] = True
        event = {'question': q['prompt'], 'concept': concept, 'answer': str(given), 'correct': correct, 'prior': prior, 'posterior': s['mastery'][concept], 'hint_used': q['hint_used'], 'due_after_attempts': max(1, int(2 + 8 * s['mastery'][concept]))}
        s['history'].append(event)
        s['feedback'] = {'correct': correct, 'expected': q['expected'], 'explanation': q['explanation'], 'trigger': {'signs': 'Reverse', 'scaling': 'Every', 'elimination': 'Cancel'}[concept]}
        return s['feedback']

    def hint(self, p):
        q = self.state['question']
        q['hint_used'] = True
        return {'hint': q['explanation']}

    def row_check(self, p):
        s = self.state
        target = int(p.get('target', 1))
        source = int(p.get('source', 0))
        if target not in [0, 1] or source not in [0, 1]:
            raise ValueError('Rows are 0 or 1')
        try:
            factor = Fraction(str(p.get('factor', -2)))
            proposed = [Fraction(x.strip()) for x in str(p.get('row', '')).split(',')]
        except (ValueError, ZeroDivisionError):
            raise ValueError('Use three comma-separated numbers, fractions allowed')
        if len(proposed) != 3:
            raise ValueError('Enter three entries')
        if target == source:
            raise ValueError('Choose different source and target rows')
        old = [[Fraction(str(x)) for x in row] for row in s['matrix']]
        expected = [old[target][j] + factor * old[source][j] for j in range(3)]
        ok = expected == proposed
        if ok:
            s['matrix'][target] = [str(x) for x in proposed]
        event = {'operation': f'R{target + 1} ← R{target + 1} + ({factor})R{source + 1}', 'correct': ok, 'expected': [str(x) for x in expected], 'submitted': [str(x) for x in proposed]}
        s['row_history'].append(event)
        return event

    def evaluate(self, p):
        e = Engine()
        concept = e.state['question']['concept']
        prior = e.state['mastery'][concept]
        e.answer({'answer': e.state['question']['expected']})
        r = e.row_check({'target': 1, 'source': 0, 'factor': -2, 'row': '0,-3,-3'})
        out = {'checks': {'correct_answer_raises_posterior': e.state['mastery'][concept] > prior, 'exact_row_check': r['correct'], 'rational_values_preserved': e.state['matrix'][1] == ['0', '-3', '-3']}, 'note': 'Mathematical/BKT regression checks. Synthetic histories do not prove learning gains.'}
        self.state['last_result'] = out
        return out
