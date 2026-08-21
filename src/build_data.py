# -*- coding: utf-8 -*-
"""
Complete content data model.

Every entry here traces to a row in content-inventory.csv. The build asserts
that every live URL in the inventory is either produced as a page or has an
explicit redirect — see build.py::verify_coverage().
"""

# ---------------------------------------------------------------------------
# CAREER PATHS — all eight, full content
# key, slug, name, outcome line, intro, roadmap[], roles[(role, desc)],
# suits[], not_for[], programme slugs
# ---------------------------------------------------------------------------
PATHS = [
    ("bim", "bim-digital-construction", "BIM &amp; Digital Construction",
     "The way modern buildings are designed, coordinated and delivered.",
     ["BIM is not a piece of software. It is how large projects are now run &mdash; a single coordinated model that architects, structural engineers and MEP teams all work against, so clashes are found on a screen rather than on site. Firms across the NCR, the Gulf and the UK are hiring for it faster than people are training for it.",
      "A BIM modeller builds and maintains the model to a standard the whole project team can rely on. A coordinator sits a level above: running clash detection between disciplines, chairing coordination reviews, managing model federation, and keeping the information structure consistent as the project changes.",
      "It is precise, collaborative work. You will spend as much time on naming conventions, worksets and information standards as on geometry, because the value of BIM is the data, not the picture."],
     ["AutoCAD fundamentals", "Revit Architecture", "Revit Structure / MEP", "Navisworks clash detection", "Model federation", "ISO 19650 concepts", "Live coordination project"],
     [("BIM Modeller", "Build and maintain discipline models to project standards"),
      ("Revit Technician", "Produce construction documentation from the model"),
      ("BIM Engineer", "Own a discipline model and its data integrity"),
      ("BIM Coordinator", "Run clash detection and cross-discipline coordination"),
      ("Documentation Lead", "Manage drawing production and issue control")],
     ["A civil engineering or architecture graduate", "A working draughtsperson wanting to move up",
      "An interior or site professional aiming at larger projects", "Targeting Gulf or European roles where BIM is mandated"],
     ["You want purely creative visualisation work &mdash; look at Architecture &amp; Visualisation instead",
      "You want to stay entirely in analysis and calculation &mdash; Structural Engineering is the better path"],
     ["revit-architecture", "revit-structure", "revit-mep", "5d-bim-navisworks", "5d-bim"]),

    ("civil", "civil-infrastructure", "Civil &amp; Infrastructure Design",
     "Roads, corridors, terrain and quantities &mdash; designed digitally.",
     ["Infrastructure work is unforgiving about accuracy. A corridor design carries earthwork quantities that turn into real money, and a surface model that is wrong is wrong all the way to site.",
      "This path moves you from 2D drafting into 3D corridor modelling and quantity extraction &mdash; the skills that infrastructure consultancies and contractors actively recruit for. You will work with survey data, build surfaces, set out alignments and profiles, and produce the quantities a contractor prices from.",
      "If you like work where the answer is either right or demonstrably wrong, this suits you."],
     ["AutoCAD Civil", "Surfaces &amp; terrain", "Alignments &amp; profiles", "Corridor modelling", "Quantity take-off", "Civil 3D live project"],
     [("Civil Design Engineer", "Produce design drawings and models for infrastructure schemes"),
      ("Highway Design Engineer", "Set out alignments, profiles and corridor geometry"),
      ("Quantity Engineer", "Extract and verify quantities from the model"),
      ("Site Design Coordinator", "Bridge design intent and site execution")],
     ["A civil engineering student or graduate", "A site engineer wanting design-office skills",
      "A draughtsperson working on infrastructure schemes", "Targeting infrastructure consultancies or EPC contractors"],
     ["You are drawn to buildings rather than infrastructure &mdash; BIM is the better path",
      "You want analysis and calculation as the core of your work &mdash; see Structural Engineering"],
     ["autocad-civil", "civil-3d", "staad-pro"]),

    ("arch", "architecture-visualisation", "Architecture &amp; Visualisation",
     "From concept model to a render a client will believe.",
     ["Visualisation is persuasion. The model has to be right, but the image has to make somebody feel something about a building that does not exist yet.",
      "This path builds both halves &mdash; accurate modelling, and the lighting, material and rendering craft that turns it into work a practice can present to a client. You will learn where realism matters and where it is wasted effort.",
      "It suits people who already have design sense and want the technical craft to express it."],
     ["SketchUp / Revit", "Materials &amp; lighting", "V-Ray", "Lumion", "3ds Max", "Portfolio project"],
     [("Architectural Designer", "Take a design from concept model to coordinated output"),
      ("3D Visualiser", "Produce presentation imagery and walkthroughs"),
      ("Design Technician", "Support a practice with modelling and documentation"),
      ("Interior Visualiser", "Model and render interior schemes")],
     ["An architecture student or graduate", "An interior designer wanting stronger output",
      "A designer whose portfolio needs presentation quality", "Someone aiming at design-practice or visualisation-studio work"],
     ["You want coordination and data rather than imagery &mdash; BIM is the better path",
      "You want engineering analysis &mdash; see Structural Engineering"],
     ["sketchup", "v-ray", "lumion", "3ds-max", "revit-architecture"]),

    ("mech", "mechanical-product-design", "Mechanical &amp; Product Design",
     "Take a product from sketch to a manufacturable assembly.",
     ["Product design is where a drawing has to survive contact with a machine shop. A model that looks right and cannot be made is a failed design.",
      "This path teaches parametric modelling, assemblies, and the tolerancing language that makes a design manufacturable &mdash; then puts a printed prototype of your own part in your hand so you find out what your design got wrong.",
      "The manufacturing belt around Gurugram, Manesar and Bhiwadi runs on exactly this skill set."],
     ["AutoCAD Mechanical", "SolidWorks", "Assemblies", "GD&amp;T", "CATIA / NX CAD", "3D printed prototype"],
     [("Design Engineer", "Model parts and assemblies to a manufacturable standard"),
      ("Product Design Engineer", "Own a product from concept through to production drawings"),
      ("CAD Engineer", "Produce and maintain the design data a manufacturer works from"),
      ("Detailing Engineer", "Produce dimensioned, toleranced drawing sets")],
     ["A mechanical engineering student or graduate", "A production or quality engineer moving into design",
      "A draughtsperson wanting 3D and tolerancing skills", "Targeting automotive, machine-building or product firms"],
     ["You want simulation as your primary work &mdash; look at the analysis programmes within this path",
      "You are focused on buildings rather than products &mdash; see BIM"],
     ["solidworks", "catia", "creo", "nx-cad", "gdt", "autodesk-inventor", "3d-printing", "autocad-mechanical", "autocad-3d", "ansys-fluent"]),

    ("struct", "structural-engineering", "Structural Engineering &amp; Analysis",
     "Model it, analyse it, and prove it stands up.",
     ["This path is for engineers who want the calculation as well as the geometry. You will model structures, apply loads, run analysis, interpret results against codes, and produce the detailing that a site can actually build from.",
      "Analysis without detailing is academic; detailing without analysis is guesswork. The roles that pay well need both, which is why this path keeps them together.",
      "It suits people who are comfortable being the person who has to justify a number."],
     ["AutoCAD", "Structural modelling", "STAAD.Pro", "ETABS", "Load cases &amp; code checks", "Revit Structure detailing"],
     [("Structural Design Engineer", "Design and verify structural systems against codes"),
      ("Analysis Engineer", "Build analysis models and interpret results"),
      ("Detailing Engineer", "Produce construction-ready structural drawings"),
      ("Structural BIM Engineer", "Own the structural model within a BIM workflow")],
     ["A civil or structural engineering graduate", "A design-office engineer wanting software depth",
      "Someone targeting consultancy rather than site work", "An engineer aiming at Gulf structural roles"],
     ["You prefer coordination and information management &mdash; BIM is the better path",
      "You want product rather than building structures &mdash; see Mechanical &amp; Product Design"],
     ["staad-pro", "etabs", "revit-structure", "ansys", "ansys-workbench", "nx-nastran"]),

    ("mep", "electrical-mep", "Electrical &amp; MEP Design",
     "The systems that make a building work.",
     ["Every building runs on services that nobody notices until they fail. MEP design is a high-demand and chronically under-supplied discipline &mdash; MEP coordinators in particular are among the hardest roles for firms to fill.",
      "This path covers electrical schematics and panel design, then moves into modelling building services in Revit MEP and coordinating them against architecture and structure.",
      "If you want a discipline where demand consistently outstrips supply, this is it."],
     ["AutoCAD Electrical", "Schematics &amp; panels", "Revit MEP", "Services coordination", "Navisworks clash detection"],
     [("MEP Design Engineer", "Design and model building services"),
      ("Electrical Design Engineer", "Produce schematics, panel layouts and control documentation"),
      ("Panel Design Engineer", "Design and document control and distribution panels"),
      ("MEP BIM Coordinator", "Coordinate services against architecture and structure")],
     ["An electrical or mechanical engineering graduate", "A site services engineer moving into design",
      "An automation or controls technician", "Targeting MEP consultancies or contractors"],
     ["You want architectural or structural work &mdash; see BIM or Structural Engineering",
      "You want product design &mdash; see Mechanical &amp; Product Design"],
     ["autocad-electrical", "revit-mep", "pc-schematic", "automation-cad"]),

    ("pm", "project-management", "Project Planning &amp; Management",
     "Plan the schedule, hold the cost, deliver the project.",
     ["Technical skill gets a project designed. Planning gets it delivered. This path suits engineers who find themselves drawn to sequencing, cost and coordination rather than to modelling.",
      "You will build work breakdown structures, activity networks, critical paths, resource and cost loading, and progress reporting against a baseline &mdash; the actual deliverables a planning engineer produces.",
      "Planning experience compounds into seniority faster than most technical routes, and Gulf EPC contractors hire for it continuously."],
     ["PM fundamentals", "MS Project", "Primavera P6", "Cost &amp; resource loading", "4D / 5D concepts", "Planning project"],
     [("Planning Engineer", "Build and maintain the project schedule"),
      ("Project Coordinator", "Coordinate delivery across disciplines and contractors"),
      ("Cost Engineer", "Track budget, commitment and variance"),
      ("Project Control Engineer", "Own schedule, cost and reporting together")],
     ["An engineer of any discipline drawn to delivery", "A site engineer wanting an office-based progression",
      "A professional targeting Gulf EPC or infrastructure roles", "Someone who wants seniority to scale with experience"],
     ["You want to stay hands-on with design software &mdash; any of the technical paths suit better"],
     ["primavera-ppm", "ms-project-ppm"]),

    ("ai", "ai-emerging-technologies", "AI &amp; Emerging Engineering Tech",
     "Automation, generative design and AI-assisted engineering workflows.",
     ["The engineering software you will use in five years will do more of the repetitive work for you. The people who benefit are the ones who understand the workflow well enough to automate it.",
      "This path layers automation and AI-assisted techniques onto a solid design foundation. It is deliberately not a replacement for learning the fundamentals &mdash; automation applied to a workflow you do not understand produces errors faster, not results.",
      "CADD Centre's national portfolio now includes AI-enabled programmes. The exact programmes this centre is authorised to deliver are being confirmed, and we will state them precisely rather than imply them."],
     ["A core design skill first", "Design automation concepts", "Parametric &amp; generative approaches", "AI-assisted productivity workflows", "Applied project"],
     [("Design Automation Specialist", "Automate repetitive modelling and documentation tasks"),
      ("BIM Technologist", "Build and maintain automated BIM workflows"),
      ("Computational Design Assistant", "Apply parametric and generative methods to design problems")],
     ["Someone who already has a core CAD or BIM skill", "An engineer whose work involves heavy repetition",
      "A professional wanting to stay ahead of workflow change"],
     ["You have no design software foundation yet &mdash; start with a core path first. Automation on top of nothing is not a career"],
     ["3d-printing"]),
]

