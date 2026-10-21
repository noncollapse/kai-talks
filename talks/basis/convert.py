#!/usr/bin/env python3
"""Rebuild the web slides from a local PPTX and a PowerPoint-exported PDF."""

import argparse
import html
import json
import posixpath
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def remove_footer_brand(path):
    """Remove this deck's three-character footer from Poppler's SVG markup."""
    svg = path.read_text()
    removed = []

    def clean_group(match):
        group = ET.fromstring(match[0].replace('xlink:href', 'href'))
        uses = list(group)
        if (
            group.get('fill') == 'rgb(53.726196%, 53.726196%, 53.726196%)'
            and len(uses) == 3
            and all(use.tag == 'use' for use in uses)
        ):
            xs = [float(use.get('x', '0')) for use in uses]
            ys = [float(use.get('y', '0')) for use in uses]
            if (
                20 < xs[0] < 50 and 510 < ys[0] < 540
                and all(abs(y - ys[0]) < 0.01 for y in ys)
                and all(abs(xs[i + 1] - xs[i] - 12) < 0.01 for i in range(2))
            ):
                removed.append([use.get('href')[1:] for use in uses])
                return ''
        return match[0]

    svg = re.sub(r'<g\b[^>]*>\s*(?:<use\b[^>]*/>\s*)+</g>\n?', clean_group, svg)
    if len(removed) > 1:
        raise ValueError(f'Ambiguous footer branding in {path.name}')
    # Drop only glyph definitions that no other visible text uses.
    for glyph in (removed[0] if removed else []):
        if f'xlink:href="#{glyph}"' not in svg:
            svg = re.sub(r'<g id="' + re.escape(glyph) + r'">.*?</g>\n?', '', svg, flags=re.DOTALL)
    ET.fromstring(svg)
    path.write_text(svg)
    return len(removed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path, help='Export all slides from PowerPoint as a PDF first.')
    parser.add_argument('--pptx', required=True, type=Path, help='Local original PPTX; it is not published.')
    parser.add_argument('--pdftocairo', default='pdftocairo')
    parser.add_argument('--pdfinfo', default='pdfinfo')
    args = parser.parse_args()
    titles = json.loads((ROOT / 'slide-titles.json').read_text())
    metadata = json.loads((ROOT / 'talk.json').read_text())

    with ZipFile(args.pptx) as archive:
        presentation = ET.fromstring(archive.read('ppt/presentation.xml'))
        relationships = ET.fromstring(archive.read('ppt/_rels/presentation.xml.rels'))
        targets = {rel.attrib['Id']: rel.attrib['Target'] for rel in relationships}
        sources = []
        for slide in presentation.findall('p:sldIdLst/p:sldId', NS):
            target = targets[slide.attrib[f'{{{NS["r"]}}}id']]
            path = target.lstrip('/') if target.startswith('/') else posixpath.normpath('ppt/' + target)
            sources.append(ET.fromstring(archive.read(path)))
        size = presentation.find('p:sldSz', NS)
        width, height = int(size.attrib['cx']), int(size.attrib['cy'])

    info = subprocess.check_output([args.pdfinfo, str(args.pdf.resolve())], text=True)
    count = re.search(r'^Pages:\s+(\d+)', info, re.MULTILINE)
    if not count or int(count[1]) != len(sources) or len(titles) != len(sources):
        raise SystemExit('The PDF, PPTX and slide-titles.json must contain the same number of slides.')

    blocks = []
    with tempfile.TemporaryDirectory(prefix='basis-slides-') as temporary:
        temporary = Path(temporary)
        for index, (title, source) in enumerate(zip(titles, sources), start=1):
            filename = f'slide-{index:02}.svg'
            subprocess.run([
                args.pdftocairo, '-svg', '-f', str(index), '-l', str(index),
                str(args.pdf.resolve()), str(temporary / filename),
            ], check=True)
            remove_footer_brand(temporary / filename)
            # Check that conversion really produced a complete SVG before replacing assets.
            ET.parse(temporary / filename)
            paragraphs = [
                ''.join(p.itertext()).strip()
                for p in source.findall('.//a:p', NS)
            ]
            paragraphs = [p for p in paragraphs if p and p != '狗熊会']
            body = '\n'.join(f'  <p>{html.escape(p)}</p>' for p in paragraphs)
            frontmatter = f'layout: none\nclass: bg-white\ntitle: {json.dumps(title)}\n'
            if index == 1:
                frontmatter = (
                    'theme: default\nauthor: Kai Ye\nrouterMode: hash\n'
                    'transition: slide-left\ncolorSchema: light\n'
                    'fonts:\n  provider: none\ndrawings:\n  persist: false\n'
                    f'aspectRatio: {width / height}\n'
                    'info: |\n  BASIS research talk, converted from the original PowerPoint.\n'
                    + frontmatter.replace(json.dumps(title), json.dumps(metadata['title']))
                )
            blocks.append(
                f'---\n{frontmatter}---\n\n'
                f'<img src="/slides/{filename}" class="absolute inset-0 w-full h-full object-contain" '
                f'alt="{html.escape(f"Slide {index}: {title}", quote=True)}" />\n\n'
                f'<div class="sr-only">\n  <h1>{html.escape(title)}</h1>\n{body}\n</div>\n'
            )

        destination = ROOT / 'public' / 'slides'
        destination.mkdir(parents=True, exist_ok=True)
        for stale in destination.glob('slide-*.svg'):
            stale.unlink()
        for path in temporary.glob('slide-*.svg'):
            shutil.copy2(path, destination / path.name)
    (ROOT / 'slides.md').write_text('\n'.join(blocks))
    print(f'Converted {len(sources)} slides into {destination}')


if __name__ == '__main__':
    main()
