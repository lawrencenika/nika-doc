"""SVG diagrams and animated infographics for the NIKA GeoEngine (Kubernetes) docs. Rendered to images/geoengine/ by build_diagrams.py."""

from html import escape

NAME = "NIKA GeoEngine"


_uid = [0]


def svg(w, h, body, label, cls="dg"):
    _uid[0] += 1
    u = f"m{_uid[0]}"
    body = body.replace("url(#ahc)", f"url(#{u}c)").replace("url(#ah)", f"url(#{u})")
    return (
        f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" '
        f'xmlns="http://www.w3.org/2000/svg"><defs>'
        f'<marker id="{u}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="ahead"/></marker>'
        f'<marker id="{u}c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="aheadc"/></marker></defs>' + body + "</svg>"
    )


def text(x, y, s, cls="t", anchor="middle"):
    s = s.replace("@@N@@", NAME)
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>'


def box(x, y, w, h, title, sub=None, cls="b", rx=10):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'
    if sub:
        out += text(x + w / 2, y + h / 2 - 3, title, "t tb") + text(x + w / 2, y + h / 2 + 15, sub, "t ts")
    else:
        out += text(x + w / 2, y + h / 2 + 5, title, "t tb")
    return out


def group(x, y, w, h, label, cls="g"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>'
        + text(x + 14, y + 22, label.upper(), "t tg", "start")
    )


def path_d(pts):
    return "M" + " L".join(f"{x} {y}" for x, y in pts)


def arrow(pts, dashed=False, cls="a"):
    m = "ahc" if "thick" in cls else "ah"
    return f'<path d="{path_d(pts)}" class="{cls}{" dash" if dashed else ""}" marker-end="url(#{m})"/>'


def line(pts, dashed=False, cls="a"):
    return f'<path d="{path_d(pts)}" class="{cls}{" dash" if dashed else ""}"/>'


def lock(x, y, s=1.0, cls="lk"):
    """Small padlock, top-left at (x, y), ~12x14 at s=1."""
    return (
        f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
        '<path d="M3 6V4a3 3 0 0 1 6 0v2" fill="none" stroke-width="1.6"/>'
        '<rect x="1" y="6" width="10" height="8" rx="2"/></g>'
    )


def chip(x, y, w, label, kind):
    """A worker chip. kind: preset | own | restricted."""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" class="chip {kind}"/>'
    if kind == "restricted":
        out += lock(x + 10, y + 6, 0.95)
        out += text(x + w / 2 + 8, y + 17.5, label, "t tc")
    else:
        out += text(x + w / 2, y + 17.5, label, "t tc")
    return out


def pod(x, y, kind, s=18, extra=""):
    cls = {"preset": "pod preset", "own": "pod own", "restricted": "pod restricted"}[kind]
    out = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" class="{cls}{extra}"/>'
    if kind == "restricted":
        out += lock(x + 4, y + 3, 0.8, "lk ink")
    return out


