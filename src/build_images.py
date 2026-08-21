# -*- coding: utf-8 -*-
"""
Image pipeline.

Takes the uploaded source images, assigns each to a named slot, slices the
"Representative Projects" composite into six individual project cards, and
emits responsive AVIF + WebP at three widths.

Run:  python3 build_images.py
"""

import os, shutil
from PIL import Image
try:                      # Pillow < 11.3 needs a plugin to write AVIF
    import pillow_avif    # noqa: F401
except ImportError:
    pass

# Override with IMAGE_SRC when the originals live somewhere else, which they
# will on any machine other than the one that first built this.
SRC = os.environ.get("IMAGE_SRC", "/mnt/user-data/uploads")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/img")

# slot -> (source file, tier, alt text, caption)
# tier A = work/objects, no people. B = labelled illustrative. C = people.
SLOTS = {
    # --- Tier C: people -----------------------------------------------------
    "hero": ("ChatGPT_Image_Aug_13__2026__01_00_48_PM.png", "C",
             "Engineers working on BIM models at a row of workstations",
             "Illustrative image"),
    "facilities": ("ChatGPT_Image_Aug_13__2026__01_26_22_PM.png", "C",
                   "Open-plan CAD training floor with multiple workstations",
                   "Illustrative image — photography of the Sector 14 centre pending"),
    "classroom": ("ChatGPT_Image_Aug_13__2026__01_16_09_PM.png", "C",
                  "A trainer explaining a Revit model to a class on a large display",
                  "Illustrative image"),
    "sitevisit": ("ChatGPT_Image_Aug_13__2026__01_26_03_PM.png", "C",
                  "Engineers in hard hats reviewing drawings on a construction site",
                  "Illustrative image"),
    "presentation": ("ChatGPT_Image_Aug_13__2026__01_26_13_PM.png", "C",
                     "Learners presenting a mechanical gear assembly to a reviewer",
                     "Illustrative image"),
    "corporate": ("ChatGPT_Image_Aug_13__2026__01_25_41_PM.png", "C",
                  "A team reviewing an industrial plant layout on screen",
                  "Illustrative image"),
    "trainer-context": ("ChatGPT_Image_Aug_13__2026__01_22_31_PM.png", "C",
                        "A trainer presenting design software to a seated group",
                        "Illustrative image — not a portrait of a named trainer"),
    # Its own slot rather than replacing "corporate", which the homepage and the
    # Life @ CADD gallery also use.
    "industry-team": ("About.jpg", "C",
                      "Learners at workstations in a CAD training lab",
                      "Illustrative image"),

    # --- Tier A: work and objects, no people --------------------------------
    "printing": ("ChatGPT_Image_Aug_13__2026__01_10_00_PM.png", "A",
                 "A 3D printer producing a mechanical housing beside the CAD model it was printed from",
                 "Representative of the CAD-to-prototype workflow"),
    "mech": ("ChatGPT_Image_Aug_13__2026__01_12_36_PM.png", "A",
             "Exploded view of a machined mechanical assembly laid over technical drawings",
             "Representative project output"),
    "arch": ("ChatGPT_Image_Aug_13__2026__01_12_46_PM.png", "A",
             "Architectural visualisation of a modern residence at dusk",
             "Representative project output"),
    "bim": ("ChatGPT_Image_Aug_13__2026__01_16_01_PM.png", "A",
            "A building shown as a photograph, a coordinated BIM model and a drawing set",
            "Representative project output"),
    "civil": ("ChatGPT_Image_Aug_13__2026__01_23_01_PM.png", "A",
              "A highway interchange shown as built, as a Civil 3D corridor model and as cross sections",
              "Representative project output"),

    # Student work. 5:4 source; the 4:3 card trims 6% top and bottom, which is
    # dark background above and the edge of the drawing sheet below.
    "proj-mep-coordination": ("MEP Services.png", "B",
                              "A federated MEP model in Revit with colour-coded HVAC, plumbing and "
                              "electrical services, the systems browser and a clash detective report",
                              "Representative project"),

    # --- Per-programme card art ---------------------------------------------
    "prog-revit-architecture": ("Revit Architecture.png", "A",
                                "A three-storey building shown half as a finished render and half as a "
                                "Revit model with structure and MEP services exposed, over drawing sheets",
                                "Representative project output"),
    "prog-revit-structure": ("Revit Structure.png", "A",
                             "A reinforced concrete frame model beside the same structure open in Revit, "
                             "with the project browser showing structural plans and levels",
                             "Representative project output"),
    "prog-revit-mep": ("Revit MEP.png", "A",
                       "A coordinated Revit MEP model on screen showing colour-coded ducting, pipework "
                       "and services above a ceiling, with duct and pipe fittings on the desk",
                       "Representative project output"),
    "prog-civil-3d": ("Civil 3D.png", "A",
                      "A highway interchange corridor model open in Civil 3D showing alignments and "
                      "surfaces, beside a physical road and bridge model on drawing sheets",
                      "Representative project output"),
    "prog-autocad-civil": ("AutoCad Civil.png", "A",
                           "A highway alignment drawing open in AutoCAD Civil showing contours, "
                           "carriageways and a roundabout, over printed setting-out sheets",
                           "Representative project output"),
    "prog-staad-pro": ("STAAD.Pro.png", "A",
                       "A steel frame analysed in STAAD.Pro with beam stresses shown as a colour "
                       "contour and a legend, beside a printed structural drawing set",
                       "Representative project output"),
    "prog-etabs": ("ETABS (CSI).png", "A",
                   "A multi-storey building analysed in ETABS with member forces shown as a colour "
                   "contour and a legend, beside a concrete frame model and drawing sheets",
                   "Representative project output"),
    "prog-5d-bim": ("5D BIM.png", "A",
                    "A 5D BIM workspace showing a building model beside a cost summary, a quantity "
                    "takeoff table and a project schedule, with a concrete frame model on the desk",
                    "Representative project output"),
    "prog-5d-bim-navisworks": ("5D BIM using Navisworks.png", "A",
                               "A federated hospital model open in Navisworks with the Clash Detective "
                               "listing hard and soft clashes and a quantity takeoff panel alongside",
                               "Representative project output"),
    "prog-sketchup": ("SketchUp.png", "A",
                      "A house modelled in SketchUp with the materials tray open, beside a timber "
                      "massing model and a sketchbook of hand-drawn elevations",
                      "Representative project output"),
    "prog-v-ray": ("V-Ray.png", "A",
                   "A dusk exterior render in the V-Ray frame buffer with the asset editor showing "
                   "render quality and environment settings, beside printed sketches and renders",
                   "Representative project output"),
    "prog-lumion": ("Lumion.png", "A",
                    "A landscaped office building in Lumion with the movie effects panel open and a "
                    "walkthrough clip timeline showing the same view from day through to night",
                    "Representative project output"),
    "prog-3ds-max": ("3D Max for Engineers.png", "A",
                     "A house in 3ds Max shown across perspective, wireframe and shaded viewports "
                     "with the modelling panel open, beside a physical massing model and sketches",
                     "Representative project output"),
    "prog-solidworks": ("SolidWorks.png", "A",
                        "A machined bearing housing modelled in SolidWorks with its feature tree, "
                        "a simulation result on a laptop, and the finished metal part on the desk",
                        "Representative project output"),
    "prog-catia": ("CATIA.png", "A",
                   "An engine bracket modelled in CATIA V5 with its specification tree of pads, "
                   "pockets and fillets, beside a detail drawing and the machined part",
                   "Representative project output"),
    "prog-nx-cad": ("NX CAD.png", "A",
                    "An engine bracket modelled in Siemens NX with its part navigator history, a "
                    "wireframe view on a laptop, and the machined part beside vernier callipers",
                    "Representative project output"),
    # 5:4 source, unlike the 4:3 rest. The card crops 6% vertically, which is
    # all background here — checked, no logo or caption is lost.
    "prog-creo": ("Creo.png", "A",
                  "A gearbox assembly shown as a cutaway in Creo Parametric with its model tree of "
                  "housing, shaft, gear and bearing parts, over dimensioned 2D drawings",
                  "Representative project output"),
    "prog-ansys": ("Ansys.png", "A",
                   "A static structural analysis in Ansys Mechanical showing von Mises stress on a "
                   "bracket as a colour contour with its scale, mesh and results tree",
                   "Representative project output"),
    "prog-ansys-workbench": ("Ansys Workbench.png", "A",
                             "The Ansys Workbench project schematic linking geometry, static "
                             "structural, fluid flow and system coupling blocks into one workflow",
                             "Representative project output"),
    # 3:2 source. The card crops 11% horizontally, all of it room background —
    # the application window (x 174-1410) is well inside what survives.
    "prog-ansys-fluent": ("Ansys Fluent.png", "A",
                          "A CFD result in Ansys Fluent showing static pressure contours and flow "
                          "streamlines through a valve, with the residuals plot converging",
                          "Representative project output"),
    "prog-nx-nastran": ("NX Nastran.png", "A",
                        "A meshed bracket solved in NX Nastran showing nodal displacement as a "
                        "colour contour, with the simulation navigator and solution summary",
                        "Representative project output"),
    "prog-autodesk-inventor": ("Autodesk Inventor.png", "A",
                               "A gearbox assembly cutaway in Autodesk Inventor with its browser "
                               "listing housing, shafts, spur gears, bearings and fasteners",
                               "Representative project output"),
    "prog-gdt": ("GD & T.png", "A",
                 "A toleranced part drawing carrying feature control frames and datum references, "
                 "with a reference panel explaining position, flatness and perpendicularity",
                 "Representative project output"),
    "prog-autocad-mechanical": ("AutoCAD 2D & 3D Mechanical.png", "A",
                                "A gearbox in AutoCAD shown as a dimensioned 2D drawing beside the "
                                "same part as a 3D solid model cut away to reveal the gear train",
                                "Representative project output"),
    "prog-autocad-3d": ("AutoCAD 3D.png", "A",
                        "A hinge bracket modelled as a 3D solid in AutoCAD with the properties "
                        "palette and solid editing tools open, beside a hand sketch of the part",
                        "Representative project output"),
    "prog-3d-printing": ("3D Printing & Prototyping.png", "A",
                         "A bracket on screen as a CAD model and mid-print on a 3D printer, with "
                         "finished prints, a lattice cube and a gear laid out beside callipers",
                         "Representative project output"),
    "prog-primavera-ppm": ("Primavera P6 with PPM.png", "A",
                           "A planner working through a construction programme, with the schedule "
                           "as a Gantt chart on screen, drawings on the desk and a site model",
                           "Representative project output"),
    "prog-ms-project-ppm": ("MS Project with PPM.png", "A",
                            "A project plan in MS Project showing a task breakdown and Gantt chart "
                            "with a portfolio dashboard of health status, cost and resource summaries",
                            "Representative project output"),
    "prog-autocad-electrical": ("AutoCAD Electrical.png", "A",
                                "A motor control circuit drawn in AutoCAD Electrical with the "
                                "project manager, ladder wiring and a components tool palette",
                                "Representative project output"),
    "prog-pc-schematic": ("PC Schematic.png", "A",
                          "A motor control circuit documented in PC|SCHEMATIC Automation with the "
                          "project explorer, IEC symbol library and a titled drawing sheet",
                          "Representative project output"),
    "prog-automation-cad": ("Automation CAD.png", "A",
                            "A PLC control circuit drawn in an automation CAD package showing "
                            "digital and analogue I/O modules, contactors and a motor starter",
                            "Representative project output"),

    # --- Life @ CADD gallery tiles ------------------------------------------
    "competition": ("Missing gallery image — Technical Competition.png", "C",
                    "Learners comparing a machined engine housing against the 3D model on screen during a design contest",
                    "Illustrative image"),
    "career-workshop": ("Missing gallery image — Career Workshop.png", "C",
                        "A speaker walking a seated group through engineering career paths on a large display",
                        "Illustrative image"),
    "mock-interview": ("Missing gallery image — Mock Interview.png", "C",
                       "A candidate being interviewed by two panellists across a table at a recruitment drive",
                       "Illustrative image"),
    "job-fair": ("Job Fair.png", "C",
                 "Two candidates with CVs talking to an employer at a recruitment stall showing engineering project work",
                 "Illustrative image"),
}

