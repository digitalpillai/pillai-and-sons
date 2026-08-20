"""
gen_content.py  —  V1
All site copy for Pillai & Sons Motor Company in one place.

PRICES: every figure below is a starting ex-showroom price taken from Maruti
Suzuki's own site in August 2026. Car prices move constantly and vary by variant
and by city. They are shown on the site labelled "ex-showroom, indicative" with a
"Get on-road price" button beside them, and every one is editable from the admin
panel. Check them before launch and after each manufacturer revision.
"""

# ============================================================ CHANNELS =======
CHANNELS = [
    {
        "key": "arena", "name": "Maruti Suzuki ARENA", "short": "ARENA",
        "tag": "New cars", "colour": "arena", "icon": "car",
        "blurb": "The everyday Maruti Suzuki range — hatchbacks, sedans, SUVs, MPVs "
                 "and vans built for Indian roads and Indian running costs.",
    },
    {
        "key": "nexa", "name": "NEXA", "short": "NEXA",
        "tag": "Premium cars", "colour": "nexa", "icon": "sparkle",
        "blurb": "Maruti Suzuki's premium channel. A quieter showroom, a different "
                 "class of car, and a buying experience built around taking your time.",
    },
    {
        "key": "true-value", "name": "True Value", "short": "True Value",
        "tag": "Pre-owned", "colour": "truevalue", "icon": "exchange",
        "blurb": "Certified pre-owned cars, each through a documented inspection, "
                 "with a clear title and a warranty you can hold us to.",
    },
    {
        "key": "service", "name": "Maruti Suzuki Service", "short": "Service",
        "tag": "Workshop", "colour": "service", "icon": "wrench",
        "blurb": "Periodic maintenance, body and paint, genuine parts and accessories, "
                 "carried out by Maruti-trained technicians on Maruti equipment.",
    },
    {
        "key": "driving-school", "name": "Maruti Driving School", "short": "Driving School",
        "tag": "Learn to drive", "colour": "school", "icon": "steering",
        "blurb": "Learn on dual-control cars with certified instructors, simulator "
                 "sessions and a syllabus that covers more than passing the test.",
    },
]

CHANNEL_BY_KEY = {c["key"]: c for c in CHANNELS}