# ------------------------------------------------------------------ D1 architecture
def d1():
    b = []
    # who submits
    b.append(group(10, 10, 210, 600, "Who submits work"))
    b.append(box(26, 58, 178, 62, "Apps and maps", "OnlyMap · API · CLI"))
    b.append(box(26, 140, 178, 62, "Pipeline tools", "Argo · Kubeflow · FME Flow"))
    b.append(box(26, 222, 178, 62, "Scripts and services", "scheduled or on demand"))
    b.append(text(26, 330, "PEOPLE AND ROLES", "t tg", "start"))
    b.append('<circle cx="40" cy="356" r="7" class="role ok"/>' + text(54, 361, "Cleared analysts", "t ts2", "start"))
    b.append('<circle cx="40" cy="384" r="7" class="role other"/>' + text(54, 389, "All other users", "t ts2", "start"))
    b.append(text(26, 420, "Every request carries the", "t ts", "start"))
    b.append(text(26, 437, "caller's roles.", "t ts", "start"))
    # bus to gateway
    for y in (89, 171, 253):
        b.append(line([(204, y), (232, y)]))
    b.append(line([(232, 89), (232, 253)]))
    b.append(arrow([(232, 108), (290, 108)], False, "a flow"))
    b.append(line([(150, 370), (232, 370), (232, 174), (290, 174)], True, "a mute"))

    # cluster
    b.append(group(244, 10, 746, 600, "Your Kubernetes cluster", "g outer"))
    b.append(group(262, 46, 302, 470, "Control plane"))
    b.append(box(290, 82, 246, 52, "Gateway", "authenticates every request"))
    b.append(box(290, 150, 246, 52, "Access control", "caller's roles vs the worker"))
    b.append(box(290, 218, 246, 56, "Orchestrator", "queue · fan-out · placement", "b acc"))
    b.append(arrow([(413, 134), (413, 150)]))
    b.append(arrow([(413, 202), (413, 218)]))
    # catalogue with worker types
    b.append(f'<rect x="276" y="292" width="274" height="146" rx="12" class="b"/>')
    b.append(text(290, 314, "Worker catalogue", "t tb", "start"))
    b.append(text(536, 314, "versioned", "t ts", "end"))
    b.append(chip(290, 326, 112, "Conversion", "preset"))
    b.append(chip(410, 326, 126, "Cloud removal", "preset"))
    b.append(chip(290, 360, 112, "Resampling", "preset"))
    b.append(chip(410, 360, 126, "Your Python / R", "own"))
    b.append(chip(290, 396, 246, "Sensitive analysis · restricted", "restricted"))
    b.append(arrow([(413, 292), (413, 274)], True))
    b.append(box(276, 452, 274, 50, "Observability", "runtime · CPU · GPU · RAM per run"))

    # execution plane
    b.append(group(590, 46, 382, 470, "Execution plane · one pod per task"))
    pools = [
        (80, "CPU pool", "everyday processing", ["preset"] * 5 + ["own"] * 3 + ["preset"] * 2),
        (204, "High-memory pool", "sized to the largest raster", ["preset", "own", "own", "restricted", "preset", "own", "restricted"]),
        (328, "GPU pool", "CUDA GPUs of several sizes", ["own", "restricted", "restricted", "own", "own"]),
    ]
    for y, t, s, kinds in pools:
        b.append(f'<rect x="608" y="{y}" width="346" height="108" rx="10" class="b"/>')
        b.append(text(624, y + 24, t, "t tb", "start"))
        b.append(text(624, y + 42, s, "t ts", "start"))
        for k, kind in enumerate(kinds):
            extra = " blink" if k == len(kinds) - 1 else ""
            b.append(pod(624 + k * 30, y + 62, kind, 22, extra))
    # legend
    ly = 458
    b.append(f'<rect x="624" y="{ly}" width="14" height="14" rx="3" class="pod preset"/>' + text(644, ly + 12, "preset worker", "t ts", "start"))
    b.append(f'<rect x="742" y="{ly}" width="14" height="14" rx="3" class="pod own"/>' + text(762, ly + 12, "your code", "t ts", "start"))
    b.append(f'<rect x="842" y="{ly}" width="14" height="14" rx="3" class="pod restricted"/>' + text(862, ly + 12, "restricted", "t ts", "start"))
    b.append(text(624, ly + 38, "Restricted tasks: cleared callers only, in their own pods.", "t ts", "start"))
    # flows
    b.append(arrow([(536, 246), (590, 246)], False, "a thick flow"))
    b.append(arrow([(590, 478), (550, 478)], True, "a"))
    b.append(box(262, 540, 302, 56, "Cluster autoscaler", "adds nodes within each pool's limit"))
    b.append(box(590, 540, 382, 56, "Shared storage", "inputs in · one result per task out", "b store"))
    b.append(arrow([(564, 568), (577, 568), (577, 500), (590, 500)], True))
    b.append(arrow([(781, 516), (781, 540)]))
    return svg(1000, 620, "".join(b), f"{NAME} architecture: clients call the gateway; access control checks roles against preset, custom and restricted workers; the orchestrator places tasks on CPU, high-memory and GPU pools that share storage", "dg d1-wide")


