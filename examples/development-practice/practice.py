"""Build and check chapter 17's deliberately restricted Markdown table."""
from pathlib import Path
import json
import re
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF
from pyshacl import validate

ROOT = Path(__file__).resolve().parent
EX = Namespace('https://example.org/dev/')
SH = Namespace('http://www.w3.org/ns/shacl#')

def parse_table(text):
    header = '| 要件ID | 要件の名称 | API ID | テストID |'
    lines = text.splitlines()
    if lines.count(header) != 1:
        raise ValueError('Expected exactly one four-column header')
    start = lines.index(header)
    if start + 1 >= len(lines) or lines[start + 1] != '|---|---|---|---|':
        raise ValueError('Unexpected table separator')
    records, seen = [], set()
    for number, line in enumerate(lines[start + 2:], start + 3):
        if not line.strip():
            continue
        if not line.startswith('|') or not line.endswith('|'):
            raise ValueError(f'Unexpected content at line {number}')
        fields = [v.strip() for v in line[1:-1].split('|')]
        if len(fields) != 4:
            raise ValueError(f'Expected four columns at line {number}')
        requirement, label, api, test = fields
        if not label or not all(re.fullmatch(pattern, value) for pattern, value in
                [(r'R-[0-9]{2}', requirement), (r'A-[0-9]{2}', api), (r'T-[0-9]{2}', test)]):
            raise ValueError(f'Invalid value at line {number}')
        if requirement in seen:
            raise ValueError('This source format allows one row per requirement')
        seen.add(requirement)
        records.append((requirement, label, api, test, number, line))
    if not records:
        raise ValueError('No records')
    return records

def build(path, text=None):
    records = parse_table(path.read_text(encoding='utf-8') if text is None else text)
    graph = Graph()
    for requirement, label, api, test, number, line in records:
        r, a, t = EX[requirement], EX[api], EX[test]
        # Example source identifiers map to the local sources/ file and its row.
        source = URIRef(f'https://example.org/practice/{path.stem}#{requirement}')
        for triple in [(r, RDF.type, EX.Requirement), (r, EX.label, Literal(label, lang='ja')),
                       (r, EX.implementedBy, a), (a, RDF.type, EX.API),
                       (t, RDF.type, EX.Test), (t, EX.tests, a), (t, EX.source, source)]:
            graph.add(triple)
    return graph, records

def context_from_query(results, records, source_path, release, requirement):
    if len(results) != 1:
        raise ValueError('This exercise expects one query result')
    api, test, source = results[0]
    expected_source = URIRef(f'https://example.org/practice/{source_path.stem}#{requirement}')
    matches = [r for r in records if r[0] == requirement
               and EX[r[2]] == api and EX[r[3]] == test and source == expected_source]
    if len(matches) != 1:
        raise ValueError('Query result does not identify one matching source row')
    row = matches[0]
    return {'release': release, 'requirement': requirement,
            'api': str(api).removeprefix(str(EX)), 'test': str(test).removeprefix(str(EX)),
            'source': {'file': f'sources/{source_path.name}', 'line': row[4], 'text': row[5]},
            'execution_status': 'not executed'}

def main():
    query = (ROOT / 'related-tests.rq').read_text(encoding='utf-8')
    shapes = Graph().parse(ROOT / 'shapes.ttl', format='turtle')
    v1, records1 = build(ROOT / 'sources/trace-v1.md')
    expected1 = (EX['A-01'], EX['T-01'],
                 URIRef('https://example.org/practice/trace-v1#R-01'))
    assert [tuple(row) for row in v1.query(query)] == [expected1]
    assert len(v1) == 14 and validate(v1, shacl_graph=shapes, inference='none')[0]
    missing = Graph()
    for triple in v1:
        missing.add(triple)
    missing.remove((EX['T-01'], EX.source, None))
    conforms, report, _ = validate(missing, shacl_graph=shapes, inference='none')
    assert not conforms and (None, SH.focusNode, EX['T-01']) in report
    assert (None, SH.sourceConstraintComponent, SH.MinCountConstraintComponent) in report
    source_text = (ROOT / 'sources/trace-v1.md').read_text(encoding='utf-8')
    for malformed in [source_text.replace('A-01 | T-01', 'A-01'),
                      source_text + '| R-01 | 重複 | A-01 | T-04 |\n']:
        try:
            parse_table(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed source accepted')
    v2, records2 = build(ROOT / 'sources/trace-v2.md')
    expected2 = (EX['A-01'], EX['T-03'],
                 URIRef('https://example.org/practice/trace-v2#R-01'))
    results2 = [tuple(row) for row in v2.query(query)]
    assert results2 == [expected2]
    assert validate(v2, shacl_graph=shapes, inference='none')[0]
    assert not list(v2.triples((EX['T-01'], None, None)))
    source_path = ROOT / 'sources/trace-v2.md'
    context = context_from_query(results2, records2, source_path, 'v2', 'R-01')
    assert (context['requirement'], context['api'], context['test']) == ('R-01', 'A-01', 'T-03')
    lines = source_path.read_text(encoding='utf-8').splitlines()
    lines[4], lines[5] = lines[5], lines[4]
    reordered_graph, reordered_records = build(source_path, '\n'.join(lines))
    reordered_context = context_from_query(
        [tuple(row) for row in reordered_graph.query(query)], reordered_records,
        source_path, 'v2', 'R-01')
    assert reordered_context['test'] == 'T-03' and reordered_context['source']['line'] == 6
    assert reordered_context['source']['text'] == context['source']['text']
    output = ROOT / 'output'
    output.mkdir(exist_ok=True)
    (output / 'context-v2.json').write_text(json.dumps(context, ensure_ascii=False, indent=2)
                                          + '\n', encoding='utf-8')
    print(json.dumps({'status': 'passed', 'v1_query': [str(x) for x in expected1],
                      'v2_query': [str(x) for x in expected2],
                      'missing_source_conforms': conforms, 'malformed_sources_rejected': 2,
                      'old_test_removed': True, 'reordered_source_context_matches': True,
                      'context': context}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