# ---------------------------------------------------------------------------
# PROGRAMMES — every live course page plus the master programmes
# slug, name, category, path key, tier, duration, software, headline tail,
# deliverable, modules[(title, [bullets])], roles[], careers paragraph,
# legacy URLs to 301
# ---------------------------------------------------------------------------
def _m(*pairs):
    return list(pairs)


PROGRAMS = [
    # ---------------- AEC ----------------
    ("revit-architecture", "Revit Architecture", "AEC", "bim", "Short-term", "Approx. 60 hours", "Revit",
     "Learn how buildings are designed in BIM",
     "A complete multi-storey building model &mdash; levels, grids, walls, floors, roofs, curtain systems, stairs and custom families &mdash; taken through to a coordinated drawing set with schedules and quantities extracted from the model itself.",
     _m(("Project setup", ["Templates, levels and grids", "The BIM way of thinking about a building", "Project browser and view organisation"]),
        ("Building the envelope", ["Walls, compound structures and layers", "Floors and floor systems", "Roofs, ceilings and voids"]),
        ("Openings and components", ["Doors and windows", "Joinery and fixed furniture", "Component placement and constraints"]),
        ("Complex geometry", ["Curtain walls, grids and mullions", "Stairs and ramps", "Railings and balustrades"]),
        ("Site and context", ["Topography and toposurfaces", "Site components and grading", "Building pads"]),
        ("Families", ["Family editor fundamentals", "Parametric family creation", "Nested and shared families"]),
        ("Documentation", ["Schedules and quantities", "Sheets, titleblocks and revisions", "Annotation and dimensioning"]),
        ("Collaboration", ["Worksharing and worksets", "Central and local models", "Linked models and coordination"]),
        ("Live project", ["A full building from setup to issued drawing set", "Portfolio-ready deliverable", "Review and critique"])),
     ["BIM Modeller", "Revit Technician", "Architectural Designer", "Documentation Assistant"],
     "Revit is now a baseline requirement rather than a differentiator in architectural practice &mdash; which means not having it closes doors, and having it opens the first one. The roles that pay well are the ones above pure modelling: coordination, documentation management, and discipline ownership.",
     ["/courses/revit-architecture/", "/revit-architecture/"]),

    ("revit-structure", "Revit Structure", "AEC", "struct", "Short-term", "Approx. 60 hours", "Revit",
     "Learn how structures get modelled, detailed and built",
     "A structural model of a multi-storey frame &mdash; grids, columns, beams, slabs and foundations &mdash; coordinated against an architectural model and issued as construction-ready structural drawings.",
     _m(("Structural setup", ["Grids, levels and datums", "Structural templates", "Discipline view organisation"]),
        ("Framing", ["Columns and structural walls", "Beams, beam systems and bracing", "Slabs and floor systems"]),
        ("Foundations", ["Isolated and strip footings", "Pile caps and mats", "Foundation detailing"]),
        ("Reinforcement and detailing", ["Rebar concepts in Revit", "Section and callout detailing", "Structural annotation"]),
        ("Coordination", ["Linking architectural models", "Copy/monitor workflows", "Interference checking"]),
        ("Documentation", ["Structural schedules", "Sheets and drawing issue", "Construction-ready output"])),
     ["Structural BIM Engineer", "Revit Structure Technician", "Detailing Engineer"],
     "Structural detailing in BIM sits at the junction of analysis and construction. Consultancies need people who can take an analysis result and turn it into something a site can build, and that combination is harder to hire for than either skill alone.",
     ["/courses/revit-structure/", "/revit-structure/"]),

    ("revit-mep", "Revit MEP", "AEC", "mep", "Short-term", "Approx. 60 hours", "Revit",
     "Learn how building services actually get coordinated",
     "A coordinated services model &mdash; HVAC ductwork, plumbing and electrical systems routed through a building and clash-checked against architecture and structure.",
     _m(("MEP setup", ["MEP templates and view discipline", "Systems and system types", "Spaces and zones"]),
        ("Mechanical", ["Ductwork layout and sizing", "Air terminals and equipment", "HVAC system logic"]),
        ("Plumbing", ["Pipe systems and routing", "Fixtures and connections", "Sanitary and supply layouts"]),
        ("Electrical", ["Circuits, panels and distribution", "Lighting layouts", "Cable trays and containment"]),
        ("Coordination", ["Linking architectural and structural models", "Interference checks", "Resolving service routes"]),
        ("Documentation", ["Schedules and equipment lists", "Sheets and issue", "Annotation standards"])),
     ["MEP Design Engineer", "Revit MEP Technician", "MEP BIM Coordinator"],
     "MEP is the discipline firms struggle hardest to staff. Services routing is where most coordination problems on a project originate, so people who can model services properly and resolve conflicts are disproportionately valuable.",
     ["/courses/revit-mep/", "/revit-mep/"]),

    ("civil-3d", "Civil 3D", "AEC", "civil", "Professional", "Approx. 80 hours", "Civil 3D",
     "Learn how infrastructure gets designed and quantified",
     "A complete corridor design &mdash; existing ground surface from survey data, horizontal alignment, vertical profile, assembly and corridor model, with earthwork quantities extracted and a drawing set produced.",
     _m(("Survey and surfaces", ["Importing and managing survey data", "Building and editing surfaces", "Surface analysis and display"]),
        ("Alignments", ["Horizontal alignment design", "Design criteria and constraints", "Alignment labelling"]),
        ("Profiles", ["Existing ground profiles", "Vertical design profiles", "Profile views and annotation"]),
        ("Corridors", ["Assemblies and subassemblies", "Corridor creation and targets", "Corridor surfaces"]),
        ("Quantities", ["Sample lines and sections", "Material lists and earthwork volumes", "Quantity take-off reporting"]),
        ("Output", ["Plan and profile sheets", "Section sheets", "Drawing production"])),
     ["Civil Design Engineer", "Highway Design Engineer", "Quantity Engineer"],
     "Corridor modelling with reliable quantity extraction is the specific capability infrastructure consultancies and contractors recruit for. Earthwork quantities carry direct commercial consequence, which is why accuracy here is valued more than speed.",
     ["/courses/civil-3d/", "/civil-3d/"]),

    ("autocad-civil", "AutoCAD Civil", "AEC", "civil", "Short-term", "Approx. 50 hours", "AutoCAD",
     "Learn the drafting discipline infrastructure work depends on",
     "A complete set of civil drawings &mdash; site plans, layouts, sections and details &mdash; drafted to a consistent standard with correct layering, annotation and sheet setup.",
     _m(("Drawing fundamentals", ["Interface, coordinates and units", "Draw and modify commands", "Precision drafting with snaps and tracking"]),
        ("Organisation", ["Layers, linetypes and standards", "Blocks and attributes", "External references"]),
        ("Civil drafting", ["Site and plot layouts", "Sections and details", "Levels and contours in 2D"]),
        ("Annotation", ["Dimensioning styles", "Text and leaders", "Tables and schedules"]),
        ("Output", ["Layouts and viewports", "Plot styles and scales", "Sheet set production"])),
     ["Civil Draughtsperson", "CAD Technician", "Junior Design Engineer"],
     "AutoCAD remains the working language of most civil drawing offices, and it is the foundation the 3D tools sit on top of. It is rarely the destination, but it is almost always the entry point.",
     ["/autocad/autocad-civil/", "/autocad-civil/"]),

    ("staad-pro", "STAAD.Pro", "AEC", "struct", "Professional", "Approx. 60 hours", "STAAD.Pro",
     "Learn how a structure is proven, not just drawn",
     "A complete structural analysis &mdash; a modelled frame with loads applied, load combinations built, analysis run, results interpreted against code, and member design verified.",
     _m(("Modelling", ["Geometry, nodes and members", "Properties and material definitions", "Supports and releases"]),
        ("Loading", ["Load types and load cases", "Load combinations to code", "Wind and seismic load application"]),
        ("Analysis", ["Running linear static analysis", "Interpreting deflection and forces", "Diagnosing model errors"]),
        ("Design", ["Steel design and code checks", "Concrete design parameters", "Member optimisation"]),
        ("Reporting", ["Result extraction", "Design reports", "Presenting analysis output"])),
     ["Structural Analysis Engineer", "Structural Design Engineer", "Detailing Engineer"],
     "Analysis software is only as good as the engineer driving it, and employers test for that in interviews. This programme spends deliberate time on interpreting results and spotting a model that is wrong &mdash; which is the part that separates a competent analyst from someone who can operate the software.",
     ["/courses/staad-pro/", "/staad-pro/"]),

    ("etabs", "ETABS (CSI)", "AEC", "struct", "Professional", "Approx. 60 hours", "ETABS",
     "Learn how buildings are analysed as complete systems",
     "A full building analysis model &mdash; storeys, framing, shear walls and diaphragms &mdash; with gravity, wind and seismic loading applied and results interpreted for design.",
     _m(("Building modelling", ["Storey definition and grids", "Frames, walls and diaphragms", "Section and material properties"]),
        ("Loading", ["Gravity load patterns", "Wind load application", "Seismic definitions and response spectra"]),
        ("Analysis", ["Modal analysis", "Storey drift and displacement checks", "Result interpretation"]),
        ("Design", ["Concrete frame design", "Shear wall design", "Code compliance checking"]),
        ("Output", ["Design reports", "Detailing output", "Model documentation"])),
     ["Structural Design Engineer", "Building Analysis Engineer", "Seismic Design Engineer"],
     "ETABS is the standard for building analysis in most Indian consultancies. Seismic and drift checking in particular are routine requirements, so competence here maps directly onto day-one usefulness in a design office.",
     ["/courses/etabs-csi/", "/etabs-csi/"]),

    ("5d-bim", "5D BIM", "AEC", "bim", "Professional", "Approx. 70 hours", "BIM &middot; Navisworks",
     "Learn how time and cost attach to a model",
     "A 5D model &mdash; a federated building model linked to a construction programme and a cost dataset, producing a sequenced simulation and cost-loaded output.",
     _m(("BIM dimensions", ["3D, 4D and 5D explained", "What data has to exist for each", "Information requirements"]),
        ("Model federation", ["Combining discipline models", "Model hygiene and naming", "Clash detection basics"]),
        ("4D sequencing", ["Linking programme activities to model elements", "Construction simulation", "Sequence review"]),
        ("5D cost", ["Quantity extraction from the model", "Cost data linkage", "Cost-loaded reporting"]),
        ("Applied project", ["A full 4D/5D exercise", "Presenting the simulation", "Reviewing accuracy"])),
     ["BIM Coordinator", "4D Planner", "Cost/BIM Engineer"],
     "4D and 5D work sits between the design office and the commercial team, and very few people are comfortable in both. That overlap is precisely why the roles are hard to fill and why they progress quickly.",
     ["/courses/5d-bim/", "/5d-bim/"]),

    ("5d-bim-navisworks", "5D BIM using Navisworks", "AEC", "bim", "Professional", "Approx. 60 hours", "Navisworks",
     "Learn how coordination and clash detection actually run",
     "A federated multi-discipline model with a complete clash detection workflow &mdash; clash tests configured, results grouped and prioritised, and a coordination report issued.",
     _m(("Navisworks fundamentals", ["Appending and federating models", "Navigation and selection trees", "Model hygiene"]),
        ("Clash detection", ["Setting up clash tests", "Rules, tolerances and exclusions", "Grouping and prioritising results"]),
        ("Coordination workflow", ["Running a coordination review", "Assigning and tracking issues", "Reporting to disciplines"]),
        ("4D simulation", ["TimeLiner and programme linkage", "Construction sequencing", "Simulation output"]),
        ("Quantification", ["Quantity take-off in Navisworks", "Cost linkage", "Reporting"])),
     ["BIM Coordinator", "Clash Detection Engineer", "4D Planner"],
     "Clash detection is where BIM proves its commercial value, and running a coordination meeting well is a genuinely distinct skill. This is the programme that moves people from modelling into coordination.",
     ["/5d-bim-using-navisworks/", "/courses/5d-bim-using-navisworks/"]),

    ("sketchup", "SketchUp", "AEC", "arch", "Short-term", "Approx. 40 hours", "SketchUp",
     "Learn to think through a design in three dimensions, fast",
     "A fully modelled building or interior scheme with materials applied, presented as a set of views suitable for a client conversation.",
     _m(("Modelling fundamentals", ["Interface and inference system", "Push/pull and geometry creation", "Groups and components"]),
        ("Building a scheme", ["Modelling from plans", "Site and context", "Interiors and detail"]),
        ("Materials and styles", ["Material application and mapping", "Styles and edge treatment", "Scenes and views"]),
        ("Extensions", ["Useful extension workflows", "Efficiency techniques", "File management"]),
        ("Presentation", ["Layout and sheets", "Export workflows", "Handing off to a render engine"])),
     ["Architectural Designer", "Interior Designer", "Design Technician"],
     "SketchUp is the fastest way to get an idea into three dimensions, which is why practices use it at concept stage even when they document in Revit. It also feeds directly into V-Ray and Lumion, so it is a natural first step on the visualisation path.",
     ["/courses/sketchup/", "/sketchup/"]),

    ("v-ray", "V-Ray", "AEC", "arch", "Short-term", "Approx. 40 hours", "V-Ray",
     "Learn what makes a render believable",
     "A photorealistic interior and exterior render set &mdash; lit, materialled and post-processed to a standard a practice could put in front of a client.",
     _m(("Render fundamentals", ["How a render engine works", "Camera and exposure", "Quality versus time"]),
        ("Lighting", ["Natural and artificial lighting", "HDRI and environment", "Interior lighting strategy"]),
        ("Materials", ["Material anatomy and layering", "Reflection, refraction and roughness", "Texture mapping"]),
        ("Output", ["Render settings and passes", "Denoising and optimisation", "Post-processing"])),
     ["3D Visualiser", "Architectural Visualiser", "Design Technician"],
     "Rendering is judged instantly and subjectively, which makes it unusually portfolio-driven. What gets people hired here is a small number of genuinely convincing images, not a long list of software.",
     ["/courses/v-ray/", "/v-ray/"]),

    ("lumion", "Lumion", "AEC", "arch", "Short-term", "Approx. 30 hours", "Lumion",
     "Learn to present a building in motion",
     "An animated walkthrough of a building in a full environment &mdash; landscaped, populated, lit for time of day, and rendered to video.",
     _m(("Environment", ["Importing models", "Terrain and landscaping", "Weather and time of day"]),
        ("Materials and population", ["Material assignment", "People, vehicles and vegetation", "Scene composition"]),
        ("Animation", ["Camera paths and keyframes", "Movement and effects", "Timeline control"]),
        ("Output", ["Still and video output", "Quality settings", "Presentation packaging"])),
     ["3D Visualiser", "Architectural Presenter", "Design Technician"],
     "Lumion trades absolute realism for speed, which is exactly the right trade for client presentations and competition submissions where turnaround matters more than perfection.",
     ["/courses/lumion/", "/lumion/"]),

    ("3ds-max", "3ds Max for Engineers", "AEC", "arch", "Short-term", "Approx. 60 hours", "3ds Max",
     "Learn modelling and rendering with full control",
     "A rendered architectural scene modelled and lit from scratch, demonstrating control over geometry, materials and lighting that automated tools do not give you.",
     _m(("Modelling", ["Primitives and modifiers", "Poly modelling", "Architectural modelling workflows"]),
        ("Materials", ["Material editor", "Mapping and UVs", "Realistic material setup"]),
        ("Lighting and cameras", ["Lighting types and strategy", "Camera setup and composition", "Exposure control"]),
        ("Rendering", ["Render engines and settings", "Render passes", "Output and post-processing"]),
        ("Animation basics", ["Camera animation", "Walkthrough setup", "Video output"])),
     ["3D Visualiser", "Architectural Modeller", "Visualisation Artist"],
     "3ds Max gives more control than the faster tools, and studios doing high-end visualisation still expect it. It suits people who want depth in imagery rather than breadth across the design process.",
     ["/courses/3ds-max-course-for-engineers/", "/3ds-max-max-for-engineers/"]),

    # ---------------- Mechanical ----------------
    ("solidworks", "SolidWorks", "Mechanical", "mech", "Professional", "Approx. 80 hours", "SolidWorks &middot; GD&amp;T",
     "Learn how a product gets manufactured",
     "A complete mechanical assembly &mdash; modelled as individual parts, assembled with correct mates, checked for interference, dimensioned and toleranced to a manufacturable standard, and issued as a full drawing set. Where the part suits it, you will 3D print a component.",
     _m(("Sketching", ["Sketch entities and relations", "Fully defined sketches", "Design intent"]),
        ("Part modelling", ["Extrude, revolve, sweep, loft", "Fillets, chamfers and draft", "Patterns and mirrors"]),
        ("Advanced features", ["Configurations and design tables", "Multibody techniques", "Surfacing fundamentals"]),
        ("Assemblies", ["Mates and degrees of freedom", "Subassemblies", "Interference and collision detection"]),
        ("Drawings", ["Views, sections and details", "Dimensioning standards", "Bill of materials"]),
        ("Tolerancing", ["GD&amp;T fundamentals", "Datums and feature control frames", "Fit and function"]),
        ("Sheet metal and weldments", ["Sheet metal features and flat patterns", "Weldment structures", "Manufacturing considerations"]),
        ("Applied project", ["Full assembly from brief to drawing set", "Prototype where suitable", "Design review"])),
     ["Design Engineer", "Product Design Engineer", "CAD Engineer", "Detailing Engineer"],
     "The manufacturing belt around Gurugram, Manesar and Bhiwadi runs on exactly this skill set. Automotive component suppliers, machine builders and product firms all need engineers who can model a part and then produce a drawing a shop floor can work from. The drawing matters as much as the model, which is why GD&amp;T sits inside this programme rather than beside it.",
     ["/courses/solid-works/", "/solid-works/"]),

    ("catia", "CATIA", "Mechanical", "mech", "Professional", "Approx. 80 hours", "CATIA",
     "Learn the platform automotive and aerospace design runs on",
     "A surfaced product model with a full assembly and drawing set, built using the workbenches automotive and aerospace suppliers actually use.",
     _m(("Sketcher", ["Constraints and design intent", "Sketch analysis", "Profile creation"]),
        ("Part design", ["Solid features", "Dress-up features", "Transformation and patterns"]),
        ("Surface design", ["Wireframe geometry", "Surface creation and joining", "Surface to solid workflows"]),
        ("Assembly design", ["Constraints and product structure", "Assembly analysis", "Large assembly handling"]),
        ("Drafting", ["Views and sections", "Dimensioning and annotation", "Drawing standards"])),
     ["Design Engineer", "Surface Modeller", "Automotive CAD Engineer"],
     "CATIA is entrenched in automotive and aerospace supply chains, and surfacing skill in particular is scarce. Employers in those sectors frequently specify it by name, which makes it a targeted rather than a general choice.",
     ["/courses/catia/", "/catia/"]),

    ("creo", "Creo Parametric", "Mechanical", "mech", "Short-term", "Approx. 60 hours", "Creo",
     "Learn parametric product modelling properly",
     "A parametric product assembly with configurations, built so that a change to a driving dimension updates cleanly through the whole model and its drawings.",
     _m(("Sketching and datums", ["Datum planes, axes and points", "Sketcher and constraints", "Parent-child relationships"]),
        ("Part modelling", ["Extrude, revolve, sweep, blend", "Engineering features", "Patterns and family tables"]),
        ("Assemblies", ["Component placement and constraints", "Assembly structure", "Interference checking"]),
        ("Drawings", ["Views and sections", "Dimensioning and tolerancing", "Drawing formats"])),
     ["Design Engineer", "Product Engineer", "CAD Engineer"],
     "Creo's strength is genuine parametric control, and firms that use it care about model robustness &mdash; whether a design updates cleanly when a dimension changes. That discipline transfers to every other CAD platform you will use.",
     ["/courses/creo/", "/creo/"]),

    ("nx-cad", "NX CAD", "Mechanical", "mech", "Short-term", "Approx. 60 hours", "NX CAD",
     "Learn industrial-grade modelling",
     "A complete product model and assembly built in NX, with drawings produced to industrial documentation standards.",
     _m(("Modelling", ["Sketching and constraints", "Feature-based modelling", "Synchronous modelling"]),
        ("Freeform", ["Surface creation", "Freeform shaping", "Surface analysis"]),
        ("Assemblies", ["Assembly navigator and structure", "Constraints and arrangements", "Large assembly performance"]),
        ("Drafting", ["Drawing views and sections", "Dimensioning and GD&amp;T", "Drawing output"])),
     ["Design Engineer", "CAD Engineer", "Product Development Engineer"],
     "NX is the platform of choice in a number of large automotive and industrial engineering organisations. Its synchronous modelling approach is genuinely different from history-based CAD, and that flexibility is a useful thing to have seen.",
     ["/courses/nx-cad/", "/nx-cad/"]),

    ("ansys", "Ansys", "Mechanical", "struct", "Professional", "Approx. 60 hours", "Ansys",
     "Learn to simulate before you commit to steel",
     "A completed finite element analysis &mdash; geometry prepared, meshed, loaded, solved and interpreted, with results validated against expectation rather than accepted blindly.",
     _m(("FEA fundamentals", ["What FEA does and where it fails", "Element types", "Idealisation and assumptions"]),
        ("Pre-processing", ["Geometry preparation", "Meshing strategy and quality", "Contacts and connections"]),
        ("Loading and constraints", ["Boundary conditions", "Load application", "Common modelling errors"]),
        ("Solving and results", ["Static structural analysis", "Stress and deformation interpretation", "Convergence and validation"]),
        ("Reporting", ["Presenting simulation results", "Justifying assumptions", "Report structure"])),
     ["Simulation Engineer", "FEA Analyst", "Design Verification Engineer"],
     "Simulation is easy to run and hard to trust. Employers screen for whether a candidate can explain why a result is believable, so this programme deliberately spends time on validation and on recognising a bad model.",
     ["/courses/ansys/", "/ansys/"]),

    ("ansys-workbench", "Ansys Workbench", "Mechanical", "struct", "Professional", "Approx. 60 hours", "Ansys Workbench",
     "Learn the simulation environment engineering teams actually use",
     "A multi-step analysis project built in the Workbench environment, with parameterised geometry and a documented result set.",
     _m(("Workbench environment", ["Project schematic and workflow", "Data linking between systems", "Parameter management"]),
        ("Geometry and meshing", ["DesignModeler and SpaceClaim basics", "Mesh controls and quality metrics", "Mesh independence"]),
        ("Analysis systems", ["Static structural", "Modal analysis", "Thermal analysis introduction"]),
        ("Results", ["Post-processing", "Parametric studies", "Reporting"])),
     ["Simulation Engineer", "FEA Analyst", "Design Engineer"],
     "Workbench is how simulation is organised in practice &mdash; linked systems, parameter sweeps and repeatable studies rather than isolated one-off runs. That workflow discipline is what makes simulation useful to a design team.",
     ["/ansys-workbench/", "/courses/ansys-workbench/"]),

    ("ansys-fluent", "Ansys Fluent", "Mechanical", "mech", "Professional", "Approx. 60 hours", "Ansys Fluent",
     "Learn to analyse how fluids and heat actually behave",
     "A completed CFD study &mdash; a flow domain meshed, boundary conditions set, solution converged, and results interpreted with an honest assessment of confidence.",
     _m(("CFD fundamentals", ["Governing principles without the maths overload", "Where CFD is reliable and where it is not", "Domain definition"]),
        ("Meshing", ["Mesh strategy for flow", "Boundary layer resolution", "Mesh quality checks"]),
        ("Setup", ["Boundary conditions", "Turbulence model selection", "Material and operating conditions"]),
        ("Solving", ["Solver settings", "Convergence monitoring", "Diagnosing divergence"]),
        ("Post-processing", ["Contours, vectors and streamlines", "Quantitative extraction", "Result validation"])),
     ["CFD Engineer", "Thermal Analysis Engineer", "Simulation Engineer"],
     "CFD is a specialist route with fewer practitioners and correspondingly less competition. It suits engineers who are comfortable with uncertainty and willing to defend a result rather than just produce a colourful picture.",
     ["/courses/ansys-fluent/", "/ansys-fluent/"]),

    ("nx-nastran", "NX Nastran", "Mechanical", "struct", "Professional", "Approx. 50 hours", "NX Nastran",
     "Learn the solver behind serious structural analysis",
     "A validated Nastran analysis with a documented solution deck, results interpretation and a written justification of the modelling assumptions.",
     _m(("Nastran fundamentals", ["Solver architecture", "Solution sequences", "Input and output structure"]),
        ("Model preparation", ["Element selection", "Material and property definition", "Constraints and loads"]),
        ("Analysis types", ["Linear static", "Normal modes", "Buckling introduction"]),
        ("Results", ["Result interpretation", "Validation approaches", "Reporting"])),
     ["FEA Analyst", "Structural Simulation Engineer", "Design Verification Engineer"],
     "Nastran is a long-established solver used where analysis results carry certification weight. Understanding what the solver is doing, rather than just driving a front end, is what distinguishes an analyst from an operator.",
     ["/courses/nx-nastran/", "/nx-nastran/"]),

    ("autodesk-inventor", "Autodesk Inventor", "Mechanical", "mech", "Short-term", "Approx. 60 hours", "Inventor",
     "Learn mechanical design with manufacturing in mind",
     "A machine assembly modelled in Inventor with drawings, a bill of materials, and sheet metal and weldment components where appropriate.",
     _m(("Part modelling", ["Sketching and constraints", "Features and design intent", "Parameters"]),
        ("Assemblies", ["Constraints and joints", "Assembly structure", "Interference analysis"]),
        ("Sheet metal and frames", ["Sheet metal design and flat patterns", "Frame generator", "Weldments"]),
        ("Drawings", ["Views and sections", "Annotation and BOM", "Drawing standards"])),
     ["Design Engineer", "Machine Design Engineer", "CAD Engineer"],
     "Inventor is common in machine building and fabrication work, where sheet metal and structural frames are everyday requirements. It sits naturally alongside AutoCAD in firms that have grown from 2D drafting into 3D design.",
     ["/courses/autodesk-inventor/", "/autodesk-inventor/"]),

    ("gdt", "GD&amp;T", "Mechanical", "mech", "Short-term", "Approx. 30 hours", "GD&amp;T",
     "Learn the language that makes a drawing manufacturable",
     "A fully toleranced drawing set for a real component, with datums selected and justified, and feature control frames that a quality department could actually inspect against.",
     _m(("Why GD&amp;T exists", ["Limitations of coordinate tolerancing", "Function-driven tolerancing", "Cost of tolerance"]),
        ("Datums", ["Datum selection and reference frames", "Datum features and targets", "Sequence and precedence"]),
        ("Geometric controls", ["Form controls", "Orientation controls", "Location and profile controls"]),
        ("Material conditions", ["MMC, LMC and RFS", "Bonus tolerance", "Virtual condition"]),
        ("Application", ["Applying GD&amp;T to a real part", "Inspection implications", "Drawing review"])),
     ["Design Engineer", "Quality Engineer", "Detailing Engineer", "Inspection Engineer"],
     "GD&amp;T is the single most common gap between someone who can model and someone who can design for manufacture. It is also one of the few skills that makes a candidate immediately useful to both design and quality functions.",
     ["/courses/gdt-course/", "/gdt/"]),

    ("autocad-mechanical", "AutoCAD 2D &amp; 3D Mechanical", "Mechanical", "mech", "Short-term", "Approx. 50 hours", "AutoCAD",
     "Learn mechanical drafting to a professional standard",
     "A mechanical drawing set &mdash; parts, assemblies, sections and details &mdash; drafted with correct standards, annotation and a bill of materials.",
     _m(("Drafting fundamentals", ["Interface and precision drawing", "Draw and modify commands", "Coordinate systems"]),
        ("Mechanical drafting", ["Orthographic projection", "Sections and auxiliary views", "Standard parts libraries"]),
        ("3D modelling", ["Solid primitives and operations", "3D to 2D view generation", "Visual styles"]),
        ("Annotation", ["Dimensioning standards", "Tolerancing and surface finish", "Parts lists and BOM"]),
        ("Output", ["Layouts and plotting", "Drawing templates", "File standards"])),
     ["Mechanical Draughtsperson", "CAD Technician", "Design Assistant"],
     "AutoCAD is still the drafting baseline in a large number of Indian manufacturing and fabrication firms. Even in offices that model in 3D, the issued drawing is frequently AutoCAD, so competence here remains directly employable.",
     ["/autocad/autocad-2d-3d-mechanical/", "/autocad-2d-3d-mechanical/"]),

    ("autocad-3d", "AutoCAD 3D", "Hybrid", "mech", "Short-term", "Approx. 40 hours", "AutoCAD",
     "Learn to model and present in three dimensions",
     "A 3D model built in AutoCAD, taken through to generated 2D views, sections and a rendered presentation image.",
     _m(("3D fundamentals", ["3D coordinate systems and UCS", "Navigation and viewports", "Visual styles"]),
        ("Solid modelling", ["Primitives and boolean operations", "Extrude, revolve, sweep, loft", "Editing solids"]),
        ("Surfaces and meshes", ["Surface creation", "Mesh modelling basics", "Converting between types"]),
        ("Output", ["Generating 2D views from 3D", "Sections and details", "Basic rendering and materials"])),
     ["CAD Technician", "Design Assistant", "Draughtsperson"],
     "AutoCAD 3D is a practical extension for people already drafting in 2D who need occasional three-dimensional work without moving to a full parametric platform.",
     ["/autocad/autocad-3d/", "/autocad-3d/"]),

    ("3d-printing", "3D Printing &amp; Prototyping", "Hybrid", "mech", "Short-term", "Approx. 30 hours", "CAD &middot; FDM",
     "Learn what happens when your design becomes an object",
     "A physical printed part that you designed &mdash; modelled, checked for printability, sliced, printed, evaluated and revised based on what the first print got wrong.",
     _m(("Additive fundamentals", ["Additive versus subtractive manufacturing", "Process types and materials", "Where 3D printing is and is not appropriate"]),
        ("Design for additive", ["Wall thickness and feature size", "Overhangs and support strategy", "Orientation and anisotropy"]),
        ("Preparation", ["Exporting and repairing meshes", "Slicing software and parameters", "Infill, layers and speed"]),
        ("Printing and finishing", ["Running a print", "Diagnosing print failures", "Post-processing and finishing"]),
        ("Iterate", ["Evaluating the printed part", "Revising the design", "Second print and comparison"])),
     ["Product Design Engineer", "Prototyping Technician", "Design Engineer"],
     "The design-make-evaluate loop is how product engineers actually learn, and it is very difficult to replicate through a screen. This is also the programme that produces something you can put in an interviewer's hand.",
     ["/courses/3d-printing/", "/3d-printing/"]),

    # ---------------- Project Management ----------------
    ("primavera-ppm", "Primavera P6 with PPM", "Project Management", "pm", "Professional", "Approx. 60 hours", "Primavera P6",
     "Learn how projects get delivered on time",
     "A complete project schedule &mdash; work breakdown structure, activity network, resource and cost loading, baseline, and progress tracking with earned-value reporting against a realistic construction programme.",
     _m(("Project management fundamentals", ["Terminology and lifecycle", "Roles and responsibilities", "Planning principles"]),
        ("Structuring the project", ["Work breakdown structure", "Activity definition and coding", "Calendars"]),
        ("Building the schedule", ["Durations and relationships", "Critical path analysis", "Float and constraints"]),
        ("Resources and cost", ["Resource assignment", "Resource levelling", "Cost loading and budgets"]),
        ("Baseline and control", ["Baselining the programme", "Progress updating", "Variance analysis"]),
        ("Earned value", ["Earned value fundamentals", "Performance indices", "Forecasting"]),
        ("Reporting", ["Layouts and filters", "Standard reports", "Presenting to a client"])),
     ["Planning Engineer", "Project Control Engineer", "Cost Engineer", "Project Coordinator"],
     "Planning is one of the few engineering roles where experience compounds quickly into seniority and where international demand is consistent &mdash; Gulf infrastructure and EPC contractors hire planning engineers continuously. It suits people who are technically capable but more interested in sequence, cost and delivery than in geometry.",
     ["/courses/primavera-with-ppm/", "/primavera-with-ppm/"]),

    ("ms-project-ppm", "MS Project with PPM", "Project Management", "pm", "Short-term", "Approx. 40 hours", "MS Project",
     "Learn scheduling that a whole team can actually read",
     "A complete project plan with a resourced schedule, baseline and progress reporting, produced in the tool most organisations already have.",
     _m(("Fundamentals", ["Project management concepts", "MS Project interface", "Project setup and calendars"]),
        ("Scheduling", ["Task definition and durations", "Dependencies and constraints", "Critical path"]),
        ("Resources", ["Resource sheets and assignment", "Levelling and over-allocation", "Cost tracking"]),
        ("Tracking", ["Baselines", "Progress updates", "Variance and reporting"])),
     ["Project Coordinator", "Planning Assistant", "Project Administrator"],
     "MS Project is the pragmatic choice in organisations that are not running large EPC programmes. It is often the entry point into planning work, and it transfers conceptually to Primavera.",
     ["/courses/microsoft-office-with-ppm/", "/microsoft-office-with-ppm/"]),

    # ---------------- Electrical ----------------
    ("autocad-electrical", "AutoCAD Electrical", "Electrical", "mep", "Short-term", "Approx. 50 hours", "AutoCAD Electrical",
     "Learn to document control systems properly",
     "A complete control panel documentation set &mdash; schematics, panel layout, terminal and wire numbering, and automatically generated reports.",
     _m(("Environment", ["Project structure and drawing organisation", "Templates and standards", "Symbol libraries"]),
        ("Schematics", ["Ladder diagrams", "Component insertion and editing", "Wire numbering and cross-referencing"]),
        ("Panel layout", ["Footprint insertion", "Panel arrangement", "Terminal strips"]),
        ("PLC", ["PLC modules and I/O", "Address assignment", "I/O drawings"]),
        ("Reports", ["Bill of materials", "Wire and terminal reports", "Automated documentation"])),
     ["Electrical Design Engineer", "Panel Design Engineer", "Controls Documentation Engineer"],
     "Control panel documentation is a persistent requirement in manufacturing and automation, and it is work that has to be right &mdash; a wiring error found on site is expensive. Automated numbering and reporting is exactly the kind of capability employers notice.",
     ["/autocad/autocad-electrical/", "/autocad-electrical/"]),

    ("pc-schematic", "PC Schematic", "Electrical", "mep", "Short-term", "Approx. 40 hours", "PC Schematic",
     "Learn electrical documentation to European standards",
     "A complete electrical and automation documentation set produced to IEC-oriented standards, with lists and reports generated from the project data.",
     _m(("Project setup", ["Project structure", "Standards and templates", "Symbol databases"]),
        ("Schematics", ["Drawing electrical diagrams", "Component references", "Cross-referencing"]),
        ("Panel and layout", ["Mechanical layout", "Component placement", "Terminal planning"]),
        ("Documentation", ["Parts and component lists", "Terminal and cable lists", "Automatic report generation"])),
     ["Electrical Design Engineer", "Automation Documentation Engineer", "Panel Designer"],
     "PC Schematic is common in firms working to European standards or supplying European customers. It is a differentiator in exactly those companies, which tend to pay accordingly.",
     ["/courses/pc-schematic/", "/pc-schematic/"]),

    ("automation-cad", "Automation CAD", "Electrical", "mep", "Short-term", "Approx. 40 hours", "Automation CAD",
     "Learn to design and document industrial automation",
     "A documented industrial automation project covering control architecture, I/O schedules, schematics and panel documentation.",
     _m(("Automation fundamentals", ["Industrial control architecture", "Sensors, actuators and signals", "Control philosophy"]),
        ("System design", ["I/O listing and scheduling", "Control panel architecture", "Power and control distribution"]),
        ("Documentation", ["Schematic production", "Panel layouts", "Cable schedules"]),
        ("Project output", ["Standards compliance", "Report generation", "Handover documentation"])),
     ["Automation Design Engineer", "Controls Engineer", "Panel Design Engineer"],
     "Automation work sits between electrical design and process understanding. Firms commissioning production lines need people who can document a system well enough for somebody else to build and maintain it.",
     ["/courses/automation-cad/", "/automation-or-cad/"]),
]