# The "Representative Projects" composite, sliced into six cards.
# (name, slug, tag, crop box on the 1448x1086 source, alt)
GRID_SRC = "ChatGPT_Image_Aug_13__2026__01_23_06_PM__1_.png"
GRID_CELLS = [
    ("BIM coordination", "bim-coordination", "bim", (16, 158, 476, 481),
     "Integrated 3D building information model with architectural, structural and MEP systems"),
    ("Highway corridor design", "highway-corridor", "civil", (490, 158, 950, 481),
     "Civil 3D model showing highway alignment, corridor design and earthwork analysis"),
    ("RCC structural analysis", "rcc-structure", "struct", (964, 158, 1432, 481),
     "STAAD.Pro and ETABS model for structural analysis and design of an RCC building"),
    ("Mechanical assembly", "mechanical-assembly", "mech", (16, 620, 476, 947),
     "3D model of a mechanical engine assembly created in SolidWorks"),
    ("Architectural visualisation", "architectural-viz", "arch", (490, 620, 950, 947),
     "Architectural design and visualisation created using Revit"),
    ("Construction programme", "construction-programme", "pm", (964, 620, 1432, 947),
     "Construction schedule and project controls built in Primavera P6"),
]

WIDTHS = [480, 960, 1600, 2400]

# Audience-card art. These replace an inline SVG drawing, so they have to land
# in exactly the box the drawing occupied (260:150) or the card row loses its
# rhythm. Each is trimmed to its content and then padded back out to that ratio
# on white — the same white the card sits on, so the padding is invisible and
# nothing is cropped away.
CARD_ART = {
    # All four are photographs now rather than drawings, so each was cropped to
    # the box instead of padded — the trim/pad path below would letterbox them on
    # white. Sources kept in src/img-src/. Every crop is centred except
    # aud-fresher, taken from the top so the subject's head stays whole.
    "aud-student": ("aud-student.jpg", 260 / 150,
                    "A smiling student holding a laptop outside a college building"),
    "aud-fresher": ("aud-fresher.jpg", 260 / 150,
                    "A learner working on a mechanical CAD drawing at a desktop workstation"),
    "aud-professional": ("aud-workingProfessional.png", 260 / 150,
                         "A working professional reviewing a 3D building model on a desktop workstation"),
    "aud-corporate": ("aud-corporate.png", 260 / 150,
                      "Glass office towers seen from street level"),
}
CARD_ART_W = 960          # these render ~240 CSS px wide; 960 covers 4x DPR


