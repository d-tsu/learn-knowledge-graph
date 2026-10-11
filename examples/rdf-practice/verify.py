"""Chapter 9: compare syntax, query records, and validate a missing value."""
from pathlib import Path
import json
import importlib.metadata
from rdflib import Graph, Namespace
from rdflib.compare import isomorphic
from pyshacl import validate
from owlrl import DeductiveClosure, OWLRL_Semantics

ROOT = Path(__file__).resolve().parent
EX = Namespace('https://example.org/library/')
data = Graph().parse(ROOT / 'loans.ttl', format='turtle')
other = Graph().parse(ROOT / 'loans.jsonld', format='json-ld')
assert len(data) == 4 and isomorphic(data, other)
query = (ROOT / 'books.rq').read_text(encoding='utf-8')
rows = list(data.query(query))
assert len(rows) == 1
assert rows[0].book == EX.A017
assert str(rows[0].title) == '知識の整理入門' and rows[0].title.language == 'ja'
shapes = Graph().parse(ROOT / 'loan-shapes.ttl', format='turtle')
conforms, _, _ = validate(data, shacl_graph=shapes, inference='none')
assert conforms
missing = Graph()
for triple in data:
    missing.add(triple)
missing.remove((EX.L08, EX.borrower, None))
bad, report, _ = validate(missing, shacl_graph=shapes, inference='none')
SH = Namespace('http://www.w3.org/ns/shacl#')
assert not bad
assert (None, SH.sourceConstraintComponent, SH.MinCountConstraintComponent) in report
assert (None, SH.focusNode, EX.L08) in report
without_title = Graph()
for triple in data:
    without_title.add(triple)
without_title.remove((EX.A017, EX.title, None))
assert not list(without_title.query(query))
assert (EX.L08, EX.book, EX.A017) in without_title
inferred = Graph().parse(ROOT / 'loans.ttl', format='turtle')
inferred.parse(ROOT / 'inverse.ttl', format='turtle')
assert (EX.U03, EX.hasLoan, EX.L08) not in inferred
DeductiveClosure(OWLRL_Semantics).expand(inferred)
assert (EX.U03, EX.hasLoan, EX.L08) in inferred
print(json.dumps({
    'versions': {name: importlib.metadata.version(name) for name in ['rdflib', 'pyshacl', 'owlrl']},
    'equivalent_triples': len(data),
    'query_rows': [[str(value) for value in row] for row in rows],
    'complete_data_conforms': conforms,
    'missing_borrower_conforms': bad,
    'missing_title_query_rows': 0,
    'inverse_relation_derived': True,
    'status': 'passed'
}, ensure_ascii=False, indent=2))