# ============================================================== MODELS =======
MODELS = [
    # ---------------------------------------------------------------- ARENA
    {
        "key": "s-presso", "name": "S-Presso", "channel": "arena",
        "body": "tall-hatch", "segment": "Hatchback", "price": "3,49,900",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "24.76 km/l", "engine": "1.0L K-Series Dual Jet",
        "pitch": "The mini SUV. High seating, a commanding view of the road and a "
                 "turning circle that makes Thanjavur's older streets easy.",
        "highlights": [
            "Raised ground clearance and an SUV-inspired stance",
            "Tall-boy cabin — genuinely easy to get in and out of",
            "Factory-fitted S-CNG option with a dual-interdependent ECU",
            "Compact footprint that parks almost anywhere",
        ],
    },
    {
        "key": "alto-k10", "name": "Alto K10", "channel": "arena",
        "body": "hatchback", "segment": "Hatchback", "price": "3,69,900",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "24.90 km/l", "engine": "1.0L K-Series Dual Jet",
        "pitch": "India's most familiar first car, on the lighter HEARTECT platform. "
                 "Cheap to run, cheaper still to maintain.",
        "highlights": [
            "The lowest cost of ownership anywhere in the range",
            "AMT option — city driving without a clutch pedal",
            "Parts available at any Maruti workshop in the country",
            "Strong, predictable resale value",
        ],
    },
    {
        "key": "celerio", "name": "Celerio", "channel": "arena",
        "body": "hatchback", "segment": "Hatchback", "price": "4,69,900",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "26.68 km/l", "engine": "1.0L K-Series Dual Jet",
        "pitch": "The mileage champion of the petrol range. If your monthly fuel bill "
                 "is the number that matters, start here.",
        "highlights": [
            "Among the highest certified petrol mileage figures on sale",
            "Roomier cabin than the footprint suggests",
            "Idle start-stop technology on higher trims",
            "AMT available across most variants",
        ],
    },
    {
        "key": "wagon-r", "name": "WagonR", "channel": "arena",
        "body": "tall-hatch", "segment": "Hatchback", "price": "4,98,900",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "24.35 km/l", "engine": "1.0L / 1.2L K-Series Dual Jet",
        "pitch": "The tall-boy that has outsold almost everything else for two decades. "
                 "Space where families need it — headroom and door openings.",
        "highlights": [
            "Best-in-class headroom and an upright driving position",
            "Two engines — 1.0L for economy, 1.2L for highway work",
            "341-litre boot, large for the segment",
            "The default choice for a growing family on a budget",
        ],
    },
    {
        "key": "swift", "name": "Swift", "channel": "arena",
        "body": "hatchback", "segment": "Hatchback", "price": "5,83,900",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "25.75 km/l", "engine": "1.2L Z-Series",
        "pitch": "The one people buy because they enjoy driving it. The Z-Series engine "
                 "is quieter and thriftier than the unit it replaced.",
        "highlights": [
            "The keenest steering and chassis of the Arena hatchbacks",
            "New-generation Z-Series engine with notably better economy",
            "9-inch SmartPlay Pro+ with wireless Android Auto and CarPlay",
            "Six airbags standard across the range",
        ],
    },
    {
        "key": "dzire", "name": "Dzire", "channel": "arena",
        "body": "sedan", "segment": "Sedan", "price": "6,30,600",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "24.79 km/l", "engine": "1.2L Z-Series",
        "pitch": "A proper boot, a quiet cabin and a badge that holds its value. The "
                 "default sedan for family use and commercial running alike.",
        "highlights": [
            "382-litre boot — a week's luggage, or a taxi's worth of bags",
            "5-star Global NCAP adult occupant rating",
            "Rear seat comfortable for three adults on a long run",
            "The strongest resale in its segment, year after year",
        ],
    },
    {
        "key": "brezza", "name": "Brezza", "channel": "arena",
        "body": "compact-suv", "segment": "Compact SUV", "price": "7,39,900",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, 6-speed AT",
        "mileage": "19.80 km/l", "engine": "1.5L K-Series Dual Jet",
        "pitch": "The compact SUV that made the segment. Sub-four-metre footprint, real "
                 "ground clearance, and a proper torque converter automatic.",
        "highlights": [
            "6-speed torque converter automatic — smoother than an AMT",
            "Electric sunroof and 360-degree camera on higher trims",
            "Head-up display and ventilated front seats",
            "S-CNG option with no compromise on boot access",
        ],
    },
    {
        "key": "ertiga", "name": "Ertiga", "channel": "arena",
        "body": "mpv", "segment": "MPV", "price": "8,90,000",
        "seats": "7", "fuel": "Petrol, CNG", "gearbox": "Manual, 6-speed AT",
        "mileage": "20.51 km/l", "engine": "1.5L K-Series Dual Jet",
        "pitch": "Seven seats without the bulk of a full-size MPV, and running costs "
                 "closer to a hatchback. The workhorse of Indian family travel.",
        "highlights": [
            "Genuine seven-seat capacity with a usable third row",
            "Second row slides and reclines for legroom or luggage",
            "S-CNG variant — among the cheapest seven-seat running costs in India",
            "6-speed automatic available on the top trim",
        ],
    },
    {
        "key": "victoris", "name": "Victoris", "channel": "arena",
        "body": "mid-suv", "segment": "SUV", "price": "10,49,900",
        "seats": "5", "fuel": "Petrol, Hybrid, CNG", "gearbox": "Manual, AT, e-CVT",
        "mileage": "Up to 28.65 km/l", "engine": "1.5L, Strong Hybrid option",
        "pitch": "Arena's midsize SUV, launched late 2025. Strong hybrid, AllGrip "
                 "all-wheel drive and a 5-star Bharat NCAP rating.",
        "highlights": [
            "Strong Hybrid variant with class-leading certified economy",
            "AllGrip Select all-wheel drive available",
            "5-star Bharat NCAP for adult and child occupants",
            "Level 2 ADAS on higher trims",
        ],
    },
    {
        "key": "eeco", "name": "Eeco", "channel": "arena",
        "body": "van", "segment": "Van", "price": "5,28,400",
        "seats": "5 / 7", "fuel": "Petrol, CNG", "gearbox": "Manual",
        "mileage": "19.71 km/l", "engine": "1.2L K-Series",
        "pitch": "Five or seven seats, or a flat load bay. The van that runs schools, "
                 "shops and small businesses across the delta.",
        "highlights": [
            "Cargo and passenger versions from the same showroom",
            "Flat floor and a tall roof — loads that will not fit in a car",
            "S-CNG option for high-mileage commercial running",
            "Simple mechanicals, cheap to keep on the road",
        ],
    },
    # ----------------------------------------------------------------- NEXA
    {
        "key": "baleno", "name": "Baleno", "channel": "nexa",
        "body": "hatchback", "segment": "Premium hatchback", "price": "5,98,000",
        "seats": "5", "fuel": "Petrol, CNG", "gearbox": "Manual, AMT",
        "mileage": "22.35 km/l", "engine": "1.2L K-Series Dual Jet",
        "pitch": "NEXA's entry point and India's best-selling premium hatchback. A big "
                 "cabin, a supple ride and a genuinely good stereo.",
        "highlights": [
            "HeadUp Display and 360-degree view camera",
            "9-inch SmartPlay Pro+ with Arkamys-tuned sound",
            "Six airbags standard, ESP with hill hold",
            "The roomiest cabin in the premium hatchback class",
        ],
    },
    {
        "key": "fronx", "name": "Fronx", "channel": "nexa",
        "body": "compact-suv", "segment": "Crossover SUV", "price": "6,84,000",
        "seats": "5", "fuel": "Petrol, Turbo, CNG", "gearbox": "Manual, AMT, 6-speed AT",
        "mileage": "21.79 km/l", "engine": "1.2L Dual Jet / 1.0L Boosterjet",
        "pitch": "A crossover that drives like a hatchback. The Boosterjet turbo with "
                 "the 6-speed automatic is the driver's pick of the NEXA range.",
        "highlights": [
            "1.0L Boosterjet turbo with a proper 6-speed torque converter",
            "Coupe-inspired roofline with real ground clearance",
            "360-degree camera and HeadUp Display",
            "S-CNG option on the naturally aspirated engine",
        ],
    },
    {
        "key": "grand-vitara", "name": "Grand Vitara", "channel": "nexa",
        "body": "mid-suv", "segment": "Midsize SUV", "price": "10,76,000",
        "seats": "5", "fuel": "Petrol, Strong Hybrid, CNG", "gearbox": "Manual, AT, e-CVT",
        "mileage": "Up to 27.97 km/l", "engine": "1.5L Intelligent Electric Hybrid",
        "pitch": "The midsize SUV that runs on electric power alone at low speeds. "
                 "Nearly 28 km/l from a petrol SUV is not a typo.",
        "highlights": [
            "Intelligent Electric Hybrid — drives on battery alone in traffic",
            "AllGrip Select all-wheel drive with four terrain modes",
            "Panoramic sunroof and ventilated front seats",
            "Level 2 ADAS with adaptive cruise control",
        ],
    },
    {
        "key": "xl6", "name": "XL6", "channel": "nexa",
        "body": "mpv", "segment": "Premium MPV", "price": "11,57,000",
        "seats": "6", "fuel": "Petrol, CNG", "gearbox": "Manual, 6-speed AT",
        "mileage": "20.97 km/l", "engine": "1.5L K-Series Dual Jet",
        "pitch": "Six seats with captain chairs in the middle row, for families who "
                 "travel together and would rather not climb over anybody.",
        "highlights": [
            "Second-row captain seats with individual armrests",
            "Walk-through access to the third row",
            "6-speed automatic and cruise control",
            "S-CNG option — rare in a premium six-seater",
        ],
    },
    {
        "key": "jimny", "name": "Jimny", "channel": "nexa",
        "body": "offroader", "segment": "Off-roader", "price": "12,39,000",
        "seats": "4", "fuel": "Petrol", "gearbox": "Manual, 4-speed AT",
        "mileage": "16.94 km/l", "engine": "1.5L K-Series",
        "pitch": "A ladder-frame, low-range four-wheel-drive off-roader with five doors. "
                 "There is nothing quite like it at this price.",
        "highlights": [
            "AllGrip Pro with a proper low-range transfer case",
            "Ladder-frame chassis and three-link rigid axles",
            "210 mm ground clearance and a 36-degree approach angle",
            "Five doors — usable daily, unlike most of its rivals",
        ],
    },
    {
        "key": "e-vitara", "name": "e Vitara", "channel": "nexa",
        "body": "mid-suv", "segment": "Electric SUV", "price": "15,99,000",
        "seats": "5", "fuel": "Electric", "gearbox": "Single-speed",
        "mileage": "Up to 543 km range", "engine": "49 kWh / 61 kWh battery",
        "pitch": "Maruti Suzuki's first electric SUV, on a dedicated EV platform, with "
                 "charging and service supported here in Thanjavur.",
        "highlights": [
            "Two battery choices — 49 kWh and 61 kWh",
            "Up to 543 km of certified range",
            "DC fast charging with a heat-pump climate system",
            "Battery covered under Maruti Suzuki's EV warranty programme",
        ],
    },
    {
        "key": "invicto", "name": "Invicto", "channel": "nexa",
        "body": "mpv", "segment": "Flagship MPV", "price": "24,97,000",
        "seats": "7 / 8", "fuel": "Strong Hybrid", "gearbox": "e-CVT",
        "mileage": "23.24 km/l", "engine": "2.0L Strong Hybrid",
        "pitch": "The flagship. A seven or eight-seat hybrid MPV for people who are "
                 "driven as often as they drive.",
        "highlights": [
            "2.0L Strong Hybrid — 23.24 km/l from a three-row MPV",
            "Seven or eight-seat layouts with second-row ottoman seats",
            "Panoramic sunroof and a powered tailgate",
            "The most equipped car Maruti Suzuki sells",
        ],
    },
]