# ------------------------------------------------------------------ D1 portrait (phones)
def d1_tall():
    b = []
    b.append(group(10, 10, 440, 236, "Who submits work"))
    for y, t, sub in [(46, "Apps and maps", "OnlyMap · API · CLI"), (94, "Pipeline tools", "Argo · Kubeflow · FME Flow"), (142, "Scripts and services", "scheduled or on demand")]:
        b.append(f'<rect x="26" y="{y}" width="408" height="40" rx="10" class="b"/>')
        b.append(text(42, y + 25, t, "t tb", "start"))
        b.append(text(420, y + 25, sub, "t ts", "end"))
    b.append('<circle cx="40" cy="204" r="7" class="role ok"/>' + text(54, 209, "Cleared analysts", "t ts2", "start"))
    b.append('<circle cx="200" cy="204" r="7" class="role other"/>' + text(214, 209, "All other users", "t ts2", "start"))
    b.append(text(26, 234, "Every request carries the caller's roles.", "t ts", "start"))
    b.append(arrow([(230, 186), (230, 318)], False, "a flow"))
    b.append(line([(33, 204), (18, 204), (18, 403), (40, 403)], True, "a mute"))

    b.append(group(10, 262, 440, 990, "Your Kubernetes cluster", "g outer"))
    b.append(group(22, 282, 416, 444, "Control plane"))
    b.append(box(40, 318, 380, 46, "Gateway", "authenticates every request"))
    b.append(box(40, 380, 380, 46, "Access control", "caller's roles vs the worker"))
    b.append(box(40, 442, 380, 50, "Orchestrator", "queue · fan-out · placement", "b acc"))
    b.append(arrow([(230, 364), (230, 380)]))
    b.append(arrow([(230, 426), (230, 442)]))
    b.append('<rect x="40" y="510" width="380" height="138" rx="12" class="b"/>')
    b.append(text(54, 532, "Worker catalogue", "t tb", "start"))
    b.append(text(406, 532, "versioned", "t ts", "end"))
    b.append(chip(54, 546, 170, "Conversion", "preset"))
    b.append(chip(236, 546, 170, "Cloud removal", "preset"))
    b.append(chip(54, 580, 170, "Resampling", "preset"))
    b.append(chip(236, 580, 170, "Your Python / R", "own"))
    b.append(chip(54, 614, 352, "Sensitive analysis · restricted", "restricted"))
    b.append(arrow([(230, 510), (230, 492)], True))
    b.append(box(40, 664, 380, 46, "Observability", "runtime · CPU · GPU · RAM per run"))

    b.append(group(22, 742, 416, 420, "Execution plane · one pod per task"))
    pools = [
        (778, "CPU pool", "everyday processing", ["preset"] * 5 + ["own"] * 3 + ["preset"] * 2),
        (890, "High-memory pool", "sized to the largest raster", ["preset", "own", "own", "restricted", "preset", "own", "restricted"]),
        (1002, "GPU pool", "CUDA GPUs of several sizes", ["own", "restricted", "restricted", "own", "own"]),
    ]
    for y, t, sub, kinds in pools:
        b.append(f'<rect x="40" y="{y}" width="380" height="100" rx="10" class="b"/>')
        b.append(text(56, y + 24, t, "t tb", "start"))
        b.append(text(56, y + 42, sub, "t ts", "start"))
        for k, kind in enumerate(kinds):
            b.append(pod(56 + k * 30, y + 58, kind, 22, " blink" if k == len(kinds) - 1 else ""))
    ly = 1116
    b.append(f'<rect x="56" y="{ly}" width="14" height="14" rx="3" class="pod preset"/>' + text(76, ly + 12, "preset worker", "t ts", "start"))
    b.append(f'<rect x="182" y="{ly}" width="14" height="14" rx="3" class="pod own"/>' + text(202, ly + 12, "your code", "t ts", "start"))
    b.append(f'<rect x="290" y="{ly}" width="14" height="14" rx="3" class="pod restricted"/>' + text(310, ly + 12, "restricted", "t ts", "start"))
    b.append(text(56, ly + 34, "Restricted tasks: cleared callers only, in their own pods.", "t ts", "start"))
    b.append(arrow([(420, 467), (431, 467), (431, 828), (420, 828)], False, "a thick flow"))
    b.append(arrow([(120, 742), (120, 710)], True))
    b.append(box(22, 1182, 204, 56, "Cluster autoscaler", "adds nodes per pool", rx=10))
    b.append(box(234, 1182, 204, 56, "Shared storage", "inputs in · results out", "b store"))
    b.append(arrow([(124, 1182), (124, 1162)], True))
    b.append(arrow([(336, 1162), (336, 1182)]))
    return svg(460, 1262, "".join(b), f"{NAME} architecture, stacked for small screens", "dg d1-tall")