# Master programmes — commercial bundles above the software layer
MASTERS = [
    ("master-bim", "Master Certificate in BIM", "AEC", "bim", "Master", "6&ndash;8 months",
     "Revit &middot; Navisworks &middot; AutoCAD &middot; Coordination",
     "Become a BIM coordinator, not just a modeller",
     "A full federated coordination project &mdash; multiple discipline models built, combined, clash-checked, reviewed and issued, with a complete drawing set and a portfolio presentation.",
     ["AutoCAD foundation", "Revit Architecture", "Revit Structure or MEP", "Navisworks coordination", "Live federated project", "Portfolio and interview preparation"],
     ["BIM Modeller", "BIM Engineer", "BIM Coordinator"],
     "The complete route from no BIM experience to a coordination-capable portfolio. This is the programme for people changing what they do, not adding a line to a CV."),
    ("master-product-design", "Master Certificate in Product Design", "Mechanical", "mech", "Master", "6&ndash;8 months",
     "SolidWorks &middot; CATIA &middot; GD&amp;T &middot; 3D printing",
     "Become a design engineer manufacturers can hire on day one",
     "A complete product development exercise &mdash; concept through parametric modelling, assembly, tolerancing, drawing set and a physical printed prototype.",
     ["AutoCAD Mechanical", "SolidWorks", "GD&amp;T", "CATIA or NX CAD", "3D printing and prototyping", "Portfolio and interview preparation"],
     ["Design Engineer", "Product Design Engineer", "CAD Engineer"],
     "Built around the manufacturing employers in the Gurugram, Manesar and Bhiwadi belt. Ends with a physical part you designed."),
    ("master-civil-structural", "Master Certificate in Civil &amp; Structural Design", "AEC", "struct", "Master", "6&ndash;8 months",
     "AutoCAD &middot; Civil 3D &middot; STAAD.Pro &middot; ETABS &middot; Revit",
     "Become an engineer who can design it and prove it",
     "A combined infrastructure and structural portfolio &mdash; a corridor design with quantities, plus a fully analysed and detailed structural frame.",
     ["AutoCAD Civil", "Civil 3D", "STAAD.Pro", "ETABS", "Revit Structure", "Portfolio and interview preparation"],
     ["Civil Design Engineer", "Structural Design Engineer", "Analysis Engineer"],
     "Covers both the geometry and the calculation, which is the combination consultancies most often struggle to hire."),
]