MODEL_BY_KEY = {m["key"]: m for m in MODELS}
ARENA_MODELS = [m for m in MODELS if m["channel"] == "arena"]
NEXA_MODELS = [m for m in MODELS if m["channel"] == "nexa"]

# ============================================================= SERVICES ======
SERVICES = [
    {
        "key": "periodic-maintenance", "icon": "wrench",
        "name": "Periodic Maintenance",
        "blurb": "Scheduled servicing to the Maruti Suzuki interval chart, with a "
                 "printed job card and nothing done that you have not approved.",
        "lead": "Servicing to the book, priced before we start",
        "intro": [
            "Every Maruti Suzuki has a published service schedule, and following it is "
            "what keeps the warranty intact and the resale value where it should be. We "
            "work to that chart — not to whatever the workshop feels like selling on the "
            "day.",
            "You get an estimate before the spanners come out. If we find something else "
            "once the car is on the lift, we call you, explain it, and wait for a yes. "
            "Nothing joins the bill silently.",
        ],
        "points": [
            "Free pick-up and drop within Thanjavur city limits",
            "Maruti Genuine Parts only, with part numbers on your invoice",
            "Digital job card — you can see what was done and what it cost",
            "Vehicle health report with photographs of anything we flag",
            "Same-day delivery on standard periodic services",
        ],
        "faqs": [
            ("How often should I service my car?",
             "Maruti Suzuki's schedule is every 10,000 km or 12 months, whichever comes "
             "first, for most current petrol models. CNG and older models differ — tell us "
             "the model and year and we will confirm the exact interval."),
            ("Will servicing elsewhere void my warranty?",
             "Warranty terms require servicing at an authorised workshop within the "
             "prescribed intervals using genuine parts. Servicing outside that network can "
             "put a claim at risk. We are an authorised Maruti Suzuki workshop."),
            ("Do you give an estimate first?",
             "Always. You approve the estimate before work starts, and we call you for "
             "approval before adding anything to it."),
        ],
    },
    {
        "key": "body-shop", "icon": "shield",
        "name": "Body Shop and Accident Repair",
        "blurb": "Panel work, denting and painting in a controlled booth, with the "
                 "insurance claim handled end to end on your behalf.",
        "lead": "Accident repair, and the paperwork that comes with it",
        "intro": [
            "An accident is stressful enough without an insurance process on top. We "
            "handle the survey, the claim and the follow-up with your insurer directly, "
            "so in most cases you pay your excess and collect the car.",
            "Paint is matched to your car's colour code and baked in a booth, not sprayed "
            "in the open. That is the difference between a repair that disappears and one "
            "you can spot from across a car park.",
        ],
        "points": [
            "Cashless claim support with all major insurers",
            "Colour-coded paint matching and an oven-baked finish",
            "Structural repair on a measuring jig where needed",
            "Photographic record of the damage before and after",
            "Free re-inspection within 30 days of collection",
        ],
        "faqs": [
            ("Do you handle the insurance claim?",
             "Yes. We coordinate the surveyor visit, submit the estimate and documents and "
             "follow the claim through. With cashless-approved insurers you settle only "
             "your excess and any non-payable items."),
            ("How long does accident repair take?",
             "Light cosmetic work is usually two to four days. Structural repair depends on "
             "parts availability and how quickly the surveyor approves — we give you a date "
             "once the survey is done, and tell you if it moves."),
        ],
    },
    {
        "key": "parts-accessories", "icon": "cog",
        "name": "Genuine Parts and Accessories",
        "blurb": "Maruti Genuine Parts over the counter, plus an accessory range "
                 "fitted and warranted by us rather than by a roadside shop.",
        "lead": "The right part, with the part number on the bill",
        "intro": [
            "Counterfeit parts are a real problem in this market, and the ones that matter "
            "most — brake pads, filters, suspension — are the ones most often faked. "
            "Everything we fit comes through the Maruti Suzuki supply chain and is printed "
            "on your invoice with its part number, so you can verify it.",
            "The accessory range runs from floor mats and seat covers to reverse cameras, "
            "body kits and security systems. Fitted here they stay inside your vehicle "
            "warranty; fitted elsewhere they may not.",
        ],
        "points": [
            "Maruti Genuine Parts and Maruti Genuine Accessories",
            "Part numbers printed on every invoice",
            "Accessory fitment that does not affect your vehicle warranty",
            "Counter sales — you do not have to book the car in",
            "Warranty on parts as well as on labour",
        ],
        "faqs": [
            ("Can I buy parts without booking a service?",
             "Yes. The parts counter is open through workshop hours for over-the-counter "
             "sales. Bring your registration number so we can confirm the exact variant."),
            ("Are accessories covered by warranty?",
             "Maruti Genuine Accessories fitted by us carry their own warranty and do not "
             "affect your vehicle warranty. Accessories fitted elsewhere can affect a claim "
             "where they involve wiring or bodywork."),
        ],
    },
    {
        "key": "extended-warranty", "icon": "certificate",
        "name": "Extended Warranty and Service Plans",
        "blurb": "Cover beyond the standard warranty period, and pre-paid service "
                 "packages that fix today's rates for years ahead.",
        "lead": "Fix the cost now, use it later",
        "intro": [
            "Maruti Suzuki's standard warranty covers the first stretch of a car's life. "
            "Extended warranty carries that further, and it is far cheaper bought before "
            "the original expires than after.",
            "Pre-paid service packages work on the same logic. You pay today's labour and "
            "parts rates for a set number of services and use them over the coming years, "
            "which takes the sting out of the bigger scheduled services.",
        ],
        "points": [
            "Extended warranty available up to the fifth year",
            "Transferable to the next owner — a real resale advantage",
            "Pre-paid service packages at today's rates",
            "Roadside assistance across India",
            "One place to buy it, one place to claim it",
        ],
        "faqs": [
            ("When should I buy extended warranty?",
             "Before the standard warranty expires. Once it has lapsed the options narrow "
             "and the vehicle usually needs inspecting first."),
            ("Does it transfer if I sell the car?",
             "Yes, and it is worth putting in the advertisement — a buyer taking on a car "
             "with warranty remaining will usually pay more for it."),
        ],
    },
]