# ------------------------------------------------------------------ D-access
def daccess():
    cols = [("Conversion", "preset"), ("Cloud removal", "preset"), ("Resampling", "preset"), ("Your Python / R", "own"), ("Sensitive analysis", "restricted")]
    b = []
    x0, cw = 190, 150
    for i, (t, k) in enumerate(cols):
        x = x0 + i * cw
        b.append(f'<rect x="{x}" y="14" width="{cw-12}" height="64" rx="12" class="b wk {k}"/>')
        if k == "restricted":
            b.append(lock(x + (cw - 12) / 2 - 6, 19, 0.9))
            b.append(text(x + (cw - 12) / 2, 50, t, "t tb"))
            b.append(text(x + (cw - 12) / 2, 67, "restricted worker", "t ts amb"))
        else:
            b.append(text(x + (cw - 12) / 2, 42, t, "t tb"))
            b.append(text(x + (cw - 12) / 2, 62, "preset" if k == "preset" else "your own code", "t ts"))
    rows = [("Cleared analysts", "ok", [1, 1, 1, 1, 1]), ("All other users", "other", [1, 1, 1, 1, 0])]
    for r, (lab, cls, cells) in enumerate(rows):
        y = 104 + r * 66
        b.append(f'<circle cx="24" cy="{y+22}" r="8" class="role {cls}"/>')
        b.append(text(42, y + 27, lab, "t tb", "start"))
        for i, ok in enumerate(cells):
            x = x0 + i * cw
            c = "cell ok" if ok else "cell no"
            b.append(f'<rect x="{x}" y="{y}" width="{cw-12}" height="44" rx="10" class="{c}"/>')
            b.append(text(x + (cw - 12) / 2, y + 27, "Granted" if ok else "Blocked", "t tb"))
    # animated requests
    b.append('<g class="req req-ok"><circle cx="0" cy="0" r="7" class="role ok"/></g>')
    b.append('<g class="req req-no"><circle cx="0" cy="0" r="7" class="role other"/></g>')
    b.append('<g class="xmark"><path d="M-8 -8L8 8M8 -8L-8 8"/></g>')
    b.append(text(450, 262, "A blocked request is refused at the gateway. No pod starts and no capacity is spent.", "t ts"))
    return svg(950, 276, "".join(b), "Worker types and who can run them: cleared analysts can run every worker; all other users can run the open workers and are blocked from restricted ones", "dg anim-access")


# ------------------------------------------------------------------ D2 life of a job
def d2():
    steps = [
        ("1", "Submit", "worker, exact version,\nmachine class, inputs"),
        ("2", "Authorise", "caller's roles checked\nagainst the worker"),
        ("3", "Accept and fan out", "one job ID · batch jobs\nexpand into tasks"),
        ("4", "Place", "each task goes to the pool\nfor its machine class"),
        ("5", "Run", "a pod starts from the\nworker image"),
        ("6", "Write results", "outputs land in shared\nstorage, one per task"),
        ("7", "Record", "status, logs and CPU,\nGPU, RAM per run"),
    ]
    b = []
    xs = [10, 250, 490, 730]
    for i, (n, t, s) in enumerate(steps):
        row, col = divmod(i, 4)
        x, y = xs[col], 20 + row * 150
        b.append(f'<g class="step" style="--i:{i}"><rect x="{x}" y="{y}" width="200" height="120" rx="12" class="b"/></g>')
        b.append(f'<circle cx="{x+28}" cy="{y+30}" r="14" class="num"/>')
        b.append(text(x + 28, y + 35, n, "t tn"))
        b.append(text(x + 52, y + 36, t, "t tb", "start"))
        for j, ln in enumerate(s.split("\n")):
            b.append(text(x + 18, y + 68 + j * 20, ln, "t ts", "start"))
        if col < 3 and i < 6:
            b.append(arrow([(x + 200, y + 60), (x + 248, y + 60)]))
    b.append(arrow([(930, 140), (930, 158), (110, 158), (110, 170)], False, "a mute"))
    return svg(950, 310, "".join(b), "Seven steps in the life of a job", "dg anim-steps")