# Legacy URLs with no direct programme equivalent
EXTRA_REDIRECTS = [
    ("/bim/", "/career-paths/bim-digital-construction/", "Course hub maps to the career path"),
    ("/revit-architecture-structure-mep-training-certification-course/", "/programs/revit-architecture/", "Combined legacy page"),
    ("/our-courses/", "/programs/", "Index replaced by filterable programmes index"),
    ("/about-us/", "/about/", "About rewritten"),
    # /blog/ pointed at /insights/ until the section was renamed to News.
    # These now jump straight to the final URL rather than chaining through
    # /insights/ — a redirect chain loses a little link equity at every hop.
    ("/blog/", "/news/", "Blog becomes News"),
    ("/blog/autocad-basic-drawing-a-complete-guide/", "/news/autocad-basic-drawing-guide/", "Article migrated"),
    ("/blog/master-autocad-2d-mechanical-drawing/", "/news/autocad-2d-mechanical-drawing/", "Article migrated"),
    ("/insights/", "/news/", "Insights section renamed to News"),
    ("/privacy-policy/", "/privacy-policy/", "Retained"),
    ("/terms-conditions/", "/terms-conditions/", "Retained"),
    ("/disclaimer-page/", "/disclaimer/", "Slug normalised"),
    ("/contact/", "/contact/", "Retained"),
    ("/first-job-pakka/", "/careers/first-job-pakka/", "Promoted into the Careers section"),
    ("/thank-you/", "/contact/", "Legacy form thank-you page — replaced by the in-page reward screen"),
]