SERVICE_BY_KEY = {s["key"]: s for s in SERVICES}

# ========================================================== TRUE VALUE =======
TRUE_VALUE_CHECKS = [
    "Engine compression and cold-start behaviour",
    "Gearbox and clutch under load",
    "Suspension, steering geometry and tyre wear pattern",
    "Brake pad and disc thickness measured, not eyeballed",
    "Electricals, air conditioning and every switch",
    "Body panel thickness gauged for hidden accident repair",
    "Chassis and engine numbers verified against the RC",
    "Loan closure, hypothecation and challan status checked",
]

TRUE_VALUE_STEPS = [
    ("Bring the car in",
     "Free valuation at our Thanjavur yard. It takes about forty minutes and you "
     "leave with a written figure."),
    ("We inspect it properly",
     "A documented check across mechanicals, body and paperwork — the same list we "
     "apply to the cars we sell."),
    ("Agree the price",
     "Our offer stands for seven days. No haggling on the day of collection and no "
     "revision after the inspection."),
    ("Paperwork and payment",
     "We handle the RC transfer, NOC and insurance transfer. Payment goes to your "
     "bank account, not in cash."),
]

# ====================================================== DRIVING SCHOOL =======
DRIVING_COURSES = [
    {
        "name": "Beginner", "duration": "21 days", "price": "6,500",
        "sessions": "21 practical sessions plus theory",
        "for": "Never driven before", "featured": False,
        "includes": [
            ("Dual-control training car", True),
            ("Certified instructor throughout", True),
            ("Traffic rules and signage theory", True),
            ("Simulator sessions", True),
            ("Learner's licence assistance", True),
            ("Driving licence test support", True),
            ("Highway and night driving module", False),
            ("Refresher sessions after licensing", False),
        ],
    },
    {
        "name": "Complete", "duration": "30 days", "price": "9,500",
        "sessions": "30 practical sessions plus theory",
        "for": "Most learners choose this", "featured": True,
        "includes": [
            ("Dual-control training car", True),
            ("Certified instructor throughout", True),
            ("Traffic rules and signage theory", True),
            ("Simulator sessions", True),
            ("Learner's licence assistance", True),
            ("Driving licence test support", True),
            ("Highway and night driving module", True),
            ("Two refresher sessions after licensing", True),
        ],
    },
    {
        "name": "Refresher", "duration": "10 days", "price": "4,500",
        "sessions": "10 practical sessions",
        "for": "Licensed but out of practice", "featured": False,
        "includes": [
            ("Dual-control training car", True),
            ("Certified instructor throughout", True),
            ("Confidence building in traffic", True),
            ("Parking and reversing intensive", True),
            ("Highway driving module", True),
            ("Flexible session timings", True),
            ("Full theory syllabus", False),
            ("Licence application assistance", False),
        ],
    },
]

