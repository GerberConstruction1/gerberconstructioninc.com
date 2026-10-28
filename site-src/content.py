# Site content for gerberconstructioninc.com — edit here, then run build.py
# Every photo slot names the Dropbox file (or shoot) that belongs there.

SITE = {
    "name": "Gerber Construction Inc.",
    "phone": "(860) 875-6684",
    "phone_href": "tel:+18608756684",
    "address1": "1 Nutmeg Drive",
    "address2": "Ellington, CT 06029",
    "maps": "https://www.google.com/maps/search/?api=1&query=1+Nutmeg+Drive+Ellington+CT+06029",
    "email_pricing": "estimating@gerber.build",
    "email_general": "office@gerberconstructioninc.com",
    "form_key": "86dfe7fe-8064-406e-ab9f-1ae17527dfd5",  # Web3Forms access key for office@ (submissions are emailed there). Empty = form shows the fallback note.
    "careers": "https://careers.gerber.build",
    "instagram": "https://www.instagram.com/gerberconstructioninc/",
    "facebook": "https://www.facebook.com/GerberConstructionIncorporated",
    "linkedin": "https://www.linkedin.com/company/gerber-construction-inc",
    "tagline": "Build the work. Build the team. Build what lasts.",
    "year": "2026",
}

VALUES = [
    {
        "how": "How we work",
        "name": "Lock In",
        "body": "We show up ready, stay locked in, and bring care to every task, because we believe in what we're building and take pride in putting our name on it.",
    },
    {
        "how": "How we communicate",
        "name": "Solve, Don't Stir",
        "body": "We talk with clarity, listen with intent, and address problems head-on, because trust is built in how we show up and speak up.",
    },
    {
        "how": "How we act",
        "name": "Good for It",
        "body": "We take ownership of our actions and our results, hold the line on what's right, and treat people the way we want to be treated. No excuses, no shortcuts.",
    },
    {
        "how": "How we think",
        "name": "Better Every Pass",
        "body": "We believe in constant improvement, on the job, in our mindset, and in our character.",
    },
]

SAFETY = "Everybody goes home every night. That's the one number on the job that has to come out perfect."

PILLARS = [
    {
        "title": "Earthwork",
        "photo": ("norwalk-grading", "Dozer grading the pad while two excavators work the cut, Norwalk High School, June 2024"),
        "photo_fallback": "osgood-excavator",
        "body": "We move the dirt ourselves. Mass excavation, cut-and-fill balance, GPS-controlled finish grading, and the crushing, screening and soil stabilization that turn what's on the site into what the job needs.",
        "items": [
            "Mass excavation and grading",
            "GPS machine control and finish grading",
            "Crushing and screening",
            "Soil stabilization",
            "Hazardous soil handling and disposal",
            "Trucking",
        ],
    },
    {
        "title": "Underground utilities",
        "photo": ("norwalk-trench", "Two excavators and the pipe crew in the trench at Norwalk High School, June 2024"),
        "photo_fallback": "bowers-trench",
        "body": "Storm, sanitary, water and electric. Deep structures, long runs and tight corridors. Our crews set pipe to line and grade, build the structures, and leave the surface ready for whoever comes next.",
        "items": [
            "Storm drainage",
            "Sanitary sewer",
            "Water mains and services",
            "Electrical ductbank",
            "Precast structures and manholes",
            "Septic systems",
        ],
    },
    {
        "title": "Turnkey site packages",
        "photo": ("norwalk-nov-aerial", "Norwalk High School from the air, November 2024: grading, utilities, structures and roads, all one contract"),
        "body": "One contract from clearing to curb. Erosion control, earthwork, utilities, retaining walls, site concrete and paving, run by one team on one schedule, with one responsible party for the whole site.",
        "items": [
            "Erosion and sediment control",
            "Retaining walls",
            "Bridges and culverts",
            "Site concrete, curbing and sidewalks",
            "Asphalt paving",
            "Site restoration",
        ],
    },
]