# ---------------------------------------------------------------------------
# CERTIFICATION LADDER — CADD Centre's actual commercial structure.
# Confirmed live on the course pages (e.g. /courses/civil-3d/). Every software
# is sold at three levels. The v1.1 build invented its own tier names and
# missed this entirely; this is the real product ladder.
# ---------------------------------------------------------------------------
CERT_LEVELS = [
    ("Proficient", "Core design and drafting skills. The working competence an employer expects on day one."),
    ("Masters", "Advanced modelling and project workflows. Depth beyond the basics, on real project structures."),
    ("Expert", "Complete project management and multidisciplinary collaboration skills."),
]

# ---------------------------------------------------------------------------
# ELIGIBILITY — the "Ideal For" block present on every live course page.
# Keyed by career path.
# ---------------------------------------------------------------------------
IDEAL_FOR = {
    "bim": ["Students pursuing or completed Civil Engineering or Architecture",
            "Diploma / ITI students in civil, architectural or drafting disciplines",
            "Working draughtspersons and site professionals moving into design",
            "Professionals targeting Gulf or European roles where BIM is mandated"],
    "civil": ["Students pursuing or completed Civil Engineering",
              "Diploma / ITI students in civil or surveying disciplines",
              "Professionals in infrastructure, transportation or land development",
              "Site engineers moving into a design office"],
    "arch": ["Students pursuing or completed Architecture or Interior Design",
             "Diploma students in architectural assistantship",
             "Designers who need presentation-quality output",
             "Professionals targeting design practices or visualisation studios"],
    "mech": ["Students pursuing or completed Mechanical, Automotive or Aeronautical Engineering",
             "Diploma / ITI students in mechanical or production disciplines",
             "Production and quality engineers moving into design",
             "Professionals in manufacturing, product development or tooling"],
    "struct": ["Students pursuing or completed Civil or Structural Engineering",
               "Diploma / ITI students in civil disciplines",
               "Design-office engineers wanting analysis depth",
               "Professionals in structural consultancy or construction"],
    "mep": ["Students pursuing or completed Electrical, Electronics or Automation Engineering",
            "Diploma / ITI students in electrical or industrial automation fields",
            "Professionals in control systems, industrial design or manufacturing",
            "Site services engineers moving into MEP design"],
    "pm": ["Engineering students and graduates of any discipline",
           "Site engineers seeking an office-based progression",
           "Professionals in construction, EPC or infrastructure delivery",
           "Anyone targeting planning or project-control roles"],
    "ai": ["Learners who already hold a core CAD or BIM skill",
           "Engineers whose work involves heavy repetition",
           "Professionals wanting to stay ahead of workflow change"],
}