# =============================================================== OFFERS ======
OFFER_KINDS = [
    ("Exchange bonus", "exchange",
     "Bring in any make or model. We value it at the True Value yard and set the "
     "figure against your new car on the same invoice."),
    ("Corporate and fleet", "briefcase",
     "Additional benefit for employees of listed companies, and negotiated terms for "
     "fleet purchases of three vehicles or more."),
    ("Finance offers", "wallet",
     "Rates from our partner banks and NBFCs, with the interest cost shown in rupees "
     "over the full term rather than as a rate alone."),
    ("Accessory packages", "cog",
     "Bundled accessory kits priced below the cost of fitting the same items "
     "individually after delivery."),
]

# ============================================================== REASONS ======
WHY_US = [
    ("certificate", "Authorised, not a broker",
     "An authorised Maruti Suzuki dealership. Every car comes with a proper invoice, "
     "full manufacturer warranty and a service history that stays on the Maruti network."),
    ("wallet", "The on-road price in writing",
     "Ex-showroom, registration, insurance, TCS and accessories itemised on one sheet "
     "before you commit. No line appears later that was not on it."),
    ("wrench", "Sales and service under one roof",
     "Buy here, service here, claim here. The people who hand you the keys are the "
     "people you speak to at the first service."),
    ("users", "A family business in Thanjavur",
     "We live here. Our reputation in this town is worth more than any single sale, "
     "and that shapes how we handle the difficult conversations."),
]

BUY_STEPS = [
    ("Tell us what you need",
     "Budget, seats, monthly running, city or highway. That narrows seventeen models "
     "to two or three very quickly."),
    ("Drive them",
     "A test drive at the showroom, or at your home or office. Take the shortlist out "
     "back to back on the same day — it is the only way to feel the difference."),
    ("See the full price",
     "An itemised on-road quotation: ex-showroom, registration, insurance, TCS, "
     "accessories, and your exchange value if there is one."),
    ("Finance, if you need it",
     "We put your case to several partner banks and show the offers side by side, "
     "including the total interest in rupees over the full term."),
    ("Booking and allotment",
     "A booking amount confirms variant and colour. We give you the realistic "
     "allotment date, and tell you again if it changes."),
    ("Delivery",
     "Pre-delivery inspection with you present, documents handed over, and a walk "
     "through the controls before you drive out."),
]

