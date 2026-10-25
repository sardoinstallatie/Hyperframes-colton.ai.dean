# Maakt build.py voor D01 uit de vaste yapping-template (templates/sardo-yapping/build.py) + d01_parts.py
import re, json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'build_tpl.py')).read()
import importlib.util
spec = importlib.util.spec_from_file_location('p', os.path.join(ROOT, 'd01_parts.py')); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)

def between(text, a, b, new):
    i = text.index(a); j = text.index(b, i)
    return text[:i] + new + text[j:]

src = src.replace("FULL = os.path.join(ROOT, 'work/full.mp4')", "FULL = os.path.join(ROOT, 'media/full-A.mp4')")
src = between(src, 'FIX = {', 'def chunks', P.FIX_CLEAN + '\n')
src = between(src, 'SCENES = [', 'EXTRA_CSS = r', P.SCENES_SVG + '\n')
src = src.replace("        -webkit-text-stroke: 3px var(--caption-stroke); paint-order: stroke fill; opacity: 0; }\n'''",
                  "        -webkit-text-stroke: 3px var(--caption-stroke); paint-order: stroke fill; opacity: 0; }\n" + P.EXTRA_CSS_ADD + "'''", 1)
src = between(src, "SCENE_JS = r'''", "full = FULL", "SCENE_JS = r'''" + P.SCENE_JS + "'''\n\n")
src = src.replace("json.load(open(os.path.join(ROOT, 'work/transcript.json')))", "json.load(open(os.path.join(ROOT, 'media/tr-full-A/transcript.json')))")
src = src.replace("json.load(open(os.path.join(ROOT, 'work/edl.json')))", "(lambda e: e['A'] + e['body'])(json.load(open(os.path.join(ROOT, 'work/edl.json'))))")
src = src.replace("'faceOffsetY': -234", "'faceOffsetY': -161")
src = src.replace("'Klaar voor een <span class=\"hl\">warmtepomp</span>?'", "'Deze fout kostte <span class=\"hl\">€7.000</span>'")
src = src.replace("'word': 'AANBOD'", "'word': 'CHECK'")
src = src.replace("'transform-origin: 540px 768px;'", "'transform-origin: 540px 695px;'")
src = src.replace("';\\n      const SVGS = ' + json.dumps(SVG, ensure_ascii=False) + ';')",
                  "';\\n      const SVGS = ' + json.dumps(SVG, ensure_ascii=False) + ';\\n      const VB = ' + json.dumps(VB) + ';\\n      const XSVG = ' + json.dumps(XSVG) + ';')")
src = src.replace("[st[2] for s in SCENES for st in s.get('steps', [])]", "[it[2] for s in SCENES for it in s.get('items', [])]")
src = src.replace("{'id': 'yap-0093-A', 'name': '2026-10-25-yapping-warmtepomp-test'}", "{'id': 'd01-A', 'name': '2026-10-25-D01-fout-7000-A'}")
for must in ("media/full-A.mp4", "faceOffsetY': -161", "540px 695px", "const VB", "'CHECK'", "it[2] for s in SCENES", "d01-A"):
    assert must in src, must
open(os.path.join(ROOT, 'build.py'), 'w').write(src)
print('build.py klaar')
