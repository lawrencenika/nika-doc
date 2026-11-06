"""Render the GeoEngine docs diagrams to self-contained SVG files, and package the OnlyMap demo.

Run from the repo root:  python3 scripts/geoengine-docs/build_diagrams.py
Writes images/geoengine/<name>-light.svg and <name>-dark.svg. Each file carries its own
styles and CSS animations, so pages embed them with plain <img> tags (server-rendered,
cached across pages, no JavaScript). Edit diagrams.py or the CSS below, then re-run.

It also turns onlymap-demo.html into snippets/geoengine/onlymap-demo.jsx. Mintlify does not
serve .html files in production, so the page embeds the demo as an iframe srcDoc instead.
Edit onlymap-demo.html, then re-run.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrams import FIGURES  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "geoengine")
DEMO_SRC = os.path.join(HERE, "onlymap-demo.html")
DEMO_OUT = os.path.join(HERE, "..", "..", "snippets", "geoengine", "onlymap-demo.jsx")

THEMES = {
    "light": "--panel:#ffffff; --panel2:#f3f0ea; --line:#e0dbd1; --text:#1a121c; --muted:#6b6270; --accent:#4d7c00; --accent-ink:#ffffff; --amber:#b9770e; --s1:#2a78d6; --crit:#d63c3b; --good:#2f8a2f;",
    "dark": "--panel:#1f1422; --panel2:#271a2b; --line:#3a2b3e; --text:#ece6ee; --muted:#a99fae; --accent:#c5ff5a; --accent-ink:#1b2400; --amber:#eba941; --s1:#3987e5; --crit:#e66767; --good:#7fd17f;",
}

FONT = '--font:"Space Grotesk",system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;'

RULES = """.g{fill:color-mix(in srgb,var(--panel2) 55%,transparent);stroke:var(--line);stroke-dasharray:5 4}
.g.outer{fill:none;stroke:var(--muted);stroke-dasharray:none;stroke-width:1.3}
.b{fill:var(--panel2);stroke:var(--line);stroke-width:1.2}
.b.acc{fill:color-mix(in srgb,var(--accent) 22%,var(--panel2));stroke:var(--accent)}
.b.own2{fill:color-mix(in srgb,var(--s1) 20%,var(--panel2));stroke:var(--s1)}
.b.store{fill:color-mix(in srgb,var(--amber) 18%,var(--panel2));stroke:var(--amber)}
.b.wk.restricted{stroke:var(--amber);stroke-width:1.6;stroke-dasharray:5 3}
.b.wk.own{stroke:var(--accent)}
.b.wk.preset{stroke:var(--s1)}
.chip{stroke-width:1.3}
.chip.preset{fill:color-mix(in srgb,var(--s1) 22%,var(--panel2));stroke:var(--s1)}
.chip.own{fill:color-mix(in srgb,var(--accent) 18%,var(--panel2));stroke:var(--accent)}
.chip.restricted{fill:color-mix(in srgb,var(--amber) 20%,var(--panel2));stroke:var(--amber);stroke-dasharray:4 3}
.pod.preset{fill:var(--s1)}.pod.own{fill:var(--accent)}
.pod.restricted{fill:color-mix(in srgb,var(--amber) 35%,var(--panel2));stroke:var(--amber);stroke-width:1.5;stroke-dasharray:3 2}
.lk rect{fill:var(--amber)}.lk path{stroke:var(--amber)}
.lk.ink rect{fill:var(--amber)}.lk.ink path{stroke:var(--amber)}
.role.ok{fill:var(--good)}.role.other{fill:var(--muted)}
.cell.ok{fill:color-mix(in srgb,var(--good) 20%,var(--panel2));stroke:color-mix(in srgb,var(--good) 60%,transparent)}
.cell.no{fill:color-mix(in srgb,var(--crit) 22%,var(--panel2));stroke:var(--crit)}
.t{fill:var(--text);font:13px var(--font)} .tb{font-weight:600;font-size:14px} .ts{fill:var(--muted);font-size:12px} .ts2{fill:var(--text);font-size:12.5px}
.tc{font-size:12px;font-weight:600}
.tg{fill:var(--muted);font-size:11px;letter-spacing:.1em;font-weight:600}
.tn{fill:var(--accent-ink);font-weight:700;font-size:14px}
.tnum{fill:var(--accent);font-weight:700;font-size:13px}
.amb{fill:var(--amber)}
.bad{fill:var(--crit);font-weight:600}.good{fill:var(--good);font-weight:600}
.num{fill:var(--accent)}
.a{fill:none;stroke:var(--muted);stroke-width:1.6}.a.thick{stroke-width:3;stroke:var(--accent)}
.a.dash{stroke-dasharray:5 4}.a.mute{opacity:.6}
.ahead{fill:var(--muted)}.aheadc{fill:var(--accent)}
.a.flow{stroke-dasharray:7 6;animation:flow 1.1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-13}}
.pod.blink{animation:blink 3.2s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}
.anim-steps .step rect{animation:stephi 7s infinite;animation-delay:calc(var(--i) * 1s)}
@keyframes stephi{0%,13%{stroke:var(--accent);stroke-width:2.6}15%,100%{stroke:var(--line);stroke-width:1.2}}
.anim-tasks .task rect{animation:taskp 2.4s ease-in-out infinite;animation-delay:calc(var(--i) * .35s)}
@keyframes taskp{0%,100%{fill:var(--panel2)}50%{fill:color-mix(in srgb,var(--s1) 35%,var(--panel2))}}
.tk{stroke:var(--s1)}
.req,.xmark{opacity:0}
.req-ok{animation:reqok 8s infinite}
.req-no{animation:reqno 8s infinite}
.xmark path{stroke:var(--crit);stroke-width:3.5;stroke-linecap:round;fill:none}
.xmark{animation:xm 8s infinite}
@keyframes reqok{0%{opacity:0;transform:translate(172px,126px)}3%{opacity:1}40%{opacity:1;transform:translate(859px,126px)}46%,100%{opacity:0;transform:translate(859px,126px)}}
@keyframes reqno{0%,48%{opacity:0;transform:translate(172px,192px)}51%{opacity:1;transform:translate(172px,192px)}80%{opacity:1;transform:translate(772px,192px)}83%,100%{opacity:0;transform:translate(772px,192px)}}
@keyframes xm{0%,80%{opacity:0;transform:translate(772px,192px) scale(.4)}84%,95%{opacity:1;transform:translate(772px,192px) scale(1)}100%{opacity:0;transform:translate(772px,192px)}}
.gauge{fill:none;stroke:var(--muted);stroke-width:1.5}.gauge.top{fill:none}
.fillbar{transform-box:fill-box;transform-origin:bottom;animation:fill 6s ease-in infinite}
.fillbar.over{animation-name:fillover}
.fillbar.fit{fill:var(--accent)}
@keyframes fill{0%{transform:scaleY(0)}55%,100%{transform:scaleY(1)}}
@keyframes fillover{0%{transform:scaleY(0);fill:var(--s1)}37%{fill:var(--s1)}40%{fill:var(--crit)}55%,100%{transform:scaleY(1);fill:var(--crit)}}
.pop{opacity:0;animation:pop 6s infinite}
@keyframes pop{0%,55%{opacity:0}60%,100%{opacity:1}}
.lane{stroke:var(--line);stroke-width:1.5}
.dot.serial{fill:var(--muted);animation:serial 7s linear infinite}
.dot.par{fill:var(--accent);animation:par 1.4s linear infinite;animation-delay:var(--d)}
@keyframes serial{from{transform:translateX(0)}to{transform:translateX(280px)}}
@keyframes par{from{transform:translateX(0)}to{transform:translateX(280px)}}
.blk{transform-box:fill-box;transform-origin:center;animation:snap 6s ease-out infinite}
.blk .sblk{animation:snapc 6s infinite}
.blk:nth-of-type(1){--ox:-26px;--r:-5deg}.blk:nth-of-type(2){--ox:22px;--r:4deg}.blk:nth-of-type(3){--ox:-14px;--r:-3deg}.blk:nth-of-type(4){--ox:30px;--r:6deg}.blk:nth-of-type(5){--ox:-20px;--r:-4deg}
.clash{animation:clash 6s infinite}
@keyframes clash{0%,35%{opacity:1}42%,100%{opacity:0}}
@keyframes snap{0%,35%{transform:translateX(var(--ox)) rotate(var(--r))}50%,100%{transform:none}}
@keyframes snapc{0%,35%{stroke:var(--crit)}50%,100%{stroke:var(--accent)}}
.gate{stroke:var(--amber);stroke-width:3;stroke-dasharray:6 4}
.tok{opacity:0}
.tok-ok{animation:tokok 7s infinite}.tok-no{animation:tokno 7s infinite}
@keyframes tokok{0%{opacity:0;transform:translate(20px,85px)}4%{opacity:1}42%{opacity:1;transform:translate(262px,85px)}48%,100%{opacity:0;transform:translate(262px,85px)}}
@keyframes tokno{0%,50%{opacity:0;transform:translate(20px,110px)}53%{opacity:1;transform:translate(20px,110px)}76%{opacity:1;transform:translate(166px,110px)}79%,100%{opacity:0;transform:translate(166px,110px)}}
.xmark2{opacity:0;animation:xm2 7s infinite}.xmark2 path{stroke:var(--crit);stroke-width:3.5;stroke-linecap:round;fill:none}
@keyframes xm2{0%,76%{opacity:0}79%,95%{opacity:1}100%{opacity:0}}
@media (prefers-reduced-motion:reduce){
  *,*:before,*:after{animation:none!important}
  .pop,.xmark2{opacity:1}.req,.tok,.xmark,.clash{opacity:0}
}
"""


def render(svg, theme):
    m = re.match(r'<svg class="([^"]*)" viewBox="0 0 (\d+) (\d+)"', svg)
    cls, w, h = m.group(1), int(m.group(2)), int(m.group(3))
    style = "<style>svg{" + THEMES[theme] + FONT + "}" + RULES + "</style>"
    head_end = svg.index(">") + 1
    svg = svg[:head_end].replace("<svg ", f'<svg width="{w}" height="{h}" ', 1) + style + svg[head_end:]
    if "dg" in cls.split():
        bg = f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" style="fill:var(--panel);stroke:var(--line)"/>'
        svg = svg.replace("</defs>", "</defs>" + bg, 1)
    return svg, w, h


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, build in FIGURES.items():
        raw = build()
        for theme in THEMES:
            svg, w, h = render(raw, theme)
            with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w") as f:
                f.write(svg)
        print(f"{name}: {w}x{h}")
    with open(DEMO_SRC) as f:
        demo = f.read()
    with open(DEMO_OUT, "w") as f:
        f.write("// Generated by scripts/geoengine-docs/build_diagrams.py from onlymap-demo.html. Do not edit by hand.\n")
        # "<\/" keeps a literal </script> in the demo from closing the inline script Mintlify renders
        f.write("export const GE_ONLYMAP_DEMO_HTML = " + json.dumps(demo).replace("</", "<\\/") + ";\n")
    print(f"onlymap demo: {len(demo)} bytes")


if __name__ == "__main__":
    main()