# ========================================================= TESTIMONIALS ======
TESTIMONIALS = [
    ("Senthil Kumar", "Swift ZXi+ · Thanjavur", "SK", 5,
     "I had a quotation from another dealer that grew by eleven thousand rupees between "
     "the estimate and the invoice. Here the sheet I was given on day one is exactly "
     "what I paid. That is the whole reason I bought from Pillai & Sons."),
    ("Dr. Meenakshi Raman", "Grand Vitara Hybrid · Kumbakonam", "MR", 5,
     "I drive to Kumbakonam and back most days. The hybrid was explained to me properly "
     "— what it does in traffic, what it does not do on the highway — instead of just "
     "being sold to me. Six months in, the fuel figures are what they said."),
    ("A. Jeyaraman", "Ertiga ZXi CNG · Pattukkottai", "AJ", 5,
     "Seven seats and CNG for the running I do. They worked out my cost per kilometre "
     "on paper against the petrol version before I decided. Nobody had done that for me "
     "anywhere else."),
    ("Fathima Beevi", "Baleno Alpha · Thanjavur", "FB", 5,
     "The lady who took me for the test drive answered every question without once "
     "making me feel it was a silly one. I have bought cars before and that has not "
     "always been my experience."),
    ("R. Venkatesan", "True Value Dzire", "RV", 5,
     "A used car with the inspection report actually printed and handed over, and the RC "
     "transfer done by them. I collected it and the transfer message came through in "
     "twelve days as promised."),
    ("S. Abirami", "Maruti Driving School", "SA", 5,
     "I was genuinely frightened of driving. Thirty days later I drive to work alone. "
     "The instructor was patient in a way I did not expect."),
]

# ================================================================ TEAM =======
TEAM = [
    ("R. Pillai", "Managing Director", "RP",
     "Second generation in the business. Still meets most people who buy a car here, "
     "and still signs off every deviation from a quoted price."),
    ("S. Sundaram", "General Manager — Sales", "SS",
     "Runs the ARENA and NEXA sales floors. Twenty-two years in Maruti Suzuki retail, "
     "most of it in the delta districts."),
    ("K. Murugan", "Service Manager", "KM",
     "Maruti-trained, and the person to ask for when something has gone wrong twice. "
     "Holds the workshop to its promised delivery times."),
    ("Lakshmi Narayanan", "True Value In-charge", "LN",
     "Values every pre-owned car that comes through the yard and signs the inspection "
     "report that goes with it."),
    ("A. Fathima", "Finance and Insurance", "AF",
     "Puts your case to the partner banks and explains what the total interest actually "
     "comes to in rupees, not just as a rate."),
    ("T. Ravichandran", "Chief Instructor — Driving School", "TR",
     "Certified instructor with a licence-test pass record he is quietly proud of. "
     "Teaches highway confidence as seriously as parking."),
]

# =============================================================== FAQS ========
FAQ_GROUPS = [
    ("Buying a car", [
        ("What documents do I need to buy a car?",
         "Aadhaar and PAN, one address proof, passport photographs and your bank details. "
         "For a company purchase we also need the GST certificate and a board resolution. "
         "For finance the lender will ask for income proof — usually three months of "
         "salary slips or two years of returns."),
        ("How long is the waiting period?",
         "It varies by model, variant and colour, and it moves month to month. We give you "
         "the realistic date at booking rather than the optimistic one, and we call you if "
         "it changes."),
        ("Can I exchange my current car?",
         "Yes, any make or model. Our True Value team values it free of charge and the "
         "figure is set against your new car on the same invoice, which also reduces the "
         "amount you need to finance."),
        ("Do you deliver outside Thanjavur?",
         "We regularly deliver across Thanjavur district and to Kumbakonam, Pattukkottai, "
         "Orathanadu and the surrounding towns. Registration can be arranged for your home "
         "RTO."),
    ]),
    ("Prices and finance", [
        ("Are the prices on this website final?",
         "No. The figures shown are starting ex-showroom prices and are indicative — they "
         "change with variant, colour and manufacturer revisions. Your on-road price also "
         "includes registration, insurance and TCS. Ask us for a written on-road "
         "quotation, which is the number that actually binds."),
        ("What is included in the on-road price?",
         "Ex-showroom price, road tax and registration, insurance, TCS where applicable, "
         "and any accessories you choose. We itemise all of it on one sheet."),
        ("Which banks do you work with?",
         "Several public and private banks and NBFCs. We put your case to more than one "
         "and show the offers side by side — including the total interest in rupees over "
         "the full term, which is the comparison that matters."),
        ("Is a lower interest rate always the better loan?",
         "Not necessarily. A lower rate over a longer term can cost more in total than a "
         "higher rate over a shorter one, and processing fees and prepayment penalties "
         "differ between lenders. We show the full cost so you can compare properly."),
    ]),
    ("Service and warranty", [
        ("How often does my car need servicing?",
         "Maruti Suzuki's schedule for most current petrol models is every 10,000 km or 12 "
         "months, whichever comes first. CNG and older models differ — tell us the model "
         "and year and we will confirm."),
        ("Do you offer pick-up and drop?",
         "Yes, free within Thanjavur city limits for scheduled services. Book a day ahead "
         "so we can plan the driver's route."),
        ("What does the warranty cover?",
         "Manufacturing defects for the standard warranty period, subject to servicing at "
         "an authorised workshop within the prescribed intervals. Wear items such as brake "
         "pads, clutch plates, wiper blades and tyres are excluded, as is damage from "
         "accident or misuse."),
        ("Can I get a service estimate before booking?",
         "Yes. Tell us the model, year and running and we will estimate the applicable "
         "service. You approve it before any work starts."),
    ]),
    ("True Value and driving school", [
        ("What makes a True Value car different?",
         "A documented inspection across mechanicals, body and paperwork, chassis and "
         "engine numbers verified against the RC, a clear title with any loan closed, and "
         "a warranty. A private sale gives you none of that."),
        ("Do you buy cars outright?",
         "Yes, and you do not have to buy a new car from us to sell one to us. Bring it in "
         "for a free valuation — the offer stands for seven days."),
        ("Do I need a learner's licence before joining the driving school?",
         "No. We help you apply for the learner's licence as part of the course and support "
         "you through the driving test at the end."),
        ("Do you teach automatic cars?",
         "Yes. Tell us at enrolment and we will schedule you on an AMT or automatic "
         "training car."),
    ]),
]