# The order real site work happens in. Numbered on the Services page because it is a sequence.
SEQUENCE = [
    ("Erosion control and clearing", "Silt fence, construction entrances, basins and swales go in first, then the site gets cleared, grubbed and stripped."),
    ("Mass excavation and grading", "Cut, fill and balance to the subgrade plan. Rock gets drilled, blasted or hammered, then crushed and screened for reuse. Unsuitable soils are stabilized or hauled."),
    ("Underground utilities", "Storm, sanitary, water and electric go in to line and grade with the structures that connect them, tested and inspected before anything gets buried."),
    ("Structures", "Retaining walls, culverts, foundation drainage and the backfill around whatever the vertical contractor is bringing."),
    ("Fine grading", "GPS-controlled grading to finished subgrade, proof-rolled and ready for base."),
    ("Site concrete and paving", "Curbing, sidewalks, pads, base and asphalt."),
    ("Restoration", "Topsoil, seed, plantings and cleanup, with the site handed over the way the drawings show it."),
]

UTILITY_COLORS = [
    ("Water mains and services", "water"),
    ("Storm drainage", "sewer"),
    ("Sanitary sewer", "sewer"),
    ("Electrical ductbank", "electric"),
    ("Gas (coordinated with the utility)", "gas"),
    ("Communications ductbank", "comm"),
]

