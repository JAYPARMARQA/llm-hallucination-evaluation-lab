import argparse
import json
import re

SOURCES = {
    'refund-policy': 'Refunds are accepted within 30 calendar days of purchase. Approved refunds are returned to the original payment method.',
    'support-hours': 'Support is available Monday through Friday, 09:00 to 17:00 IST.',
}

SAMPLES = {
    'grounded': [
        {'claim': 'Refunds are accepted within 30 calendar days of purchase.', 'citation': 'refund-policy'},
        {'claim': 'Support is available Monday through Friday.', 'citation': 'support-hours'},
    ],
    'hallucinated': [
        {'claim': 'Refunds are accepted within 30 calendar days of purchase.', 'citation': 'refund-policy'},
        {'claim': 'Refunds are processed instantly to any bank account.', 'citation': 'refund-policy'},
        {'claim': 'Support is available 24 hours every day.', 'citation': None},
    ],
}

def normalize(text: str) -> set[str]:
    return set(re.findall(r'[a-z0-9]+', text.lower()))

def supported(claim: str, source: str) -> bool:
    claim_words = normalize(claim)
    source_words = normalize(source)
    return bool(claim_words) and claim_words.issubset(source_words)

def evaluate(items: list[dict]) -> dict:
    rows = []
    for item in items:
        citation = item.get('citation')
        source = SOURCES.get(citation, '')
        is_supported = supported(item['claim'], source)
        cited = citation is not None
        rows.append({**item, 'supported': is_supported, 'cited': cited})
    total = len(rows)
    grounded = sum(row['supported'] and row['cited'] for row in rows)
    return {
        'total_claims': total,
        'grounded_claims': grounded,
        'groundedness_score': round(grounded / total * 100, 1) if total else 0,
        'unsupported_claims': [row['claim'] for row in rows if not row['supported']],
        'missing_citations': [row['claim'] for row in rows if not row['cited']],
        'results': rows,
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', choices=SAMPLES, required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(SAMPLES[args.sample]), indent=2))
