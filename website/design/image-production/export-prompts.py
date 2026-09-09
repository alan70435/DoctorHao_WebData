#!/usr/bin/env python3
"""Export text briefs only. No model, API, credential or network access."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_jobs() -> tuple[dict, list[dict]]:
    spec = json.loads((HERE / 'spec.json').read_text(encoding='utf-8'))
    jobs = []
    for filename in spec['articleFiles']:
        for row in json.loads((HERE / filename).read_text(encoding='utf-8')):
            if len(row) != 5 or not all(isinstance(value, str) for value in row):
                raise ValueError('Invalid article record')
            slug, category, topic, scene, avoid = row
            jobs.append({'id': f'article-{slug}', 'topicLabel': topic, 'scene': scene,
                         'avoid': avoid, 'targetAspectRatio': '16:9',
                         'targetPixels': spec['articleTargetPixels'],
                         'source': spec['articleSourceTemplate'].format(slug=slug)})
    for item in json.loads((HERE / spec['supplementalFile']).read_text(encoding='utf-8')):
        jobs.append({**item, 'source': 'See spec.json sourceDocuments; review the relevant page.'})
    ids = [job['id'] for job in jobs]
    if len(jobs) != spec['briefCount'] or len(set(ids)) != len(ids):
        raise ValueError('Brief count or ID uniqueness check failed')
    if any(not re.fullmatch(r'[a-z0-9-]+', ident) for ident in ids):
        raise ValueError('Unsafe brief ID')
    return spec, jobs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New or empty destination directory')
    args = parser.parse_args()
    spec, jobs = load_jobs()
    destination = args.output.expanduser().resolve()
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        parser.error('Output must be a new or empty directory; existing files will not be overwritten.')
    destination.mkdir(parents=True, exist_ok=True)
    for job in jobs:
        width, height = job['targetPixels']
        text = (
            f"DRAFT BRIEF — NOT A GENERATED IMAGE\n{job['topicLabel']}\n"
            f"Source: {job['source']}\nPreferred model: {spec['preferredModelId']}\n"
            'Read the full source and resolve medical/service blockers before generation.\n\n'
            f"{spec['commonPrompt']}\n\nSCENE: {job['scene']}\n\n"
            f"EXCLUSIONS: {job['avoid']}\n\nLAYOUT: {job['targetAspectRatio']}; "
            f"delivery target {width} x {height}, not a prevalidated API size parameter.\n"
        )
        if job['id'] == 'treatment-bma':
            text = f"BLOCKED PENDING SERVICE CONFIRMATION: {spec['bmaBlocker']}\n\n" + text
        (destination / f"{job['id']}.txt").write_text(text, encoding='utf-8')
    print(f'Exported {len(jobs)} prompt text files. Images generated: 0.')


if __name__ == '__main__':
    main()