# ------------------------------------------------------------------ D4 where it fits
def d4():
    b = []
    b.append(group(10, 10, 740, 130, "Where work comes from"))
    tops = [("Map apps", "OnlyMap front ends"), ("Argo Workflows", "steps and triggers"), ("Kubeflow Pipelines", "ML and data pipelines"), ("FME Flow", "workspaces · Automations")]
    for i, (t, s) in enumerate(tops):
        b.append(box(28 + i * 180, 50, 164, 64, t, s))
        b.append(arrow([(110 + i * 180, 114), (110 + i * 180, 186)], False, "a flow"))
    b.append(box(28, 186, 712, 60, "@@N@@", "submit · authorise · schedule · run · observe", "b acc"))
    b.append(group(10, 284, 740, 96, "Data you own"))
    b.append(box(28, 316, 500, 48, "Shared storage", "Cloud-Optimised GeoTIFF · Zarr · GeoJSON · GeoParquet", "b store"))
    b.append(box(574, 316, 166, 48, "Imagery servers", "e.g. ArcGIS Image Server"))
    b.append(arrow([(290, 246), (290, 316)], False, "a"))
    b.append(text(300, 288, "writes results", "t ts", "start"))
    b.append(arrow([(528, 340), (574, 340)], True))
    b.append(text(551, 308, "reads", "t ts"))
    b.append(group(10, 400, 740, 66, "Infrastructure"))
    b.append(box(200, 414, 540, 40, "Kubernetes · nodes · GPUs · volumes"))
    return svg(760, 476, "".join(b), f"Map apps, Argo, Kubeflow and FME Flow submit work to {NAME}; it writes results to storage that imagery servers and maps read; everything runs on Kubernetes")


# ------------------------------------------------------------------ D5 batch fan-out
def d5():
    b = []
    b.append(box(10, 90, 170, 80, "1 batch job", "worker 1.2.0 · 200 scenes"))
    b.append(box(230, 90, 150, 80, "Orchestrator", "fans out", "b acc"))
    b.append(arrow([(180, 130), (230, 130)], False, "a flow"))
    for i, t in enumerate(["Task 1 · scene 001", "Task 2 · scene 002", "Task 3 · scene 003", "Task 200 · scene 200"]):
        y = 14 + i * 64
        b.append(f'<g class="task" style="--i:{i}"><rect x="440" y="{y}" width="190" height="48" rx="10" class="b tk"/></g>')
        b.append(text(535, y + 29, t, "t tb"))
        b.append(arrow([(380, 130), (440, y + 24)], False, "a flow"))
        b.append(arrow([(630, y + 24), (680, y + 24), (680, 120), (700, 120)], False, "a mute"))
    b.append(box(700, 76, 190, 90, "Shared storage", "one result per task", "b store"))
    b.append(text(535, 284, "tasks run in parallel; the pool scales with the queue", "t ts"))
    return svg(900, 300, "".join(b), "A batch job fans out into parallel tasks that each write one result", "dg anim-tasks")


# ------------------------------------------------------------------ D6 OnlyMap + GeoEngine
def d6():
    b = []
    b.append(group(10, 10, 250, 300, "Browser"))
    b.append(box(28, 48, 214, 60, "OnlyMap", "the map your users see", "b own2"))
    for i, t in enumerate(["draw an area of interest", "watch tasks complete live", "explore results as layers"]):
        b.append(text(40, 140 + i * 26, "· " + t, "t ts2", "start"))
    b.append(box(320, 48, 200, 60, "Your app API", "auth · business rules"))
    b.append(group(580, 10, 310, 300, "Your Kubernetes cluster", "g outer"))
    b.append(box(600, 48, 270, 60, "@@N@@", "batch job → parallel tasks", "b acc"))
    b.append(box(600, 216, 270, 64, "Shared storage", "COG · Zarr · GeoJSON results", "b store"))
    b.append(arrow([(242, 70), (320, 70)], False, "a flow"))
    b.append(text(281, 62, "1", "t tnum"))
    b.append(arrow([(520, 70), (600, 70)], False, "a flow"))
    b.append(text(560, 62, "2", "t tnum"))
    b.append(arrow([(735, 108), (735, 216)], False, "a flow"))
    b.append(text(747, 166, "3 tasks write results", "t ts", "start"))
    b.append(arrow([(320, 94), (242, 94)], True))
    b.append(text(281, 112, "4", "t tnum"))
    b.append(arrow([(600, 260), (220, 260), (220, 108)], True, "a"))
    b.append(text(410, 252, "5 stream tiles by HTTP range request", "t ts"))
    b.append(text(450, 334, "1 submit the area · 2 create a batch job · 4 poll status and per-task results", "t ts"))
    return svg(900, 346, "".join(b), f"OnlyMap in the browser calls your app API, which submits a batch job to {NAME}; tasks write results to storage that OnlyMap streams directly")


