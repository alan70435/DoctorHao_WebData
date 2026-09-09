#!/usr/bin/env python3
"""Validate the isolated visual kit using Python standard-library tools only."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
WEBSITE = HERE.parents[1]
PUBLIC = WEBSITE / 'public/visual-kit'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    manifest = json.loads((PUBLIC / 'manifest.json').read_text(encoding='utf-8'))
    entries = manifest['assets']
    files = {str(path.relative_to(PUBLIC)) for path in PUBLIC.rglob('*.svg')}
    require(len(entries) == 33, 'Expected 33 SVG assets')
    require(files == {item['file'] for item in entries}, 'SVG files and manifest differ')
    require(len(files) == len(entries), 'Duplicate manifest path')
    for item in entries:
        path = (PUBLIC / item['file']).resolve()
        require(path.is_relative_to(PUBLIC.resolve()), 'Unsafe asset path')
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == item['sha256'], f'Hash mismatch: {item["file"]}')
        root = ET.fromstring(data)
        require(root.tag.endswith('}svg'), 'Not an SVG root')
        box = [float(n) for n in root.attrib['viewBox'].split()]
        require(box == [0, 0, item['width'], item['height']], f'Incorrect viewBox: {path.name}')
        require(root.find('{http://www.w3.org/2000/svg}title') is not None, 'Missing title')
        require(root.find('{http://www.w3.org/2000/svg}desc') is not None, 'Missing description')
        for node in root.iter():
            name = node.tag.split('}')[-1]
            require(name not in {'script', 'foreignObject', 'image', 'use'}, f'Non-self-contained SVG: {path.name}')
            for key, value in node.attrib.items():
                attr = key.split('}')[-1]
                require(not attr.lower().startswith('on'), 'Event handler in SVG')
                require(attr != 'href', 'External/reference link in SVG')
                require('url(' not in value, 'External/filter resource in SVG')
        require(item['creationMethod'] == 'code-authored-svg' and item['imageModel'] is None,
                'Incorrect SVG provenance')
        require(not item['decorative'] or item['alt'] == '', 'Decorative image must have empty alt')
    spec = json.loads((HERE / 'spec.json').read_text(encoding='utf-8'))
    rows = []
    for filename in spec['articleFiles']:
        rows.extend(json.loads((HERE / filename).read_text(encoding='utf-8')))
    supplemental = json.loads((HERE / spec['supplementalFile']).read_text(encoding='utf-8'))
    slugs = [row[0] for row in rows]
    require(len(rows) == len(set(slugs)) == 52, 'Expected 52 unique article briefs')
    require(len(supplemental) == 13 and len(rows) + len(supplemental) == spec['briefCount'] == 65,
            'Brief count differs')
    counts = {key: sum(row[1] == key for row in rows)
              for key in ('sports-injury', 'weight-management', 'training')}
    require(counts == {'sports-injury': 27, 'weight-management': 13, 'training': 12},
            'Article category counts differ from source inventory')
    require(spec.get('gptImageOutputCount', 0) == 0,
            'Do not claim GPT Image outputs unless GPT Image 2.5 was actually used')
    generated_root = WEBSITE / 'src/assets/generated'
    imagine_count = spec.get('imagineOutputCount', 0)
    if generated_root.exists() and imagine_count:
        live = {p for p in generated_root.rglob('*.webp') if '_hold' not in p.parts}
        hold = {p for p in generated_root.rglob('*.webp') if '_hold' in p.parts}
        require(len(live) == spec.get('liveEnabledCount', 0), 'Live generated WebP count differs from spec')
        require(len(hold) == spec.get('holdCount', 0), 'Hold generated WebP count differs from spec')
        require(len(live) + len(hold) == imagine_count, 'imagineOutputCount does not match files on disk')
    source_dir = WEBSITE / 'src/content/articles'
    parity = 'skipped: source directory not included in isolated kit'
    if source_dir.exists():
        actual = {path.stem for path in source_dir.glob('*.md')}
        require(actual == set(slugs), 'Article source paths and brief coverage differ')
        parity = 'passed: all current article paths covered'
    report = {'svgAssets': len(files), 'svgChecks': 'passed', 'briefCount': 65,
              'articleBriefs': 52, 'articleCategoryCounts': counts, 'articleSourceParity': parity,
              'gptImageOutputs': 0,
              'imagineOutputs': spec.get('imagineOutputCount', 0),
              'liveGeneratedWebp': spec.get('liveEnabledCount', 0),
              'holdGeneratedWebp': spec.get('holdCount', 0),
              'actualGenerationModel': spec.get('actualGenerationModel'),
              'astroProductionBuild': 'not run by this validator'}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