FAQ_CATEGORIES = [
    ("Buying a car", "car", "Documents, waiting periods, exchange and delivery."),
    ("Prices and finance", "wallet", "On-road pricing, loans and what to compare."),
    ("Service and warranty", "wrench", "Intervals, pick-up and what is covered."),
    ("True Value and driving school", "certificate", "Pre-owned cars and learning to drive."),
]

# =============================================================== BLOG ========
POSTS = [
    {
        "key": "on-road-price",
        "slug": "what-on-road-price-actually-includes.html",
        "title": "What “on-road price” actually includes, line by line",
        "excerpt": "Ex-showroom is the number in the advertisement. Here is every other "
                   "line that sits between it and the amount you actually pay.",
        "date": "2026-07-22", "date_h": "22 Jul 2026", "day": "22", "mon": "JUL",
        "read": "6 min read", "tag": "Buying",
        "body": [
            ("p", "Almost every argument between a car buyer and a dealer starts in the "
                  "same place: the price in the advertisement is not the price on the "
                  "invoice. It was never meant to be — but nobody explains that early "
                  "enough."),
            ("h2", "Ex-showroom price"),
            ("p", "The manufacturer's price for the car including GST and cess. This is the "
                  "figure quoted in advertisements and on this website. Nobody pays only "
                  "this."),
            ("h2", "Road tax and registration"),
            ("p", "Paid to the Tamil Nadu government, calculated as a percentage of the "
                  "ex-showroom price. It varies with the price band and with whether the "
                  "vehicle is registered to an individual or a company. This is a "
                  "government charge — no dealer can discount it."),
            ("h2", "Insurance"),
            ("p", "Third-party cover is compulsory. Own-damage cover is not compulsory but "
                  "is unwise to skip, and is required in practice if you are financing the "
                  "car. You are free to arrange your own policy rather than take the one "
                  "offered — compare the two."),
            ("h2", "TCS"),
            ("p", "Tax collected at source applies on vehicles above ten lakh rupees. It is "
                  "not a dealer charge; it is adjusted against your income tax, so it comes "
                  "back to you when you file."),
            ("h2", "Accessories, extended warranty, service plans"),
            ("p", "All optional. All should appear as separate lines you can point at and "
                  "remove. If any of them arrive folded into a single unexplained figure, "
                  "ask for the breakdown."),
            ("blockquote", "One question settles most of it: “can I have the on-road price "
                           "itemised on one sheet, before I pay the booking amount?” Any dealer "
                           "who will not is telling you something."),
            ("h2", "What to compare between dealers"),
            ("p", "Compare the total on-road figure and the itemised sheet behind it, not "
                  "the discount headline. A large discount on the car, offset by a costly "
                  "insurance policy and a compulsory accessory pack, is not a better deal — "
                  "it is the same deal described differently."),
        ],
    },
    {
        "key": "petrol-cng-hybrid",
        "slug": "petrol-cng-or-hybrid-which-suits-your-running.html",
        "title": "Petrol, CNG or hybrid — work it out from your own running",
        "excerpt": "The right answer depends on how many kilometres you actually do in a "
                   "month. Here is the arithmetic, with the break-even points.",
        "date": "2026-06-18", "date_h": "18 Jun 2026", "day": "18", "mon": "JUN",
        "read": "7 min read", "tag": "Ownership",
        "body": [
            ("p", "Three fuel choices now sit in the same showroom, often on the same "
                  "model. The honest answer to “which is best” is that it depends entirely "
                  "on your monthly running, and it is worth ten minutes with a calculator "
                  "before deciding."),
            ("h2", "The rule of thumb"),
            ("ul", ["Under about 800 km a month: petrol. The cheaper purchase price will not "
                    "be recovered by fuel savings for years.",
                    "800 to 1,500 km a month: CNG usually wins on cost, if there is a "
                    "filling station on a route you already drive.",
                    "Above 1,500 km a month, mostly in traffic: a strong hybrid starts to "
                    "make real sense.",
                    "Long, steady highway runs: the hybrid advantage narrows, because "
                    "hybrids recover their energy from braking."]),
            ("h2", "What CNG actually costs you"),
            ("p", "The fuel is materially cheaper per kilometre. Against that: a higher "
                  "purchase price, boot space taken by the cylinder, a mandatory cylinder "
                  "test every few years, and slightly higher service costs. Factory-fitted "
                  "CNG keeps your warranty intact — an aftermarket kit generally does not, "
                  "and that is not a small detail."),
            ("h2", "What a strong hybrid actually does"),
            ("p", "It drives on the electric motor alone at low speed and recovers energy "
                  "when you brake, which is why the benefit is largest in traffic and "
                  "smallest on an open highway. There is nothing to plug in. The battery "
                  "carries its own warranty."),
            ("blockquote", "Bring your monthly running figure to the showroom and we will do "
                           "this arithmetic with you on paper, for your shortlist, before you "
                           "decide."),
            ("h2", "And the electric option"),
            ("p", "An EV makes sense when you can charge where you park and your daily "
                  "distance sits comfortably inside the range. If both are true, the running "
                  "cost is lower than anything else here. If either is not, it will "
                  "frustrate you."),
        ],
    },
    {
        "key": "first-service",
        "slug": "getting-the-most-from-your-first-service.html",
        "title": "Your first service: what to ask, and what to check afterwards",
        "excerpt": "Ten minutes of preparation is the difference between a service that "
                   "fixes things and one that just changes the oil.",
        "date": "2026-05-14", "date_h": "14 May 2026", "day": "14", "mon": "MAY",
        "read": "5 min read", "tag": "Service",
        "body": [
            ("p", "The first service sets the pattern for the relationship between you, the "
                  "car and the workshop. It is worth arriving prepared."),
            ("h2", "Before you go"),
            ("ul", ["Write down every noise, rattle or behaviour that has bothered you, and "
                    "when it happens — cold start, over speed bumps, only in the morning. "
                    "“There is a noise” is very hard to chase.",
                    "Note the odometer reading yourself.",
                    "Take out anything valuable.",
                    "Ask for the estimate in advance, not on collection."]),
            ("h2", "At the counter"),
            ("p", "Ask for a printed job card listing what will be done, and ask to be "
                  "called before anything is added to it. A good workshop offers this "
                  "without being asked."),
            ("h2", "When you collect the car"),
            ("ul", ["Check the invoice lists part numbers, not just descriptions.",
                    "Ask for the old parts back if anything significant was replaced. You "
                    "are entitled to them.",
                    "Check the odometer against the reading you noted.",
                    "Look at the service record before you drive away."]),
            ("blockquote", "Asking for replaced parts back is not rude, and no honest "
                           "workshop minds. It is simply how you verify that what you paid for "
                           "actually happened."),
            ("h2", "Afterwards"),
            ("p", "Drive it for a few days before deciding you are satisfied. If something "
                  "is not right, come back while it is clearly connected to the work — a "
                  "problem raised a week later is far easier to resolve than one raised "
                  "three months later."),
        ],
    },
]