# ------------------------------------------------------------------ problem infographics
def p_memory():
    b = []
    b.append(text(70, 16, "Fixed server · 64 GB", "t ts2"))
    b.append('<rect x="40" y="70" width="60" height="80" rx="6" class="gauge"/>')
    b.append('<rect x="46" y="30" width="48" height="114" rx="4" class="fillbar over"/>')
    b.append('<rect x="40" y="70" width="60" height="80" rx="6" class="gauge top"/>')
    b.append(text(70, 166, "✕ out of memory", "t ts bad pop"))
    b.append(text(230, 16, "Sized worker · 128 GB", "t ts2"))
    b.append('<rect x="200" y="22" width="60" height="128" rx="6" class="gauge"/>')
    b.append('<rect x="206" y="30" width="48" height="114" rx="4" class="fillbar fit"/>')
    b.append(text(230, 166, "✓ fits", "t ts good pop"))
    b.append(text(150, 96, "96 GB", "t tb"))
    b.append(text(150, 112, "raster", "t ts"))
    return svg(300, 176, "".join(b), "A 96 GB raster overflows a 64 GB server but fits a 128 GB high-memory worker", "ig ig-mem")


def p_fanout():
    b = []
    b.append(text(10, 16, "One at a time", "t ts2", "start"))
    b.append('<line x1="10" y1="34" x2="290" y2="34" class="lane"/>')
    b.append('<circle cx="10" cy="34" r="6" class="dot serial"/>')
    b.append(text(10, 70, "Fanned out", "t ts2", "start"))
    for i in range(6):
        y = 86 + i * 14
        b.append(f'<line x1="10" y1="{y}" x2="290" y2="{y}" class="lane"/>')
        b.append(f'<circle cx="10" cy="{y}" r="5" class="dot par" style="--d:{i*0.13:.2f}s"/>')
    return svg(300, 176, "".join(b), "Processing scenes one at a time versus fanned out in parallel", "ig ig-fan")


def p_stack():
    b = []
    labels = ["Your code", "PyTorch · numpy", "rasterio · shapely", "GDAL 3.9 · PROJ", "CUDA 12.2"]
    for i, t in enumerate(labels):
        y = 8 + i * 28
        b.append(f'<g class="blk" style="--i:{i}"><rect x="60" y="{y}" width="180" height="24" rx="6" class="b sblk"/>{text(150, y + 16.5, t, "t ts2")}</g>')
    b.append(text(150, 168, "✕ version conflicts", "t ts bad clash"))
    b.append(text(150, 168, "✓ one managed geo runtime", "t ts good pop"))
    return svg(300, 176, "".join(b), "Conflicting GDAL, CUDA and Python package versions snapping into one managed runtime", "ig ig-stack")


def p_gate():
    b = []
    b.append('<line x1="186" y1="10" x2="186" y2="140" class="gate"/>')
    b.append(lock(176, 62, 1.6))
    b.append(text(250, 24, "Sensitive", "t ts2"))
    b.append(text(250, 40, "analysis", "t ts2"))
    b.append('<circle cx="0" cy="0" r="8" class="role ok tok tok-ok"/>')
    b.append('<circle cx="0" cy="0" r="8" class="role other tok tok-no"/>')
    b.append('<g class="xmark2"><path d="M160 104l12 12M172 104l-12 12"/></g>')
    b.append('<circle cx="16" cy="162" r="5" class="role ok"/>' + text(26, 166, "cleared", "t ts", "start"))
    b.append('<circle cx="96" cy="162" r="5" class="role other"/>' + text(106, 166, "everyone else", "t ts", "start"))
    return svg(300, 176, "".join(b), "Cleared analysts pass the gate to a sensitive worker; everyone else is blocked", "ig ig-gate")