PROJECTS = [
    {
        "slug": "norwalk-high-school",
        "title": "Norwalk High School",
        "town": "Norwalk, Connecticut",
        "line": "More than 100,000 cubic yards moved and four miles of pipe under a new high school campus.",
        "facts": [
            ("Location", "Norwalk, CT"),
            ("Owner", "City of Norwalk"),
            ("Construction manager", "Gilbane"),
            ("Gerber's role", "Site and utility contractor"),
            ("Years", "2024 to present"),
        ],
        "photo": "Norwalk High School site from the air, June 2024",
        "img": "norwalk-aerial",
        "gallery": [("norwalk-nov-pipe", "Setting large-diameter storm pipe, November 2024"), ("norwalk-nov-crew", "Crew setting structures, November 2024"), ("norwalk-topdown", "Setting a structure, straight down from the drone, June 2024")],
        "paras": [
            "Norwalk's new high school campus sits on a tight urban site with a lot of contractors working at once. Gerber's crews excavated, graded and balanced more than 100,000 cubic yards of material to build the building pads, the parking lots and the athletic fields.",
            "Below grade, we installed more than 21,000 linear feet of storm, sanitary and water pipe, including deep storm drainage structures and extensive underdrain systems. Above it, we built the retaining walls, curbing, sidewalks and asphalt paving for both the main campus and the athletic complex.",
            "The job ran on a phased schedule that had to hold for everyone else on site. We delivered a fully prepared site, ready for vertical construction, on time and within budget.",
        ],
        "numbers": [("100,000+", "cubic yards excavated, graded and balanced"), ("21,000+", "linear feet of storm, sanitary and water pipe")],
        "scope": ["Mass excavation and grading", "Storm, sanitary and water utilities", "Deep storm structures and underdrain", "Retaining walls", "Curbing and sidewalks", "Asphalt paving", "Athletic field construction"],
    },
    {
        "slug": "bowers-elementary-school",
        "title": "Bowers Elementary School",
        "town": "Manchester, Connecticut",
        "line": "The full site package for Manchester's new elementary school, with stormwater storage below grade.",
        "facts": [
            ("Location", "Manchester, CT"),
            ("Owner", "Town of Manchester"),
            ("Gerber's role", "Site and utility contractor"),
            ("Years", "2022 to 2024"),
        ],
        "photo": "Bowers Elementary site from the air, April 2023",
        "img": "bowers-aerial",
        "gallery": [("bowers-trench", "Storm pipe going in, April 2023"), ("bowers-boom", "A Gerber excavator at Bowers"), ("bowers-loading", "Loading out")],
        "paras": [
            "Manchester replaced Bowers Elementary with a new school, and Gerber delivered the site package underneath it: mass excavation and grading for the building and its grounds, then the storm, sanitary and water utilities that serve them.",
            "Stormwater on a school campus has nowhere to go but down, so the site carries a subsurface storage system beneath it. Our crews installed it along with the drainage that feeds it, then finished the site with curbing, sidewalks and paving.",
        ],
        "numbers": [],
        "scope": ["Mass excavation and grading", "Storm, sanitary and water utilities", "Subsurface stormwater storage", "Site concrete, curbing and sidewalks", "Paving"],
    },
    {
        "slug": "osgood-park",
        "title": "Osgood Park",
        "town": "New Britain, Connecticut",
        "line": "A city park rebuilt with Gerber as general contractor: new building, lit fields and a spray pad.",
        "facts": [
            ("Location", "New Britain, CT"),
            ("Owner", "City of New Britain"),
            ("Gerber's role", "General contractor"),
            ("Years", "2022 to 2023"),
        ],
        "photo": "The new fields at Osgood Park from the air, April 2023",
        "img": "osgood-field",
        "gallery": [("osgood-building", "The new park building, April 2023"), ("osgood-excavator", "Site work at Osgood Park")],
        "paras": [
            "Osgood Park is a neighborhood park in New Britain, and Gerber was the general contractor for its renovation. We took down the old bathroom and concession buildings, handled the abatement that came with them, and built the new multipurpose building in their place.",
            "Around it, our crews rebuilt the grounds: site utilities, mass and trench rock excavation, new sports lighting on the fields and a spray pad for the summer. It's the kind of job where the earthwork, the utilities and the building all have to come from one team that owns the whole schedule.",
        ],
        "numbers": [],
        "scope": ["Demolition and abatement", "New multipurpose building", "Site utilities", "Mass and trench rock excavation", "Sports lighting", "Spray pad", "Site concrete and paving"],
    },
    {
        "slug": "route-140-charters-brook",
        "title": "Route 140 over Charters Brook",
        "town": "Ellington, Connecticut",
        "line": "A CTDOT bridge replacement over Charters Brook in our hometown, built inside a cofferdam.",
        "facts": [
            ("Location", "Ellington, CT"),
            ("Owner", "Connecticut Department of Transportation"),
            ("Gerber's role", "Prime contractor"),
            ("Years", "2020 to 2021"),
        ],
        "photo": "Inside the cofferdam at Charters Brook, August 2021",
        "img": "route140-cofferdam",
        "gallery": [("route140-sheeting", "Sheeting and excavation, July 2021"), ("route140-pour", "Concrete, August 2021")],
        "paras": [
            "Bridge No. 02668 carries Route 140 over Charters Brook in Ellington, a few minutes from our shop. For CTDOT, Gerber replaced the structure as prime contractor.",
            "We installed a cofferdam and handled the brook through the work, made the mass cut and set the sheeting, placed the new precast structure and the cast-in-place concrete around it, then rebuilt and paved the roadway over the top. State bridge work on a live road, with the water running the whole time.",
        ],
        "numbers": [],
        "scope": ["Cofferdam and water handling", "Mass excavation and sheeting", "Precast structure", "Cast-in-place concrete", "Roadway reconstruction and paving"],
    },
    {
        "slug": "uconn-athletic-district",
        "title": "UConn Athletic District",
        "town": "Storrs, Connecticut",
        "line": "Site development and utilities beneath UConn's new stadium district.",
        "facts": [
            ("Location", "Storrs, CT"),
            ("Owner", "University of Connecticut"),
            ("Gerber's role", "Site and utility contractor"),
            ("Years", "2019 to 2021"),
        ],
        "photo": "The Athletic District from the air, November 2020",
        "img": "uconn-athletic-overview",
        "gallery": [("uconn-athletic-pipe-crew", "Setting reinforced concrete storm pipe, June 2020"), ("uconn-athletic-pipe", "Pipe in the trench, June 2020"), ("uconn-athletic-dji", "The baseball field, December 2020"), ("uconn-athletic-softball", "The softball field, November 2020")],
        "paras": [
            "UConn rebuilt its Athletic District around a new soccer stadium, new baseball and softball fields and a new hockey arena. Gerber's part was the ground under all of it.",
            "Our crews performed the site development and underground utility infrastructure across the district: the earthwork that shaped the stadium and field footprints and the storm, sanitary, water and electrical systems that serve them, on an active campus with a hard calendar.",
        ],
        "numbers": [],
        "scope": ["Site development and mass grading", "Storm drainage", "Sanitary sewer and water", "Electrical ductbank", "Site concrete and paving"],
    },
    {
        "slug": "uconn-innovation-partnership-building",
        "title": "UConn Innovation Partnership Building",
        "town": "Storrs, Connecticut",
        "line": "Earthwork and utilities for the research building that anchors UConn's Technology Park.",
        "facts": [
            ("Location", "Storrs, CT"),
            ("Owner", "University of Connecticut"),
            ("Gerber's role", "Site and utility contractor"),
            ("Years", "2016 to 2017"),
        ],
        "photo": "The Innovation Partnership Building from the air, August 2017",
        "img": "uconn-ipb-aerial",
        "gallery": [("uconn-ipb-aerial-2", "Technology Park from above, August 2017")],
        "paras": [
            "The Innovation Partnership Building is the research building that anchors UConn's Technology Park in Storrs. Gerber performed the earthwork and underground utilities for the building and its grounds.",
            "Campus work like this runs under the university's wrap-up insurance and inspection program, and it rewards contractors who do their own work and keep their own schedule.",
        ],
        "numbers": [],
        "scope": ["Mass excavation and grading", "Storm, sanitary and water utilities", "Electrical ductbank", "Site concrete and paving"],
    },
    {
        "slug": "uconn-south-campus-infrastructure",
        "title": "UConn South Campus Infrastructure, Phase 1",
        "town": "Storrs, Connecticut",
        "line": "Every utility under South Campus rerouted ahead of the new residence hall, with classes in session.",
        "facts": [
            ("Location", "Storrs, CT"),
            ("Owner", "University of Connecticut"),
            ("Construction manager", "O&G Industries"),
            ("Years", "2023 to 2024"),
        ],
        "photo": "The braced excavation at South Campus with the crew down in it, April 2024",
        "img": "south-campus-excavation",
        "gallery": [("south-campus-box", "Pipe going in behind the bracing, April 2024"), ("south-campus-pipe", "Setting large-diameter pipe in the trench box, March 2024"), ("south-campus-trench", "Pre-insulated piping in the trench, April 2024"), ("south-campus-structure", "Setting a precast structure, December 2023")],
        "paras": [
            "Under UConn's South Campus runs the utility backbone for the residence halls and dining hall that were about to be built. Working for O&G Industries, Gerber rerouted and rebuilt it ahead of the new construction.",
            "Steam, storm, sanitary and water lines, pump station work, and the Gilbert Road and Mansfield Road intersection, all on an open campus and around the academic calendar, from 2023 into 2024. Phasing, traffic control and keeping buildings in service were as much the job as the pipe.",
        ],
        "numbers": [],
        "scope": ["Steam line relocation", "Storm, sanitary and water utilities", "Pump station work", "Roadway and intersection reconstruction", "Campus phasing and maintenance of traffic"],
    },
]