# ============================================================== CAREERS ======
JOBS = [
    ("Sales Consultant — ARENA", "Thanjavur showroom", "Full time", "1+ years",
     "Take customers from first enquiry to delivery. Product training provided; what "
     "we cannot train is patience and straight dealing."),
    ("Sales Consultant — NEXA", "Thanjavur showroom", "Full time", "2+ years",
     "Premium retail experience preferred. A slower, more consultative sale than the "
     "ARENA floor."),
    ("Service Advisor", "Thanjavur workshop", "Full time", "2+ years",
     "The link between customer and technician. You will write job cards, explain "
     "estimates and make the follow-up calls."),
    ("Automobile Technician", "Thanjavur workshop", "Full time", "ITI / Diploma",
     "Periodic maintenance and diagnostics across the current Maruti Suzuki range. "
     "Maruti training provided and certified."),
    ("Driving Instructor", "Maruti Driving School", "Full time", "5+ years driving",
     "Valid licence and a clean record essential. Teaching experience welcome, but we "
     "will train the right person."),
    ("True Value Evaluator", "Thanjavur yard", "Full time", "3+ years",
     "Inspect and value incoming pre-owned cars. Mechanical knowledge and an unusually "
     "careful eye for accident repair."),
]

# ======================================================== HOME HIGHLIGHTS ====
HOME_STATS = [
    ("17", "", "Models across ARENA and NEXA"),
    ("5", "", "Businesses under one roof"),
    ("30", "+", "Years serving Thanjavur"),
    ("100", "%", "Maruti Genuine Parts"),
]