# ------------------------------------------------------------------ phone (stacked) versions
def daccess_tall():
    rows = [("Conversion", "preset"), ("Cloud removal", "preset"), ("Resampling", "preset"), ("Your Python / R", "own"), ("Sensitive analysis", "restricted")]
    b = []
    b.append('<circle cx="262" cy="26" r="6" class="role ok"/>' + text(272, 30, "Cleared", "t ts2", "start"))
    b.append('<circle cx="360" cy="26" r="6" class="role other"/>' + text(370, 30, "Everyone else", "t ts2", "start"))
    for i, (t, k) in enumerate(rows):
        y = 50 + i * 56
        b.append(f'<rect x="16" y="{y}" width="220" height="44" rx="10" class="b wk {k}"/>')
        b.append(text(30, y + 19, t, "t tb", "start"))
        b.append(text(30, y + 36, {"preset": "preset", "own": "your own code", "restricted": "restricted worker"}[k], "t ts" + (" amb" if k == "restricted" else ""), "start"))
        if k == "restricted":
            b.append(lock(212, y + 8, 1.0))
        for j, x in enumerate((248, 352)):
            ok = not (k == "restricted" and j == 1)
            b.append(f'<rect x="{x}" y="{y}" width="92" height="44" rx="10" class="cell {"ok" if ok else "no"}"/>')
            b.append(text(x + 46, y + 27, "Granted" if ok else "Blocked", "t tb"))
    b.append(text(230, 350, "A blocked request is refused at the gateway.", "t ts"))
    b.append(text(230, 368, "No pod starts and no capacity is spent.", "t ts"))
    return svg(460, 382, "".join(b), "Worker types and who can run them, stacked for small screens", "dg")


def d2_tall():
    steps = [
        ("1", "Submit", "worker, exact version, machine class, inputs"),
        ("2", "Authorise", "caller's roles checked against the worker"),
        ("3", "Accept and fan out", "one job ID · batch jobs expand into tasks"),
        ("4", "Place", "each task goes to the pool for its class"),
        ("5", "Run", "a pod starts from the worker image"),
        ("6", "Write results", "outputs land in shared storage, one per task"),
        ("7", "Record", "status, logs and CPU, GPU, RAM per run"),
    ]
    b = []
    for i, (n, t, sub) in enumerate(steps):
        y = 10 + i * 76
        b.append(f'<g class="step" style="--i:{i}"><rect x="20" y="{y}" width="420" height="60" rx="12" class="b"/></g>')
        b.append(f'<circle cx="48" cy="{y + 30}" r="14" class="num"/>')
        b.append(text(48, y + 35, n, "t tn"))
        b.append(text(74, y + 26, t, "t tb", "start"))
        b.append(text(74, y + 45, sub, "t ts", "start"))
        if i < 6:
            b.append(arrow([(230, y + 60), (230, y + 76)]))
    return svg(460, 542, "".join(b), "Seven steps in the life of a job, stacked for small screens", "dg anim-steps")