# ---------------------------------------------------------------------------
# CLIENT-SUPPLIED RECORDS
# Empty until the centre provides verified data + written consent. Templates
# read these lists; when a list is empty the section renders an invitation to
# visit instead of a placeholder card. Nothing bracketed ever reaches a page.
# ---------------------------------------------------------------------------
TRAINERS = []   # {"name","role","experience","background","specialisms","photo"}
STORIES = []    # {"name","before","track","skills","role","employer","consent"}


# ---------------------------------------------------------------------------
# EMPLOYER / PARTNER LOGOS
# Populate ONLY with written permission from each named organisation. Showing
# a company's trademark under "trusted by" asserts a commercial relationship;
# doing so without permission is trademark misuse and, in India, an ASCI
# advertising-compliance exposure. Empty renders an honest alternative.
# ---------------------------------------------------------------------------
# (name, logo file under assets/img/logos/, intrinsic width, intrinsic height)
PARTNERS = [
    ("Larsen & Toubro",   "larsen_tourbro.png",         250,  250),
    ("AECOM",             "aecom-logo-dark.svg",        240,   55),
    ("TATA Projects",     "tata-projects.png",          176,   96),
    ("Havells",           "havells.png",               1280,  845),
    ("Wipro",             "Wipro_new_logo.svg.webp",   1280,  513),
    ("JLL",               "jll.png",                    281,  126),
    ("Godrej Properties", "godrej-properties.png",      381,   82),
]
# Written permission confirmed by the client for each name above.
# Keep the permission correspondence in the substantiation register; if any
# permission lapses, remove the name here and the band updates on rebuild.
# The band renders each logo white-on-dark; supply artwork on a transparent
# background, as the name stays only in the img alt text.