STORY_SHORT = [
    "In 1984, Ron Gerber decided he couldn't milk one more cow on his family's dairy farm in Vernon. He and a friend pooled their money for a 1974 Ford backhoe and went looking for digging work. The first jobs were backyards. One was moving a three-foot boulder for an elderly neighbor, and he still talks about it.",
    "Forty years on, Gerber Construction is a heavy civil and utility contractor working across Connecticut and into New England, prequalified with CTDOT, CT DAS and MassDOT, running our own equipment with our own crews. The equipment and the technology get better every year. The people are the point: everyone who joins becomes part of the story, and every job is built by the men and women who wear our name.",
]

STORY = [
    "In 1984, Ron Gerber realized he couldn't milk one more cow on his family's dairy farm in Vernon, Connecticut. Determined to chart a new path, he and a friend pooled their money to buy a 1974 Ford backhoe and set out to find someone in need of excavation work. Ron quickly developed a passion for digging, learning his craft in the backyards of his community. He still recalls with pride the day he moved a three-foot boulder for an elderly neighbor, a small job that was the start of something much bigger.",
    "With grit, long hours and a focus on doing things the right way, Ron grew Gerber Construction from a two-man operation into a respected heavy civil and utility contractor. What began with backyard projects soon expanded into large-scale site development and utility infrastructure across Connecticut.",
    "From the beginning, quality and integrity have been our foundation. As projects grew larger, so did our team, and today Gerber Construction stands as one of Connecticut's leading contractors, with our eyes set on even greater opportunities across New England.",
    "We continue to invest in state-of-the-art equipment, the latest technology and, most importantly, our people. At Gerber, we're a family. Every new team member becomes part of our story, and every project is built on the hard work and dedication of the men and women who wear our name with pride.",
]