def d4_tall():
    b = []
    b.append(group(10, 10, 440, 170, "Where work comes from"))
    for i, (t, sub) in enumerate([("Map apps", "OnlyMap front ends"), ("Argo Workflows", "steps and triggers"), ("Kubeflow Pipelines", "ML and data pipelines"), ("FME Flow", "workspaces · Automations")]):
        x, y = 26 + (i % 2) * 208, 46 + (i // 2) * 64
        b.append(box(x, y, 200, 56, t, sub))
    b.append(arrow([(230, 180), (230, 210)], False, "a flow"))
    b.append(text(242, 199, "submit · poll · read", "t ts", "start"))
    b.append(box(26, 210, 408, 60, "@@N@@", "authorise · schedule · run · observe", "b acc"))
    b.append(group(10, 300, 440, 170, "Data you own"))
    b.append(box(26, 334, 408, 56, "Shared storage", "COG · Zarr · GeoJSON · GeoParquet", "b store"))
    b.append(box(26, 410, 408, 50, "Imagery servers", "e.g. ArcGIS Image Server"))
    b.append(arrow([(230, 270), (230, 334)]))
    b.append(text(242, 292, "writes results", "t ts", "start"))
    b.append(arrow([(230, 390), (230, 410)], True))
    b.append(text(242, 404, "reads", "t ts", "start"))
    b.append(group(10, 490, 440, 70, "Infrastructure"))
    b.append(box(26, 516, 408, 34, "Kubernetes · nodes · GPUs · volumes"))
    return svg(460, 570, "".join(b), f"Where {NAME} fits, stacked for small screens", "dg")


def d5_tall():
    b = []
    b.append(box(115, 10, 230, 64, "1 batch job", "worker 1.2.0 · 200 scenes"))
    b.append(arrow([(230, 74), (230, 100)], False, "a flow"))
    b.append(box(130, 100, 200, 56, "Orchestrator", "fans out", "b acc"))
    b.append(line([(230, 156), (230, 170), (60, 170), (60, 369)], False, "a flow"))
    for i, t in enumerate(["Task 1 · scene 001", "Task 2 · scene 002", "Task 3 · scene 003", "Task 200 · scene 200"]):
        y = 186 + i * 54
        b.append(f'<g class="task" style="--i:{i}"><rect x="80" y="{y}" width="300" height="42" rx="10" class="b tk"/></g>')
        b.append(text(230, y + 26, t, "t tb"))
        b.append(arrow([(60, y + 21), (80, y + 21)]))
        b.append(line([(380, y + 21), (400, y + 21)], False, "a mute"))
    b.append(line([(400, 207), (400, 442)], False, "a mute"))
    b.append(arrow([(400, 442), (380, 442)], False, "a mute"))
    b.append(box(80, 410, 300, 64, "Shared storage", "one result per task", "b store"))
    b.append(text(230, 500, "tasks run in parallel; the pool scales with the queue", "t ts"))
    return svg(460, 516, "".join(b), "A batch job fans out into parallel tasks, stacked for small screens", "dg anim-tasks")


def d6_tall():
    b = []
    b.append(group(10, 10, 440, 160, "Browser"))
    b.append(box(26, 46, 408, 56, "OnlyMap", "the map your users see", "b own2"))
    b.append(text(40, 128, "· draw an area of interest", "t ts2", "start"))
    b.append(text(40, 150, "· watch tasks complete live", "t ts2", "start"))
    b.append(box(26, 196, 408, 56, "Your app API", "auth · business rules"))
    b.append(arrow([(390, 102), (390, 196)], False, "a flow"))
    b.append(text(400, 154, "1", "t tnum", "start"))
    b.append(arrow([(330, 196), (330, 102)], True))
    b.append(text(314, 154, "4", "t tnum", "start"))
    b.append(group(10, 278, 440, 286, "Your Kubernetes cluster", "g outer"))
    b.append(box(26, 312, 408, 56, "@@N@@", "batch job → parallel tasks", "b acc"))
    b.append(arrow([(390, 252), (390, 312)], False, "a flow"))
    b.append(text(400, 288, "2", "t tnum", "start"))
    b.append(box(26, 476, 408, 64, "Shared storage", "COG · Zarr · GeoJSON results", "b store"))
    b.append(arrow([(230, 368), (230, 476)], False, "a flow"))
    b.append(text(242, 426, "3 tasks write results", "t ts", "start"))
    b.append(arrow([(26, 508), (18, 508), (18, 74), (26, 74)], True))
    b.append(text(230, 592, "5 OnlyMap streams tiles by HTTP range request", "t ts"))
    b.append(text(230, 612, "1 submit the area · 2 create a batch job", "t ts"))
    b.append(text(230, 630, "4 poll status and per-task results", "t ts"))
    return svg(460, 646, "".join(b), f"OnlyMap and {NAME}, stacked for small screens", "dg")


# Output file stem -> builder. build_diagrams.py renders each in light and dark.
FIGURES = {
    "architecture": d1, "architecture-tall": d1_tall, "access": daccess, "job-lifecycle": d2,
    "stack-fit": d4, "batch-fanout": d5, "onlymap-flow": d6,
    "access-tall": daccess_tall, "job-lifecycle-tall": d2_tall, "stack-fit-tall": d4_tall,
    "batch-fanout-tall": d5_tall, "onlymap-flow-tall": d6_tall,
    "problem-memory": p_memory, "problem-fanout": p_fanout, "problem-stack": p_stack, "problem-gate": p_gate,
}