# ---------------------------------------------------------------------------
# ACCREDITATIONS — the authorisations shown on the home page.
#
# These are the strongest credential the centre has, so they get their own
# band directly under the statistics card. Each entry:
#
#   key        internal id, also the asset filename stem
#   awarding   the body that grants it, as it should read on screen
#   title      the EXACT programme name as printed on the certificate
#   note       one short line on what it means for a learner
#   logo       file under assets/img/logos/, or "" until artwork is supplied
#   logo_w/h   intrinsic pixel size of that artwork (prevents layout shift)
#   cert       certificate image under assets/img/certs/, or "" if not supplied
#   cert_w/h   intrinsic pixel size of the certificate image
#
# `title` must be copied verbatim from the certificate. Autodesk and PMI each
# run several tiers with similar names, and PMI retired "Registered Education
# Provider" in favour of "Authorized Training Partner" in 2021 — so the wrong
# label here is a false credential claim, not a typo. Both marks are also
# governed by their owners' brand guidelines: use the artwork they supply,
# unmodified, and only while the authorisation is current.
#
# An entry with no logo renders a neutral type-only tile rather than an
# invented lockup, and one with no certificate simply omits the view link, on
# the same principle as PARTNERS above: never show a credential we cannot
# substantiate.
# ---------------------------------------------------------------------------
ACCREDITATIONS = [
    {"key": "autodesk",
     "awarding": "Autodesk",
     # Exactly as printed on the certificate. Autodesk's programme name uses
     # US spelling — "Authorized Training Center" — even though the rest of
     # this site is written in British English. It is a proper name, not prose.
     "title": "Authorized Training Center",
     "note": "Autodesk's own standard for instructor-led training. Verified as an "
             "authorised ATC Site for delivery in India, covering AutoCAD, Revit, "
             "Civil 3D and Inventor.",
     "detail": "Site ID AP701381 &middot; Organisation ID OP701161",
     "valid": "Valid until 1 February 2027",
     "logo": "autodesk-atc.webp", "logo_w": 640, "logo_h": 187,
     "cert": "autodesk-atc-authorisation.webp", "cert_w": 1901, "cert_h": 1469},

    # PMI is held by the centre but no certificate has been supplied yet, so it
    # is not published: an entry with neither logo nor certificate is skipped by
    # accreditation_band(). Fill in the artwork and it appears on the next build.
    #
    # Confirm the exact programme name against the certificate before it goes
    # live. PMI retired "Registered Education Provider (R.E.P.)" in favour of
    # "Authorized Training Partner (ATP)" in 2021, and the two are different
    # credentials — the wrong label here is a false claim, not a typo.
    {"key": "pmi",
     "awarding": "PMI",
     "title": "Authorized Training Partner",     # TODO verify against certificate
     "note": "Project Management Institute authorisation covering PMP and CAPM "
             "preparation, taught against the current PMBOK guide.",
     "detail": "",
     "valid": "",
     "logo": "", "logo_w": 0, "logo_h": 0,
     "cert": "", "cert_w": 0, "cert_h": 0},
]
