"""Evaluate the fictional chapter 15 rules; no UI, API, or database access."""
from pathlib import Path
import copy
import json

def available_amount(records, department):
    selected = [r for r in records
                if r['department'] == department and r['status'] == 'pending']
    return 100 - sum(r['amount'] for r in selected), [r['id'] for r in selected]

def evaluate(category, amount, records, department='D-01'):
    if category not in ('normal', 'special'):
        raise ValueError('Unknown category')
    if type(amount) is not int or not 1 <= amount <= 150:
        raise ValueError('Amount must be an integer from 1 to 150')
    destination = 'C' if category == 'normal' else 'D'
    limit = available_amount(records, department)[0] if destination == 'C' else 50
    return destination, amount > limit

def main():
    records = json.loads((Path(__file__).resolve().parent / 'requests.json').read_text())
    limit, selected = available_amount(records, 'D-01')
    assert selected == ['P-01', 'P-02'] and limit == 70
    cases = [('normal', 70, ('C', False)), ('normal', 71, ('C', True)),
             ('special', 50, ('D', False)), ('special', 51, ('D', True))]
    for category, amount, expected in cases:
        assert evaluate(category, amount, records) == expected
    candidates = [amount for amount in range(1, 151)
                  if evaluate('normal', amount, records) == ('C', True)]
    assert candidates == list(range(71, 151)) and 85 in candidates
    impossible = [amount for amount in range(1, 151)
                  if evaluate('special', amount, records)[0] == 'C']
    assert impossible == []
    changed = copy.deepcopy(records)
    changed[1]['amount'] = 40
    assert available_amount(changed, 'D-01')[0] == 50
    assert evaluate('normal', 51, changed) == ('C', True)
    assert available_amount(records, 'D-01')[0] == 70
    for invalid in (0, 151, '2', True):
        try:
            evaluate('normal', invalid, records)
        except ValueError:
            pass
        else:
            raise AssertionError(f'Invalid amount accepted: {invalid!r}')
    print(json.dumps({'status': 'passed', 'selected_records': selected,
                      'available_amount': limit,
                      'boundary_cases': [{'category': c, 'amount': a,
                                         'destination': e[0], 'business_error': e[1]}
                                        for c, a, e in cases],
                      'C_error_candidates': len(candidates),
                      'special_to_C_candidates': len(impossible),
                      'changed_available_amount': 50,
                      'scope': 'fictional rule calculation only'}, indent=2))

if __name__ == '__main__':
    main()