def emit(im, stem, upscale=1.0):
    """Write AVIF + WebP across the width ladder. Returns bytes written."""
    from PIL import ImageFilter
    total = 0

    if upscale > 1.0:
        # Sliced cards are natively small. A Lanczos upscale plus a light
        # unsharp pass will not invent detail, but it stops the browser doing
        # a cheap bilinear stretch, which is what actually reads as "blurry".
        w0, h0 = im.size
        im = im.resize((round(w0 * upscale), round(h0 * upscale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=62, threshold=3))

    w0, h0 = im.size
    ladder = [w for w in WIDTHS if w <= w0 * 1.15]
    # A source narrower than 960 would otherwise stop at 480 and throw away
    # resolution we actually have. Keep the native size as the top rung.
    if w0 < 960 and w0 not in ladder:
        ladder.append(w0)
    for w in sorted(ladder):
        if w > w0 * 1.15:
            continue
        h = round(h0 * w / w0)
        r = im.resize((w, h), Image.LANCZOS) if w != w0 else im
        # higher fidelity on the tiers a large screen actually pulls
        q_avif = 68 if w >= 1600 else (64 if w >= 960 else 60)
        for ext, kw in (("avif", dict(quality=q_avif)),
                        ("webp", dict(quality=84, method=6))):
            p = os.path.join(OUT, f"{stem}-{w}.{ext}")
            r.save(p, **kw)
            total += os.path.getsize(p)
    return total


def main():
    # Additive, deliberately. The original uploads for most slots are long gone;
    # wiping OUT would destroy artwork this script can no longer regenerate.
    # Only slots whose source is present are re-emitted, and the manifest is
    # merged rather than replaced.
    os.makedirs(OUT, exist_ok=True)

    manifest = {}
    try:
        from image_manifest import IMAGES
        manifest.update(IMAGES)
    except ImportError:
        pass
    total = 0

    for slot, (fn, tier, alt, cap) in SLOTS.items():
        src = os.path.join(SRC, fn)
        if not os.path.exists(src):
            print(f"  ! missing source for {slot}: {fn}")
            continue
        im = Image.open(src).convert("RGB")
        total += emit(im, slot)
        manifest[slot] = {"tier": tier, "alt": alt, "caption": cap,
                          "w": im.size[0], "h": im.size[1]}
        print(f"  {slot:18} {im.size[0]}x{im.size[1]}  tier {tier}")

    for slot, (fn, aspect, alt) in CARD_ART.items():
        src = os.path.join(SRC, fn)
        if not os.path.exists(src):
            print(f"  ! missing source for {slot}: {fn}")
            continue
        im = Image.open(src).convert("RGB")

        # Trim the surrounding white so the artwork fills the box.
        from PIL import ImageChops
        diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
        bbox = diff.convert("L").point(lambda p: 255 if p > 12 else 0).getbbox()
        if bbox:
            im = im.crop(bbox)

        # Pad back out to the card-art ratio, centred, on white.
        w, h = im.size
        if w / h < aspect:
            cw, ch = round(h * aspect), h
        else:
            cw, ch = w, round(w / aspect)
        canvas = Image.new("RGB", (cw, ch), (255, 255, 255))
        canvas.paste(im, ((cw - w) // 2, (ch - h) // 2))
        canvas = canvas.resize((CARD_ART_W, round(CARD_ART_W * ch / cw)), Image.LANCZOS)

        total += emit(canvas, slot)
        manifest[slot] = {"tier": "C", "alt": alt, "caption": "",
                          "w": canvas.size[0], "h": canvas.size[1]}
        print(f"  {slot:18} {canvas.size[0]}x{canvas.size[1]}  card art")

    grid_path = os.path.join(SRC, GRID_SRC)
    if not os.path.exists(grid_path):
        print(f"\n  ! {GRID_SRC} not present — keeping the existing project cards")
        GRID_CELLS.clear()
    grid = Image.open(grid_path).convert("RGB") if GRID_CELLS else None
    if GRID_CELLS:
        print(f"\n  slicing {GRID_SRC} ({grid.size[0]}x{grid.size[1]}) into {len(GRID_CELLS)} cards")
    for name, slug, tag, box, alt in GRID_CELLS:
        cell = grid.crop(box)
        # normalise every card to 4:3 so the grid never jumps
        tw, th = cell.size
        target = 4 / 3
        if tw / th > target:
            nw = int(th * target)
            cell = cell.crop(((tw - nw) // 2, 0, (tw - nw) // 2 + nw, th))
        else:
            nh = int(tw / target)
            cell = cell.crop((0, 0, tw, nh))
        stem = "proj-" + slug
        total += emit(cell, stem, upscale=2.2)
        manifest[stem] = {"tier": "B", "alt": alt, "caption": "Representative project",
                          "name": name, "tag": tag, "w": cell.size[0], "h": cell.size[1]}
        print(f"    {slug:24} {cell.size[0]}x{cell.size[1]}")

    # encoding is explicit: captions carry em-dashes, and Windows would
    # otherwise write cp1252 that Python cannot read back as UTF-8.
    with open(os.path.join(os.path.dirname(OUT), "..", "image_manifest.py"),
              "w", encoding="utf-8") as f:
        f.write("# generated by build_images.py — do not edit\nIMAGES = ")
        f.write(repr(manifest))
        f.write("\n")

    print(f"\n  {len(manifest)} slots, {total/1024/1024:.1f} MB total across all sizes")


if __name__ == "__main__":
    main()
