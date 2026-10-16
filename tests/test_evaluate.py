from src.evaluate import SAMPLES, evaluate

def test_grounded_sample_is_fully_supported_and_cited():
    report = evaluate(SAMPLES['grounded'])
    assert report['groundedness_score'] == 100
    assert report['unsupported_claims'] == []

def test_hallucinated_sample_exposes_unsupported_claims_and_missing_citation():
    report = evaluate(SAMPLES['hallucinated'])
    assert report['groundedness_score'] < 100
    assert len(report['unsupported_claims']) == 2
    assert len(report['missing_citations']) == 1
